# Configuration loaded from environment variables.
# Copy .env.example to .env and fill in your values.
# Never commit .env or credentials.json.

import os

from dotenv import load_dotenv
load_dotenv()

SHEET_ID = os.environ.get("SHEET_ID", "")
INGRESAR_DATOS_SHEET_ID = os.environ.get("INGRESAR_DATOS_SHEET_ID", "")

# Google Drive folder IDs
FOLDER_ID_FACTURAS = os.environ.get("FOLDER_ID_FACTURAS", "")
FOLDER_ID_CLIENTES_LOGOS = os.environ.get("FOLDER_ID_CLIENTES_LOGOS", "")

# Password gate for master data management
MAESTROS_PASSWORD = os.environ.get("MAESTROS_PASSWORD", "")
