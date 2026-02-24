# Streamlit + Google Workspace POC

A **proof of concept** web app for exploring Streamlit’s capabilities and integrating with Google Sheets and Google Drive. The domain (agricultural / asparagus sales) is secondary; the focus is on trying different features and patterns.

---

## 🎯 Goals

This POC is used to learn and practice:

| Capability | What I'm Trying |
|------------|-----------------|
| **Streamlit** | Multi-page navigation, forms, session state, file uploads, caching |
| **Google Sheets API** | CRUD operations via gspread, reading/writing from multiple worksheets |
| **Google Drive API** | Uploading files (PDFs, images), public sharing links |
| **Auth patterns** | Environment-aware credentials (Streamlit Cloud secrets vs local `credentials.json`) |
| **Form patterns** | Reusable form builders, validation, add/edit/delete flows |
| **Data layer** | Loaders, writers, records abstraction over Sheets |
| **UI patterns** | Sidebar navigation, tabbed flows, password gate, styled components |

---

## 📁 Project Structure

```
├── main.py                 # App entry point, sidebar navigation, service initialization
├── config.py               # Loads config from environment variables
├── .env.example            # Template for .env (copy to .env, never commit .env)
├── requirements.txt        # Dependencies
│
├── views/                  # View modules (one per section)
│   ├── gestionar_maestros  # Master data CRUD (Agricultores, Clientes, Productos, etc.)
│   ├── ingresar_datos      # Transaction entry (Facturas, Folios)
│   ├── procesar_datos      # Placeholder
│   └── visualizar_reportes # Placeholder
│
└── utils/                  # Shared utilities
    ├── auth.py             # Google API credentials (Cloud + local)
    ├── loaders.py          # Load Sheets → DataFrame
    ├── writers.py          # Append rows to Sheets
    ├── records.py          # add / edit / delete record helpers
    ├── forms.py            # Reusable form layouts
    ├── validators.py       # Email, phone, currency, uniqueness
    ├── uploader.py         # Drive upload + public share
    └── facturas_helpers.py # Invoice-specific save/load logic
```

---

## 🛠️ Setup

1. **Environment:**
   ```bash
   conda create -n streamlit_webapp python=3.10
   conda activate streamlit_webapp
   pip install -r requirements.txt
   ```

2. **Configuration:**
   - Copy `.env.example` to `.env` and fill in your values
   - Required: `SHEET_ID`, `INGRESAR_DATOS_SHEET_ID`, `FOLDER_ID_FACTURAS`, `FOLDER_ID_CLIENTES_LOGOS`, `MAESTROS_PASSWORD`
   - Never commit `.env` (it is in `.gitignore`)

3. **Google APIs:**
   - Create a GCP project and enable **Google Sheets API** and **Google Drive API**
   - Create a service account and download `credentials.json`
   - Place `credentials.json` in the project root (for local runs)
   - For Streamlit Cloud: use `st.secrets["gcp_service_account"]` with the JSON content and set env vars in the app settings

4. **Run:**
   ```bash
   streamlit run main.py
   ```

---

## 📋 Implemented Sections

| Section | Status | Capabilities Explored |
|---------|--------|------------------------|
| **Gestionar Maestros** | ✅ | CRUD on Agricultores, Clientes, Productos, Comisiones, Cajas; password gate; Drive upload for logos |
| **Ingresar Datos** | ✅ | Facturas with header + detail, Drive upload for documents, form-based entry |
| **Procesar Datos** | 🚧 | Placeholder |
| **Ver Reportes** | 🚧 | Placeholder |

---

## 📦 Dependencies

- `streamlit` — Web app
- `pandas` — Data handling
- `gspread` — Google Sheets
- `oauth2client` — Service account auth
- `google-api-python-client` — Drive API
- `python-dotenv` — Load `.env` into environment

---

## 📌 Notes

- **Domain:** Agricultural / asparagus sales (farmers, clients, products, invoices). The data model is domain-specific, but the integration patterns are reusable.
- **Never commit:** `credentials.json`, `.env`, or any file with real API keys or passwords. Use `.env.example` as a template.
