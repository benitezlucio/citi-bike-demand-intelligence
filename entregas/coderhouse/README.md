# Coderhouse — Entregas académicas

Esta carpeta contiene **materiales de entrega**, separados deliberadamente de los notebooks y del pipeline principal. Se pueden retirar al finalizar la cursada sin afectar las etapas 01, 02 y 03.

## Entrega actual: Machine Learning · Etapa 03

**Archivo a presentar:** [Citi_Bike_Coderhouse_Entrega_ML.ipynb](Citi_Bike_Coderhouse_Entrega_ML.ipynb).

Es la copia académica del [notebook principal de forecasting](../../notebooks/03_ml_hourly_demand_forecasting.ipynb). Incluye abstract y audiencia, problema de regresión, EDA breve, ingeniería de atributos y estandarización para Ridge, tres modelos ML, validación cruzada temporal, RandomizedSearchCV, selección por MAE/RMSE, análisis de error e interpretación de resultados.

**Para evaluadores:**
1. Instalar dependencias desde [requirements.txt](../../requirements.txt) si corresponde.
2. Ejecutar desde la raíz del repositorio o `notebooks/`; en Colab el notebook intenta clonar el repositorio público si no detecta los CSV.
3. La primera ejecución requiere conexión para recuperar pronósticos históricos GFS de Open-Meteo; después usa caché local.
4. Ejecutar **Restart & Run All** y guardar las salidas antes de presentar el notebook final. Los resultados del resumen ejecutivo son **valores registrados de una ejecución previa**; aún falta reejecutar íntegramente la edición publicada.
5. Revisar [checklist académico y de reproducibilidad](../../docs/CODERHOUSE_ML_CHECKLIST_ES.md) y [limitaciones de ML](../../docs/ML_FORECASTING_ES.md).

## Materiales de entrega anterior: EDA

- [Citi_Bike_Coderhouse_Entrega_Academica.ipynb](Citi_Bike_Coderhouse_Entrega_Academica.ipynb): síntesis del EDA y las seis hipótesis.
- [Citi_Bike_Presentacion_Ejecutiva_Coderhouse.pptx](Citi_Bike_Presentacion_Ejecutiva_Coderhouse.pptx): presentación ejecutiva de la fase de EDA.

**No confundir:** esos dos archivos pertenecen al trabajo anterior y no sustituyen la entrega actual de Machine Learning.
