# PDF Quote Generator

A standalone Python tool that batch-fills quote PDFs with dynamic rate data based on commission tiers. Designed for sales teams, brokers, or financing firms that generate proposals from standardized templates.

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
