# Citi Bike Demand Intelligence

**Understanding when, under which conditions, and where New York City's bike-sharing demand concentrates.**

An end-to-end data analytics project built from **44,302,480 Citi Bike rides started in 2024**, integrating trip history with historical weather data. The goal is to turn large-scale mobility data into interpretable findings for operations and mobility planning, with hourly demand forecasting as a future extension.

> **Project status (October 2026):** Data acquisition, processing and the completed six-hypothesis EDA notebook are published. Results and methodology are summarized here and in [the Spanish EDA report](docs/EDA_FINDINGS_ES.md).

## At a glance

| Item | Scope |
|---|---|
| Geography | New York City, USA |
| Period | January 1–December 31, 2024 |
| Trip starts analyzed | **44,302,480** |
| Hourly observations | **8,783** distinct local-hour labels (DST-aware) |
| Weather | Open-Meteo historical hourly conditions |
| Tools | Python, pandas, NumPy, Matplotlib, Seaborn, requests, Jupyter |
| Focus | Exploratory analysis, data quality, reproducibility, operational insights |

## Research question

> Which temporal, weather, and user-behavior factors are associated with Citi Bike demand, and how can historical patterns inform operational planning?

## Key findings

| Hypothesis | Evidence from 2024 | Assessment |
|---|---|---|
| **H1 · Time of day** | Mean demand peaks at **17:00 (11,147 starts/hour)**, with a smaller morning peak at **08:00 (7,468)**. These patterns are consistent with, but do not prove, commuting. | Partially supported |
| **H2 · Weekday vs. weekend** | Workdays show pronounced 08:00 and 17:00 peaks; weekends have a broader midday/afternoon profile. | Supported |
| **H3 · Member vs. casual** | Members account for **80.7%** of starts. Average daily member starts are **21.18% lower** on weekends, while casual starts are **39.14% higher**. | Supported |
| **H4 · Weather** | Precipitation hours have **32.46% lower** mean demand after comparison within month × hour × weekend groups. Adjusted correlations: temperature **+0.396**, wind **−0.037**. | Partially supported |
| **H5 · Seasonality** | Summer mean daily starts are **120.8% higher** than winter; **September** has the highest mean daily demand and **October** the highest monthly total. | Supported |
| **H6 · Origin-station concentration** | The busiest **20% of station IDs account for 62.44%** of identified starts; the Lorenz-based **Gini coefficient is 0.599**. | Supported |

**Interpretation:** Demand varies strongly by calendar patterns and user segment, is negatively associated with precipitation, and is unevenly distributed across origin-station identifiers. These are **observational associations**, not causal estimates or validated operational interventions.

See [EDA findings and methodological decisions (Spanish)](docs/EDA_FINDINGS_ES.md) for more detail, including limitations and the interpretation of adjusted comparisons.

## Repository structure

```text
citi-bike-demand-intelligence/
├── data/
│   ├── raw/                  # Downloaded raw trips; ignored by Git
│   └── processed/            # Versioned analysis-ready CSVs
├── notebooks/
│   ├── 01_data_acquisition_preparation.ipynb
│   └── 02_eda_insights.ipynb # Completed EDA, visualizations and conclusions
├── docs/
│   └── EDA_FINDINGS_ES.md
├── requirements.txt
└── README.md
```

### Processed datasets

| File | Grain / purpose |
|---|---|
| `data/processed/citibike_analysis_hourly_2024.csv` | One row per distinct local-hour label; rides + weather + calendar features (**8,783 rows**). |
| `data/processed/citibike_segmented_hourly_2024.csv` | Hour × member/casual × bike type (**35,113 rows**). |
| `data/processed/citibike_stations_2024.csv` | Origin-station aggregates (**4,131 source rows**, requiring consolidation to **2,378 unique station IDs** for H6). |

Trips without a valid origin station (**29,834**) are excluded **only** from the origin-station analysis. They remain in the hourly and segmented totals.

## Reproducibility

Clone the repository and install the pinned-range dependencies:

```bash
git clone https://github.com/benitezlucio/citi-bike-demand-intelligence.git
cd citi-bike-demand-intelligence
python -m pip install -r requirements.txt
jupyter lab
```

**Quick start:** Open [`notebooks/02_eda_insights.ipynb`](notebooks/02_eda_insights.ipynb) and run it against the versioned CSVs in `data/processed/`. It does not need to download the raw trip history again.

**Full reproduction:** Run `notebooks/01_data_acquisition_preparation.ipynb` to retrieve and prepare the raw Citi Bike and Open-Meteo data, then run notebook 02. This pipeline processes trip files in chunks rather than loading tens of millions of raw records into memory at once. Internet access is required for acquisition.

The notebooks use repository-relative paths and are designed for local Python/Jupyter and Google Colab.

### Data-quality and time-handling decisions

- Trip records are limited to starts during **2024**; non-positive trip durations are removed. Long durations are not discarded arbitrarily when counting trip starts.
- Raw trips are processed in **250,000-row chunks** to limit memory use.
- The pipeline accounts for **New York daylight saving time (DST)**. The nonexistent spring-forward hour is not invented as a zero-demand hour. The repeated fall-back local hour is represented by one local-hour label, with weather observations consolidated appropriately.
- Final hourly trip and weather tables align at **8,783 local timestamps**, with no missing merged values.
- Origin-station source records are not one-to-one with station IDs. H6 consolidates counts by `start_station_id`; some IDs have multiple recorded names. Results describe **station identifiers**, which are not guaranteed to map one-to-one to distinct physical locations.

## Sources

- [Citi Bike System Data — Trip History](https://citibikenyc.com/system-data)
- [Open-Meteo Historical Weather API](https://open-meteo.com/en/docs/historical-weather-api), with a New York City reference location and `America/New_York` timezone.

## Limitations

This study covers **one calendar year**, so recurring multi-year seasonality is not established. Recorded starts are not the same as latent demand or unmet demand. The dataset does not directly provide trip purpose, station inventory, dock capacity, or arrival–departure balance. Weather is measured at a city-level reference point, and weather associations may retain unmeasured confounding. Extreme heat and snow conditions have limited observations.

## Next steps

1. Use the published EDA notebook and its visualizations as the basis for the academic presentation and portfolio.
2. Define an hourly forecasting horizon and information-availability assumptions.
3. Evaluate time-aware baselines and regression models with chronological validation (MAE / RMSE).
4. Test whether weather features improve on calendar-only baselines, without leaking future observed weather into predictions.

---

**Author:** [Lucio Benítez](https://github.com/benitezlucio) · [LinkedIn](https://www.linkedin.com/in/lucio-benitez-data/)

*The notebooks and detailed academic write-up are written in Spanish; this README provides an English overview for an international audience.*
