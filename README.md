# Streamlit Web App Template

## 🛠️ Getting Started

1. Create and activate the environment:
   ```bash
   conda create -n streamlit_webapp python=3.10
   conda activate streamlit_webapp
   pip install -r requirements.txt
   ```

2. Launch the app:
   ```bash
   streamlit run main.py
   ```

3. To enable Google Sheets integration, create a `.streamlit/secrets.toml` file
   with your `gcp_service_account` credentials. Without this file the app will
   run in read‑only mode and new entries will not be stored.

## 📁 Folder Structure

- `main.py`: Your main Streamlit app.
- `requirements.txt`: Python dependencies.
- `.vscode/settings.json`: Preconfigured for VS Code.
- `data/`: Put your CSVs or data files here.
