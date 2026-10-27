# Citi Bike Demand Intelligence — Hallazgos del EDA (2024)

> Reporte de resultados analíticos a partir del notebook completo y publicado en [`notebooks/02_eda_insights.ipynb`](../notebooks/02_eda_insights.ipynb).

## Objetivo y fuentes

**Pregunta:** ¿Qué factores temporales, climáticos y de comportamiento están asociados con la demanda de Citi Bike y cómo pueden utilizarse los datos históricos para entender los períodos de mayor y menor utilización?

- **Citi Bike Trip History:** 44.302.480 viajes iniciados entre enero y diciembre de 2024.
- **Open-Meteo:** temperatura, precipitación, nieve, viento, humedad y sensación térmica, con referencia geográfica en Nueva York.
- **Granularidad principal:** 8.783 etiquetas horarias locales distintas, considerando el cambio de horario de verano de Nueva York.
- **Segmentación:** tipo de usuario (member/casual) y bicicleta (classic/electric).
- **Estaciones:** 44.272.646 viajes con origen identificado; 29.834 viajes sin estación de origen válida se excluyen solamente del análisis espacial.

## Resumen de hipótesis

| Hipótesis | Resultados observados | Veredicto |
|---|---|---|
| **H1. Horario** | Picos a las 08:00 (7.468 viajes/h) y 17:00 (11.147 viajes/h); el máximo supera un 121% la media horaria general. | Parcialmente apoyada: no se identifica el propósito de cada viaje. |
| **H2. Laborables vs. fines de semana** | Laborables: máximos a las 08:00 y 17:00. Fines de semana: perfil más gradual, pico a las 15:00. Entre 12:00 y 16:00 se concentra 28,89% del perfil laboral y 39,22% del perfil de fin de semana. | Apoyada. |
| **H3. Member vs. casual** | Members: 80,7% de los viajes. Demanda diaria member: −21,18% en fines de semana; casual: +39,14%. Participación casual: 16,84% laboral y 26,33% fin de semana. | Apoyada. |
| **H4. Clima** | Precipitación: −32,43% bruto y −32,46% estratificado por mes/hora/tipo de día (343 grupos comparables, 90% de horas con precipitación). Temperatura: correlación ajustada +0,396. Viento: −0,037 ajustada. | Parcialmente apoyada. |
| **H5. Estacionalidad** | Septiembre: 166.576 viajes diarios promedio (máximo mensual normalizado); octubre: 5.150.717 viajes (máximo total mensual). Verano: 153.368 viajes diarios vs. invierno: 69.454 (+120,8%). | Apoyada. |
| **H6. Concentración por origen** | 2.378 IDs únicos tras consolidación. Top 10% de IDs: 39,67% de viajes; top 20%: 62,44%; 335 IDs (14,09%) concentran 50% de salidas. Gini: 0,599. | Apoyada. |

## Insights de negocio

1. **Planificación diferenciada por horario y tipo de día.** Las curvas horarias laborales y de fin de semana no tienen la misma forma. Una asignación uniforme basada en la media general omitiría picos relevantes.
2. **Diferencias entre segmentos.** Members y casuals muestran patrones de utilización distintos; esto justifica investigar políticas operativas y comerciales por segmento, sin inferir directamente motivos de viaje.
3. **Clima como señal predictiva.** La precipitación está asociada con menor uso incluso al comparar franjas temporales similares. Las correlaciones de temperatura y viento cambian al ajustar factores temporales; no deben interpretarse como efectos causales.
4. **Capacidad estacional.** La demanda diaria de verano es más del doble que la de invierno, pero septiembre y octubre lideran por promedio mensual. La planificación debe considerar meses específicos además de estaciones.
5. **Priorización espacial.** Las salidas están concentradas en ciertos IDs de origen; esto identifica candidatos para análisis de disponibilidad, pero **no** permite deducir déficits de bicicletas sin llegadas, inventario y capacidad.

## Decisiones metodológicas

- El procesamiento anual de viajes se realiza por *chunks* de 250.000 registros para limitar el uso de memoria.
- Se filtran viajes iniciados estrictamente en 2024; se excluyen duraciones no positivas, sin eliminar automáticamente viajes largos.
- El horario inexistente durante el salto de verano no se agrega como cero; la hora local repetida en noviembre se consolida respetando observaciones meteorológicas.
- Las comparaciones temporales H2/H3 utilizan perfiles horarios normalizados cuando corresponde, para distinguir volumen y forma de las curvas.
- En H4, el contraste de precipitación empareja mes, hora y tipo de día; temperatura y viento se evalúan también mediante anomalías respecto de promedios de esos grupos, sobre horas sin precipitación.
- La correlación de Pearson mide **asociación lineal**, no causalidad ni relaciones no lineales.
- Los rangos extremos de temperatura, nieve y viento cuentan con menos observaciones.
- En H5 se prioriza la media diaria por mes para evitar confundir demanda con distinta cantidad de días.
- El dataset de estaciones contiene 4.131 registros pero sólo 2.378 IDs únicos, 1.741 pares ID + nombre repetidos y 12 IDs asociados con múltiples nombres. H6 consolida **sumando por ID** sin descartar viajes.
- La concentración anual de viajes iniciados no equivale a ocupación, balance de bicicletas o demanda insatisfecha.

## Limitaciones

Estudio observacional de un único año; no demuestra causalidad ni patrones plurianuales. La meteorología proviene de un punto de referencia geográfico y no de cada estación. No hay información directa de propósito de viaje ni de disponibilidad o capacidad de cada estación. Los identificadores consolidados no garantizan equivalencia exacta con ubicaciones físicas únicas.

## Próxima etapa: Machine Learning

Definir horizonte de predicción, baseline temporal y separación cronológica; comparar modelos de regresión con MAE/RMSE; medir aporte incremental de variables climáticas frente a variables de calendario; garantizar que únicamente se usan valores disponibles al momento de generar la predicción (en particular, no incorporar clima futuro observado).

**Fuentes:** [Citi Bike System Data](https://citibikenyc.com/system-data) · [Open-Meteo Historical Weather API](https://open-meteo.com/en/docs/historical-weather-api).
