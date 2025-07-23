# PDF Quote Generator

A standalone Python tool that batch-fills quote PDFs with dynamic rate data based on commission tiers. Designed for sales teams, brokers, or financing firms that generate proposals from standardized templates.

Issue - Client was manually updating rate multipliers for their pdf quotes on a monthly basis. They had 3 different forms, all with 6 different variants (for each commission tier). Each form had 12 hidden fields that housed the multipliers to calculate the payments. This equated to 216 fields that needed to be manually updated every month. Aesthetic updates to the forms were also cumbersome to do the nature of manual edits. To create a multipliers each month, an employee had to manually create them, one by one, using different scenarios in T-Value Software. Monthly time allocation for updates was 20hrs +.

Solution - I created a Google Sheet that utilized formulas to mass calculate the factor rates for them. All they needed to do was input the interest rate and all of the corresponding multipliers would populate. Another Google Sheet was created and linked to the rate control sheet. The secondary sheet utilized Apps Script to export the rates & needed field names to JSON. The JSON were housed in a shared folder on Google Drive.   Python would then query the shared folder to automatically update the JSON folder on a local level with the latest  version. Python then takes each of the three blank templates, and creates all 6 of the different variants for each (18 pdfs in total)  and fills each form with the appropriate rate multipliers for each tier. The company only needs to maintain three main templates now, making aesthetic changes significantly easier, as the main templates do not house any specific multipliers themselves. 
Monthly updates now take less than 5 minutes.   

---

## 🚀 Features

- Autofills rate data into pre-mapped PDF form fields
- Supports multiple commission tiers (e.g. A–F)
- Dynamic date and tier auto-population for tracking
- Syncs rate JSON files from a Google Drive folder
- Simple GUI built with Tkinter (no command-line needed)
- Buildable to `.exe` for Windows users

---

## 🖥️ GUI Preview

- Click **Run Batch Processing**
- All PDFs from `/Input_PDFs/` are filled using the proper rate file and tier logic
- Outputs are saved in `/Output_PDFs/`

---

## 📁 Folder Structure

```plaintext
project/
├── main.py
├── requirements.txt
├── creds.json               # (placeholder — see below)
├── json_files/              # Rate tables in JSON format
├── Input_PDFs/              # Blank template PDFs to populate
├── Output_PDFs/             # Filled results (created automatically)
├── Assets/                  # Optional icon
└── build_scripts/           # Optional: EXE and installer scripts
```

---

## 🔐 Google Drive Integration

To auto-download updated rate tables from Google Drive:

1. Create a [Google Service Account](https://console.cloud.google.com/)
2. Enable the **Google Drive API**
3. Download the `creds.json` file and place it in the root folder
4. Share your target Google Drive folder with the service account email

See `creds.json` (dummy file provided) for instructions.

---

## 🛠️ Build EXE (Optional)

Install dependencies and run:

```bash
pyinstaller --onefile --windowed --icon=assets/app_icon.ico ^
  --add-data "creds.json;." main.py
```

This creates a standalone `.exe` in the `/dist` folder.

---

## 🧪 Requirements

Install required packages with:

```bash
pip install -r requirements.txt
```

---

## 📝 Customization

- Edit the `RATE_FILES` dictionary in `main.py` to match your form types
- Adjust `TIERS` to reflect your actual commission letters
- PDF field names are mapped via JSON keys like `ZeroDown_Term60_Over50k`

---

## 📄 License

MIT — use it, break it, ship it.
