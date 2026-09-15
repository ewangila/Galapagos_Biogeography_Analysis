# Galapagos Island Biogeography Analysis

Statistical analysis of the classic Galapagos plant species dataset to test the Theory of Island Biogeography. This project evaluates the species–area relationship using ordinary least squares (OLS), log-log power-law (Arrhenius) models, and multivariate regression, with full residual diagnostics.

---

## Research questions

1. **Does island area predict species richness?**  
2. **Does a log-log (power-law) transformation better capture the non-linear relationship?**  
3. **Do additional geographic factors (elevation, isolation) improve predictive performance?**

---

## Dataset

| Property | Detail |
|----------|--------|
| **Source** | `faraway.datasets.galapagos` (classic botanical survey of the Galapagos Islands) |
| **Observations** | 30 islands |
| **Key variables** | `Species`, `Area`, `Elevation`, `Nearest`, `Scruz`, `Adjacent` |

The dataset records the number of plant species and physical characteristics of each island and is widely used to illustrate the species–area relationship in ecology.

---

## Methods

### Models fitted

| Model | Specification | Purpose |
|-------|---------------|---------|
| **Linear OLS** | `Species ~ Area` | Baseline linear relationship |
| **Log-Log Power Law** | `log₁₀(Species) ~ log₁₀(Area)` | Arrhenius species–area relationship |
| **Multivariate Log** | `log₁₀(Species) ~ log₁₀(Area) + Elevation + Nearest + Scruz` | Control for topography and isolation |

### Diagnostics

- Adjusted R², AIC, BIC  
- Shapiro–Wilk test (residual normality)  
- Breusch–Pagan test (homoscedasticity)  
- Diagnostic plots: log-log species–area scatter with regression line + Q–Q plot of residuals

---

## Key findings (high level)

| Model | Adj. R² | Notes |
|-------|---------|-------|
| Linear OLS | ~0.36 | Poor fit; residuals violate normality |
| Log-Log Power Law | ~0.75 | Strong improvement; supports power-law relationship |
| Multivariate Log | ~0.76 | Modest further gain after controlling for elevation & isolation |

The log-log transformation substantially improves model fit and residual behavior, consistent with classic island biogeography theory. Adding elevation and isolation yields only a small additional improvement on this dataset.

*(Exact coefficients, p-values, and diagnostic statistics are available by running the notebook or script.)*

---

## Project structure

```text
Galapagos_Biogeography_Analysis/
├── Galapagos_Island_Biogeography.ipynb   # Full interactive analysis notebook
├── galapagos_biogeography_analysis.py    # Standalone Python pipeline
├── requirements.txt                      # Python dependencies
├── LICENSE                               # MIT
└── README.md
```
## Setup & usage

### Requirements

- Python 3.8+
- Jupyter (recommended for the notebook)

### Install

```bash
git clone https://github.com/ewangila/Galapagos_Biogeography_Analysis.git
cd Galapagos_Biogeography_Analysis
pip install -r requirements.txt
```
### Run the analysis

Option 1 – Jupyter Notebook (recommended)

```Bash
Jupyter notebook Galapagos_Island_Biogeography.ipynb
```
Option 2 – Python script

```Bash
python galapagos_biogeography_analysis.py
```

The script will:

1. Load the Galapagos dataset  
2. Fit the three regression models  
3. Print performance metrics and residual diagnostics  
4. Display the log-log species–area plot and Q–Q plot

---

## Technologies used

- **Python**
- **pandas** & **numpy** – data handling
- **statsmodels** – OLS regression & diagnostics
- **scipy** – Shapiro–Wilk test
- **matplotlib** & **seaborn** – visualization
- **faraway** – Galapagos dataset

---

## Limitations

- Relatively small sample (30 islands)  
- Classic observational data — no experimental manipulation of area or isolation  
- Focus is on methodological demonstration rather than new ecological discovery  
- Multicollinearity among geographic predictors is not exhaustively explored

---

## Suggested next steps

- Explore interaction terms (e.g., Area × Elevation)  
- Apply robust or Bayesian regression approaches  
- Compare results with other classic biogeography datasets  
- Add spatial residual analysis or Moran’s I  
- Extend the pipeline to additional taxa or island systems

---

## Author

**Eugin Wangila**  
[GitHub](https://github.com/ewangila)

## License

This project is licensed under the [MIT License](LICENSE).
