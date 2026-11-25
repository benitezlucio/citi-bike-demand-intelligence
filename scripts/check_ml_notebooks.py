#!/usr/bin/env python3
"""Controles estáticos de la entrega ML. No entrena modelos ni exige red."""

import ast
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / "notebooks" / "03_ml_hourly_demand_forecasting.ipynb"
ACADEMIC = ROOT / "entregas" / "coderhouse" / "Citi_Bike_Coderhouse_Entrega_ML.ipynb"
DATA = ROOT / "data" / "processed" / "citibike_analysis_hourly_2024.csv"

errors = []

def check_notebook(path):
    if not path.is_file():
        errors.append(f"No existe {path.relative_to(ROOT)}")
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        errors.append(f"JSON inválido: {path.name}: {exc}")
        return None
    if payload.get("nbformat") != 4:
        errors.append(f"Versión de notebook inesperada: {path.name}")
    code = []
    markdown = []
    for index, cell in enumerate(payload.get("cells", [])):
        source = cell.get("source", "")
        source = "".join(source) if isinstance(source, list) else str(source)
        if cell.get("cell_type") == "code":
            try:
                ast.parse(source, filename=f"{path.name}:celda-{index}")
            except SyntaxError as exc:
                errors.append(f"Error de sintaxis {path.name} celda {index}: {exc}")
            code.append(source)
        elif cell.get("cell_type") == "markdown":
            markdown.append(source)
            # Los esquemas deben estar guardados en el notebook.
            for image in ("resumen_test.png", "modelos_esquema.png"):
                if f"attachment:{image}" in source:
                    if image not in cell.get("attachments", {}):
                        errors.append(f"Falta adjunto {image} en {path.name}")
    combined = "\n".join(code)
    for required in (
        "TimeSeriesSplit", "RandomizedSearchCV", "Ridge",
        "RandomForestRegressor", "HistGradientBoostingRegressor",
        "StandardScaler", "mean_absolute_error", "permutation_importance",
        "forecast_precipitation",
    ):
        if required not in combined:
            errors.append(f"Componente faltante {required} en {path.name}")
    if len(code) < 15 or len(markdown) < 12:
        errors.append(f"Cuaderno incompleto: {path.name}")
    return payload


a = check_notebook(MASTER)
b = check_notebook(ACADEMIC)
if a is not None and b is not None and a != b:
    errors.append("La copia académica no coincide con el notebook principal")

if not DATA.is_file():
    errors.append("Falta el CSV horario del proyecto")

requirements = (ROOT / "requirements.txt").read_text(encoding="utf-8")
if "scikit-learn" not in requirements:
    errors.append("Falta scikit-learn en requirements.txt")

if errors:
    print("VALIDACIÓN ESTÁTICA: ERROR")
    for error in errors:
        print(" -", error)
    sys.exit(1)

print("VALIDACIÓN ESTÁTICA: OK")
print(f"Notebook principal y copia académica coinciden: {len(a['cells'])} celdas")
print("Sintaxis Python, adjuntos, componentes y CSV: OK")
print("IMPORTANTE: esto NO acredita ejecución de modelos con datos reales.")
