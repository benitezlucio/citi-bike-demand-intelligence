# Etapa 03 — Metodología y resultados de Machine Learning

**Estado:** notebook de ML incorporado al repositorio, con revisión estructural y ejecución retrospectiva anterior proporcionada por el autor. La versión revisada publicada **todavía requiere una ejecución integral con datos reales**. No se ha demostrado despliegue ni operación en tiempo real.

## 1. Pregunta y audiencia

**Problema de regresión:** predecir el número de viajes de Citi Bike que comenzarán en una hora futura en todo NYC, con anticipación de una hora antes del inicio de ese intervalo.

**Audiencia:** planificación y analistas de operaciones. Se trata de **inicios de viajes agregados**, no de bicicletas disponibles por estación ni demanda insatisfecha.

**Hipótesis:** incorporar pronósticos meteorológicos históricos de temperatura, precipitación y viento puede mejorar la predicción frente a emplear solamente calendario y demanda pasada.

## 2. Fuentes y granularidad

- [Historial de Citi Bike](https://citibikenyc.com/system-data), agregado en el pipeline de [Etapa 01](../notebooks/01_data_acquisition_preparation.ipynb). Los 44.302.480 viajes de 2024 están resumidos en **8.783 etiquetas horarias locales**.
- [Open-Meteo Previous Runs API](https://open-meteo.com/en/docs/previous-runs-api), modelo `gfs_global`, campos `temperature_2m_previous_day1`, `precipitation_previous_day1`, `wind_speed_10m_previous_day1`, consulta y alineación en UTC.
- En las consultas reales realizadas por el autor, la cobertura comienza el **19 de enero de 2024 a las 12:00 UTC**; se encontraron **8.345 horas de pronósticos completos** en el año local y 439 sin clima completo.
- Se excluye la hora local ambigua **2024-11-03 01:00** de los viajes para esta primera versión, dado que contiene dos intervalos físicos en un solo registro del EDA. Al calcular los rezagos UTC, otras ocho observaciones pierden referencias históricas, resultando **8.335 horas de modelado**.
- El CSV horario principal no vuelve a descargarse; la caché de GFS es regenerable y no se versiona.

## 3. Qué se conoce al emitir la predicción

Para predecir viajes **15:00–16:00** a las **14:00** hora de Nueva York, `lag_2h` toma el número de viajes de **13:00–14:00**. Se asume que el conteo de esa hora se publica inmediatamente al concluir.

Las diferencias de `lag_2h`, `lag_3h`, `lag_24h` y `lag_168h` se calculan con intervalos UTC, no con desplazamientos de filas. La media móvil usa solamente intervalos que ya finalizaron.

`previous_day1` indica una anticipación **nominal** de 24 horas respecto de la validez de cada pronóstico. En este notebook no se reconstruyó independientemente el timestamp exacto de publicación de cada corrida. Temperatura y viento se alinean a la hora de inicio; la precipitación acumulada para 15:00–16:00 se toma de la etiqueta meteorológica de las **16:00**. Esta interpretación depende de la definición temporal de Open-Meteo.

**Límite:** sin medir los instantes reales de publicación y la latencia de conteos horarios, no puede afirmarse que el experimento representa una operación automatizada disponible en producción. Se trata de un ejercicio de *backtesting* de condiciones nominales.

## 4. Diseño experimental

- **Objetivo:** `ride_count`.
- **Predictores sin clima (12):** codificaciones cíclicas de hora, día de semana y mes; indicador de fin de semana; `lag_2h`, `lag_3h`, `lag_24h`, `lag_168h` y media de tres horas históricas.
- **Predictores con clima (15):** las doce anteriores más temperatura, precipitación y viento pronosticados.
- **Modelos:** Ridge con `StandardScaler` dentro de `Pipeline`, Random Forest y HistGradientBoostingRegressor. Baselines de persistencia, mismo horario día anterior y mismo horario semana anterior.
- **Entrenamiento:** enero (desde el 19) a agosto. **Validación:** septiembre–octubre. **Test reservado:** noviembre–diciembre, sin utilizarse en tuning.
- **Validación cruzada temporal:** cuatro folds de `TimeSeriesSplit`, con `gap=1` en el notebook revisado.
- **Optimización:** `RandomizedSearchCV` con quince combinaciones de hiperparámetros de Gradient Boosting; la configuración inicialmente elegida se conservó para los experimentos posteriores.
- **Métricas:** MAE primario, RMSE complementario. Se analizan los errores por lluvia pronosticada, tipo de día y hora pico.
- **Interpretación:** permutación de variables sobre validación. Importancia predictiva no significa causalidad ni se puede sumar entre variables correlacionadas.

## 5. Resultados registrados de la ejecución anterior

Estos números fueron **comunicados desde el notebook original por su autor**; no representan una ejecución nueva comprobada de la versión editorial publicada.

| Evaluación test nov–dic 2024 | MAE | RMSE |
|---|---:|---:|
| Baseline semanal | 1378,97 | 2082,11 |
| Gradient Boosting sin pronósticos | **609,17** | 971,88 |
| Gradient Boosting con pronósticos | 612,59 | **943,70** |

El mejor MAE es el del modelo **sin clima**, con una mejora de aproximadamente **55,8 %** frente al baseline semanal. El mejor RMSE lo alcanza el modelo **con clima**, con una reducción aproximada de **2,9 %** frente al otro ensemble.

Durante **204 horas con lluvia pronosticada** del test, el MAE fue **1002,35** sin clima y **658,27** con clima, una reducción del **34,3 %**. No se eligieron ni modificaron hiperparámetros en función de este resultado del test.

En validación (septiembre–octubre), el modelo con clima redujo el MAE frente al sin clima (745,03 → 710,50), pero en 73 horas con lluvia pronosticada empeoró el MAE; la evidencia indica variación de resultados entre períodos. La temperatura fue la variable meteorológica de mayor importancia por permutación entre las tres incorporadas, mientras rezagos históricos y horario dominaron el modelo.

## 6. Interpretación y decisiones

**Conclusión conservadora:** los modelos ensemble superaron claramente el baseline en el test 2024. La información meteorológica es útil en algunos escenarios (en particular lluvia pronosticada) y reduce el RMSE, pero no garantiza una mejora del MAE total.

**No se concluye:** causalidad meteorológica, mejora de disponibilidad por estación, reducción medida de costos, generalización a años nuevos ni existencia de un servicio en vivo.

**Próximos pasos posibles (fuera de la entrega):** validar nuevas temporadas, medir latencias reales, estudiar calibración y cuantificar beneficios de negocio con datos de estaciones.

## 7. Qué verificar para publicar resultados como reproducidos

1. Abrir [notebook 03](../notebooks/03_ml_hourly_demand_forecasting.ipynb) con el CSV procesado original.
2. Comprobar acceso a Open-Meteo o a una caché generada por ese mismo endpoint y parámetros.
3. Ejecutar desde cero con **Restart & Run All** sin cambiar modelos, predictores ni rango de test.
4. Comparar todas las métricas con la sección 5; registrar cualquier discrepancia y su causa.
5. Guardar salidas ejecutadas y verificar que los gráficos y archivos adjuntos se renderizan.
6. Completar el [checklist académico](CODERHOUSE_ML_CHECKLIST_ES.md).
