# ============================================================
# 🌎 API DE DATOS DE INCENDIOS FORESTALES (JSON SDK)
# ============================================================

from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import json
import os

app = FastAPI(
    title="API de Incendios Forestales",
    description="Datos oficiales históricos de incendios forestales, divididos en Teziutlán y Nacional.",
    version="1.1.0",
    contact={
        "name": "Ing. Víctor Noé Martín Sierra",
        "url": "https://helenashop.com.mx",
        "email": "v33119521n@gmail.com",
    },
)

# --- Servir el dashboard visual HTML ---
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
    """Información general de la API"""
    return {
        "proyecto": "API de Incendios Forestales",
        "version": "1.1.0",
        "autor": "Ing. Víctor Noé Martín Sierra",
        "contacto": "v33119521n@gmail.com",
        "endpoints": {
            "Datos Teziutlán": "/data/teziutlan",
            "Datos Nacional": "/data/nacional",
            "Documentación Visual": "/docs",
        },
    }


# --- ENDPOINT: TEZIUTLÁN ---
@app.get("/data/teziutlan")
def get_teziutlan(
    año: int | None = Query(None, description="Filtrar por año (ejemplo: 2023)"),
    causa: str | None = Query(None, description="Filtrar por causa (ejemplo: Intencional)"),
):
    """Devuelve los datos de incendios en Teziutlán (opcionalmente filtrados)."""
    datos = DATA_TEZIUTLAN
    if año:
        datos = [d for d in datos if d.get("año") == año]
    if causa:
        datos = [d for d in datos if causa.lower() in str(d.get("causa", "")).lower()]
    return JSONResponse(content=datos[:100])  # se devuelven máximo 100 registros


# --- ENDPOINT: NACIONAL ---
@app.get("/data/nacional")
def get_nacional(
    entidad: str | None = Query(None, description="Filtrar por entidad (ejemplo: Teziutlán)"),
    año: int | None = Query(None, description="Filtrar por año (ejemplo: 2023)"),
):
    """Devuelve los datos nacionales (opcionalmente filtrados)."""
    datos = DATA_NACIONAL
    if entidad:
        datos = [d for d in datos if entidad.lower() in str(d.get("entidad", "")).lower()]
    if año:
        datos = [d for d in datos if d.get("año") == año]
    return JSONResponse(content=datos[:100])
