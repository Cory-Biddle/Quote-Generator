import os
import sys  # [MODIFIED]
import json
import io
from pathlib import Path
from tkinter import Tk, Label, Button, messagebox
from pdfrw import PdfReader, PdfWriter, PdfDict
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

# --- CONFIG ---
BASE_DIR = Path.home() / "Documents" / "PaymentCalculator"
INPUT_DIR = BASE_DIR / "Input_PDFs"
OUTPUT_DIR = BASE_DIR / "Output_PDFs"
JSON_DIR = BASE_DIR / "json_files"
REQUIRED_FOLDERS = [INPUT_DIR, OUTPUT_DIR, JSON_DIR]

RATE_FILES = {
    "ABC": JSON_DIR / "rates_ABC.json",    # Identifies which form based on keyword in name, then assigns appropriate multipliers
    "XYZ": JSON_DIR / "rates_XYZ.json",    # Update these to match your real JSON file names and identifiers
    "123": JSON_DIR / "rates_123.json", 
}

TIERS = ["A", "B", "C", "D", "E", "F"]       #Replace with your correct tiers embedded in your JSON files

# --- GOOGLE DRIVE SYNC ---
SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]

# Determine dynamic path to creds.json whether running as .py or .exe
if getattr(sys, "frozen", False):
    APP_PATH = Path(sys._MEIPASS)  # bundled path for .exe
else:
    APP_PATH = Path(__file__).parent

SERVICE_ACCOUNT_FILE = APP_PATH / "creds.json"  # creds.json is excluded from public repo; required for Google Drive sync
FOLDER_ID = "enter_yours_here"    # replace with your true folder link 


def download_json_files_from_drive():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    service = build("drive", "v3", credentials=creds)

    results = (
        service.files()
        .list(
            q=f"'{FOLDER_ID}' in parents and name contains 'rates_' and mimeType='application/json'",
            fields="files(id, name)",
        )
        .execute()
    )

    files = results.get("files", [])
    if not files:
        print("[!] No JSON files found in Drive folder.")
        return

    JSON_DIR.mkdir(parents=True, exist_ok=True)

    for file in files:
        file_id = file["id"]
        file_name = file["name"]
        request = service.files().get_media(fileId=file_id)
        fh = io.FileIO(JSON_DIR / file_name, "wb")
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
        print(f"[↓] Downloaded {file_name}")


# --- UTILITIES ---
def ensure_folders():
    for folder in REQUIRED_FOLDERS:
        folder.mkdir(parents=True, exist_ok=True)


def get_term_and_tier(filename):
    term = None
    tier = None
    for t in RATE_FILES:
        if t.lower() in filename.lower():
            term = t
            break
    for letter in TIERS:
        if f" {letter}" in filename or f"_{letter}" in filename:
            tier = letter
            break
    return term, tier


from datetime import datetime


def fill_pdf_fields(input_path, output_path, field_values, tier=None):
    # Inject dynamic date and tier
    today = datetime.today().strftime("%B %Y")
    field_values = dict(field_values)  # clone so we don't mutate original
    if tier:
        field_values["hidden_tier"] = tier
    field_values["hidden_date"] = today

    pdf = PdfReader(str(input_path))
    for page in pdf.pages:
        annotations = page.get("/Annots")
        if annotations:
            for annot in annotations:
                if annot["/Subtype"] == "/Widget" and annot.get("/T"):
                    field_name = annot["/T"][1:-1]
                    if field_name in field_values:
                        annot.update(
                            PdfDict(
                                V=field_values[field_name],
                                DV=field_values[field_name],
                                Ff=1,
                                AP=None,
                            )
                        )
    PdfWriter().write(str(output_path), pdf)


def process_all_pdfs():
    ensure_folders()
    input_files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(".pdf")]
    if not input_files:
        messagebox.showerror("No PDFs Found", f"No PDFs found in '{INPUT_DIR}' folder.")
        return

    for file in input_files:
        term, _ = get_term_and_tier(file)
        if not term:
            print(f"[!] Skipped: '{file}' — Missing term (e.g., '60', '72', etc.).")
            continue

        rate_path = RATE_FILES.get(term)
        if not rate_path or not rate_path.exists():
            print(f"[!] Rate file missing: {rate_path.name}")
            continue

        with open(rate_path, "r") as f:
            rates = json.load(f)

        input_path = INPUT_DIR / file

        for tier in TIERS:
            if tier not in rates:
                print(f"[!] Tier '{tier}' missing in {rate_path.name}, skipping.")
                continue

            base_name = Path(file).stem
            from datetime import datetime

            date_str = datetime.today().strftime("%B %Y")  # e.g., July 2025
            output_file = f"{base_name} {tier} {date_str}.pdf"
            output_path = OUTPUT_DIR / output_file

            print(
                f"[+] Generating '{output_file}' using {term} rates for Tier '{tier}'..."
            )
            fill_pdf_fields(input_path, output_path, rates[tier], tier)

    messagebox.showinfo("Done", "✅ All PDFs processed for all tiers.")


# --- GUI ---
def run_all_steps():
    try:
        download_json_files_from_drive()
        process_all_pdfs()
    except Exception as e:
        messagebox.showerror("Error", str(e))


root = Tk()
root.title("Payment Calculator Generator")
root.geometry("520x180")

Label(root, text="PDF Injector - Batch Mode", font=("Arial", 14, "bold")).pack(pady=10)
Button(
    root, text="Run Batch Processing", command=run_all_steps, width=30, height=2
).pack(pady=10)
Label(
    root,
    text=f"Input PDFs in folder: '{INPUT_DIR}'\nOutput will appear in: '{OUTPUT_DIR}'",
    font=("Arial", 9),
).pack()

root.mainloop()
