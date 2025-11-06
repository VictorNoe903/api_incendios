# ============================================================
# 🌎 API DE DATOS DE INCENDIOS FORESTALES (JSON SDK)
# ============================================================

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import json
import os

app = FastAPI(
    title="API Nacional de Incendios Forestales",
    description="Datos oficiales históricos de incendios forestales, divididos en Teziutlán y Nacional.",
    version="1.0.0",
    contact={
        "name": "Ing. Víctor Noé",
        "url": "https://helenashop.com.mx",
        "email": "v33119521n@gmail.com",
    },
)

# --- Servir el dashboard (documentación visual HTML) ---
app.mount("/docs", StaticFiles(directory="docs", html=True), name="docs")

# --- Cargar datasets JSON ---
BASE_PATH = os.path.join(os.getcwd(), "data")
with open(os.path.join(BASE_PATH, "teziutlan.json"), encoding="utf-8") as f:
    DATA_TEZIUTLAN = json.load(f)
with open(os.path.join(BASE_PATH, "nacional.json"), encoding="utf-8") as f:
    DATA_NACIONAL = json.load(f)


# --- RUTA RAÍZ ---
@app.get("/")
def home():
    return {
        "proyecto": "API Nacional de Incendios Forestales",
        "version": "1.0",
        "autor": "Ing. Víctor Noé",
        "endpoints": {
            "Datos Teziutlán": "/data/teziutlan",
            "Datos Nacional": "/data/nacional",
            "Documentación Visual": "/docs",
        },
    }


# --- ENDPOINTS PRINCIPALES ---
@app.get("/data/teziutlan")
def get_teziutlan():
    return JSONResponse(content=DATA_TEZIUTLAN)

@app.get("/data/nacional")
def get_nacional():
    return JSONResponse(content=DATA_NACIONAL)
