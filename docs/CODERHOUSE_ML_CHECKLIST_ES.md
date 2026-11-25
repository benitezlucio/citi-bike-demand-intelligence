# Checklist Coderhouse — Machine Learning (Etapa 03)

**Archivo académico actual:** [Citi_Bike_Coderhouse_Entrega_ML.ipynb](../entregas/coderhouse/Citi_Bike_Coderhouse_Entrega_ML.ipynb)

## Consigna y verificación

| Requisito | Dónde aparece en el notebook | Estado |
|---|---|---|
| Abstract, motivación y audiencia | Sección 2 | Incluido |
| Pregunta concreta, problema de regresión | Sección 2 | Incluido |
| EDA descriptivo breve + faltantes | Sección 5 | Incluido |
| Ingeniería de atributos, encoding y normalización | Sección 7, Ridge en sección 9 | Incluido |
| Entrenamiento de al menos dos modelos | Sección 9 (Ridge, RF, Gradient Boosting) | Incluido |
| Validación cruzada | Secciones 9–11 (`TimeSeriesSplit`) | Incluido |
| Optimización de hiperparámetros | Sección 10 (`RandomizedSearchCV`) | Incluido |
| Métricas para elegir el mejor modelo | Secciones 9, 11 y 13 (MAE/RMSE) | Incluido |
| Ensemble Models | Random Forest y Gradient Boosting | Incluido |
| Gráficos e interpretación | Secciones 5, 9, 11–14 | Incluido |
| Ejecución integral tras edición | Todo el notebook | **Pendiente** |
| Inspección visual de salidas generadas | Todo el notebook | **Pendiente** |

## Instrucciones de ejecución

1. Clonar [repositorio](https://github.com/benitezlucio/citi-bike-demand-intelligence) y usar Python 3.11 o equivalente.
2. Instalar con `python -m pip install -r requirements.txt`.
3. Ejecutar el notebook desde la raíz o `notebooks/`, o abrirlo en Google Colab con red para clonación y descarga.
4. La primera ejecución descarga pronósticos de Open-Meteo; si la API falla, revisar conectividad, límites de acceso y caché.
5. Hacer **Restart & Run All**, verificar la salida final y guardar el archivo **con outputs**.
6. Para entrega exclusivamente por archivo, verificar que Colab abra el notebook y encuentre las dependencias. Las salidas ejecutadas ayudan al corrector cuando no hay acceso a internet.
7. Si se solicita URL en vez de un archivo, usar la ruta directa de la entrega ML y **no** el notebook de EDA anterior.

## Verificaciones finales antes de subir

- [ ] Todos los códigos terminan sin excepción en un kernel limpio con datos reales.
- [ ] La tabla real y la cobertura climatológica coinciden con las fuentes.
- [ ] Los datos procesados están disponibles o el notebook puede clonarlos.
- [ ] Los gráficos renderizan con títulos, ejes, unidades y leyendas legibles.
- [ ] Las tablas de validación y test se reproducen o las diferencias se documentan.
- [ ] Se comprende el alcance retrospectivo, DST, cobertura desde enero 19 y el supuesto de disponibilidad de pronósticos.
- [ ] La sección final no afirma beneficios operativos que no medimos.
- [ ] Se indica el archivo correcto de ML y se evita entregar accidentalmente el archivo viejo de EDA.
