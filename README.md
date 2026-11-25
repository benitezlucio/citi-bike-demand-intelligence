# Citi Bike Demand Intelligence

**From 44.3 million New York City bike-share trips to interpretable demand forecasts.**

End-to-end analytics and Machine Learning portfolio project covering **44,302,480 ride starts in 2024**, historical Citi Bike activity and weather data. It combines a large-scale processing pipeline, statistical EDA and a time-aware experiment predicting total hourly trip starts.

> **Status · November 2026:** Stages **01 (data acquisition)** and **02 (EDA)** are complete. Stage **03 (hourly demand forecasting)** is published for academic review. The cleaned notebook is structurally validated; a fresh end-to-end execution of that revised notebook with the real datasets and API is still required before submission. Results below come from the earlier executed experiment, not a newly verified run.

## Project navigation

| Stage | Deliverable | Purpose |
|---|---|---|
| 01 — Data acquisition | [Preparation notebook](notebooks/01_data_acquisition_preparation.ipynb) | Chunked ingestion, quality checks, NYC time handling, historical observed weather |
| 02 — Exploratory data analysis | [EDA notebook](notebooks/02_eda_insights.ipynb) · [Findings (ES)](docs/EDA_FINDINGS_ES.md) | Six hypotheses, temporal/weather/user/station patterns |
| 03 — Machine Learning | [Forecasting notebook](notebooks/03_ml_hourly_demand_forecasting.ipynb) · [ML methodology (ES)](docs/ML_FORECASTING_ES.md) | Hourly demand prediction, baselines, models, weather ablation, time-aware evaluation |
| Academic materials | [Coderhouse submissions](entregas/coderhouse/README.md) | Separate earlier EDA and new ML submission |

### Stage 03 — problem and business relevance

**Question:** Can we predict the number of trips starting in a target hour **one hour before that hour begins**? Does adding archived weather forecasts improve performance beyond calendar and historical demand?

- **Prediction target:** hourly trip starts (`ride_count`), supervised regression, system-level aggregate.
- **Information:** hour/day/month encodings, known historical trip counts, and optionally **nominal 24-hour-ahead GFS forecasts** for temperature, precipitation, and wind.
- **Comparison:** weekly/previous-hour baselines, Ridge Regression, Random Forest and HistGradientBoostingRegressor.
- **Evaluation:** MAE (primary), RMSE, four chronological CV folds, `RandomizedSearchCV` on training only and November–December holdout.
- **Interpretation:** permutation importance and error analysis by forecast rain, peak periods and type of day.

### Recorded results (original experiment; re-execution pending)

| Model | Nov–Dec 2024 MAE ↓ | Nov–Dec RMSE ↓ |
|---|---:|---:|
| Gradient Boosting **without** forecast weather | **609.17** | 971.88 |
| Gradient Boosting **with** forecast weather | 612.59 | **943.70** |
| Weekly seasonal baseline | 1,378.97 | 2,082.11 |

The weather variant showed a lower rain-hour MAE (**658.27 vs 1,002.35**, across 204 hours with forecast precipitation) but **not** a lower overall MAE. We do not claim the models are live-deployable or that prediction creates proven operational savings.

**Important caveats:** the analysis simulates hourly demand counts being available promptly, and `previous_day1` indicates nominal forecast lead time rather than independently verified publication timestamps. Forecast coverage begins on **2024-01-19**; local DST produces a repeated hour that is explicitly excluded in Stage 03. These are documented in the [ML methodology](docs/ML_FORECASTING_ES.md).

## Data and reproducibility

```bash
git clone https://github.com/benitezlucio/citi-bike-demand-intelligence.git
cd citi-bike-demand-intelligence
python -m venv .venv
# Activate the venv for your shell, then:
python -m pip install -r requirements.txt
jupyter lab
```

Open `notebooks/03_ml_hourly_demand_forecasting.ipynb` and choose **Restart & Run All**. Run from the repository root or `notebooks/` so the project can find `data/processed/citibike_analysis_hourly_2024.csv`.

The notebook downloads Open-Meteo **Previous Runs GFS previous_day1** forecast data once (internet required, subject to API availability) and caches a local file named `data/processed/citibike_gfs_previous_day1_2024.csv`. That cache is deliberately **gitignored**. A new run may return different data if the provider updates its historical archive.

For Coderhouse, use the **separate academic copy** at [`entregas/coderhouse/Citi_Bike_Coderhouse_Entrega_ML.ipynb`](entregas/coderhouse/Citi_Bike_Coderhouse_Entrega_ML.ipynb). If submitting a standalone file, ensure the processed CSV is accessible or run the notebook in Colab with its repository bootstrap and internet access.

**Before submitting:** execute the notebook end-to-end with real data, confirm metrics, inspect plots and errors, and save the executed output. The current committed notebook includes embedded explanatory diagrams and recorded reference results but has empty execution outputs.

### Repository structure

```text
data/
  raw/                  # ignored large downloads
  processed/            # versioned analysis-ready Citi Bike CSVs
notebooks/
  01_data_acquisition_preparation.ipynb
  02_eda_insights.ipynb
  03_ml_hourly_demand_forecasting.ipynb
docs/
  EDA_FINDINGS_ES.md
  ML_FORECASTING_ES.md
  CODERHOUSE_ML_CHECKLIST_ES.md
entregas/coderhouse/
  Citi_Bike_Coderhouse_Entrega_Academica.ipynb  # prior EDA submission
  Citi_Bike_Presentacion_Ejecutiva_Coderhouse.pptx # prior EDA slides
  Citi_Bike_Coderhouse_Entrega_ML.ipynb          # current ML submission
scripts/
  check_ml_notebooks.py
requirements.txt
README.md
```

## Data integrity and limitations

The two original notebooks and their outputs remain unchanged. The 2024 aggregation has **8,783 local-hour labels**, from **44,302,480 trip starts**. The spring-forward 02:00 hour does not exist; the repeated November local 01:00 was consolidated for EDA and excluded in ML. The ML experiment uses **8,335 usable observations** after forecast coverage, DST and historical-lag filters.

Observed weather supports the EDA; **future observed weather is not used as a predictive feature**. Station totals cannot identify unmet demand without arrivals, dock capacity and bike inventory. One year alone cannot establish multi-year generalization.

## Sources and use

- [Citi Bike System Data](https://citibikenyc.com/system-data)
- [Open-Meteo Historical Weather](https://open-meteo.com/en/docs/historical-weather-api)
- [Open-Meteo Previous Runs](https://open-meteo.com/en/docs/previous-runs-api)
- [scikit-learn TimeSeriesSplit](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html)

Respect the providers' licensing and attribution rules before redistributing or deploying datasets or products. This portfolio project is **not affiliated with Citi Bike**.

---

Author: [Lucio Benítez](https://github.com/benitezlucio) · [LinkedIn](https://www.linkedin.com/in/lucio-benitez-data/)
