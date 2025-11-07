# ============================================================
# 🌎 API DE DATOS DE INCENDIOS FORESTALES (JSON SDK)
# ============================================================

from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import json
import os

# ============================================================
# 🚀 CONFIGURACIÓN PRINCIPAL
# ============================================================

app = FastAPI(
    title="API Nacional de Incendios Forestales",
    description="Datos oficiales históricos de incendios forestales: Teziutlán y Nacional.",
    version="1.1.0",
    contact={
        "name": "Ing. Víctor Noé Martín Sierra",
        "url": "https://helenashop.com.mx",
        "email": "v33119521n@gmail.com",
    },
)

# --- Directorio base ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DOCS_DIR = os.path.join(BASE_DIR, "docs")

# ============================================================
# 🗂️ MONTAR CARPETAS ESTÁTICAS
# ============================================================

# Carpeta de datos JSON
app.mount("/data", StaticFiles(directory=DATA_DIR), name="data")

# Carpeta de documentación (HTML visual)
app.mount("/docs", StaticFiles(directory=DOCS_DIR), name="docs")

# Endpoint para abrir el index directamente
@app.get("/docs/index.html")
def docs_index():
    """Devuelve la página de documentación HTML principal"""
    return FileResponse(os.path.join(DOCS_DIR, "index.html"))

# ============================================================
# 📦 CARGA DE DATOS
# ============================================================

try:
    with open(os.path.join(DATA_DIR, "teziutlan.json"), encoding="utf-8") as f:
        DATA_TEZIUTLAN = json.load(f)

    with open(os.path.join(DATA_DIR, "nacional.json"), encoding="utf-8") as f:
        DATA_NACIONAL = json.load(f)
except Exception as e:
    DATA_TEZIUTLAN, DATA_NACIONAL = [], []
    print(f"⚠️ Error cargando datos: {e}")

# ============================================================
# 🏠 RUTA PRINCIPAL
# ============================================================

@app.get("/")
def home():
    """Información general del servicio API"""
    return {
        "proyecto": "API Nacional de Incendios Forestales",
        "version": "1.1.0",
        "autor": "Ing. Víctor Noé Martín Sierra",
        "contacto": "v33119521n@gmail.com",
        "endpoints": {
            "Datos Teziutlán": "/data/teziutlan",
            "Datos Nacional": "/data/nacional",
            "Documentación Visual": "/docs/index.html",
        },
    }

# ============================================================
# 🌄 ENDPOINT: TEZIUTLÁN
# ============================================================

@app.get("/data/teziutlan")
def get_teziutlan(
    año: int | None = Query(None, description="Filtrar por año (ejemplo: 2023)"),
    causa: str | None = Query(None, description="Filtrar por causa (ejemplo: Intencional)"),
):
    """Devuelve los datos de incendios de la región de Teziutlán."""
    datos = DATA_TEZIUTLAN

    if año:
        datos = [d for d in datos if d.get("año") == año]
    if causa:
        datos = [d for d in datos if causa.lower() in str(d.get("causa", "")).lower()]

    return JSONResponse(content=datos[:100])  # máximo 100 registros

# ============================================================
# 🇲🇽 ENDPOINT: NACIONAL
# ============================================================

@app.get("/data/nacional")
def get_nacional(
    entidad: str | None = Query(None, description="Filtrar por entidad (ejemplo: Puebla)"),
    año: int | None = Query(None, description="Filtrar por año (ejemplo: 2023)"),
):
    """Devuelve los datos nacionales consolidados."""
    datos = DATA_NACIONAL

    if entidad:
        datos = [d for d in datos if entidad.lower() in str(d.get("entidad", "")).lower()]
    if año:
        datos = [d for d in datos if d.get("año") == año]

    return JSONResponse(content=datos[:100])  # máximo 100 registros

# ============================================================
# ✅ FIN DEL ARCHIVO
# ============================================================
