import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import statsmodels.api as sm
from faraway.datasets import galapagos
from scipy import stats
from statsmodels.stats.diagnostic import het_breuschpagan


class GalapagosBiogeographyPipeline:
    """An analytical pipeline for testing Island Biogeography theory using

    OLS, non-linear log-log transformations, and multivariate diagnostics.
    """

    def __init__(self):
        self.raw_df = galapagos.load()
        self.df = self.raw_df.copy()
        self.models = {}

    def preprocess(self) -> "GalapagosBiogeographyPipeline":
        """Log-transforms variables to model non-linear Arrhenius relationships

        and handles structural scale differences.
        """
        # Small offset to handle zero/near-zero values safely if applicable
        self.df["log_Area"] = np.log10(self.df["Area"])
        self.df["log_Species"] = np.log10(self.df["Species"])
        return self

    def fit_models(self) -> "GalapagosBiogeographyPipeline":
        """Fits Linear, Log-Log (Power Law), and Multivariate regression

        models.
        """
        # 1. Base Untransformed OLS
        X_base = sm.add_constant(self.df["Area"])
        self.models["Linear_OLS"] = sm.OLS(self.df["Species"], X_base).fit()

        # 2. Log-Log OLS (Arrhenius Species-Area Relationship)
        X_log = sm.add_constant(self.df["log_Area"])
        self.models["LogLog_PowerLaw"] = sm.OLS(
            self.df["log_Species"], X_log
        ).fit()

        # 3. Multivariate OLS (Controlling for Elevation & Distance)
        X_multi = sm.add_constant(
            self.df[["log_Area", "Elevation", "Nearest", "Scruz"]]
        )
        self.models["Multivariate_Log"] = sm.OLS(
            self.df["log_Species"], X_multi
        ).fit()

        return self

    def evaluate_models(self) -> pd.DataFrame:
        """Runs residual diagnostics including Shapiro-Wilk (normality) and

        Breusch-Pagan (homoscedasticity) tests across models.
        """
        metrics = []
        for name, model in self.models.items():
            bp_test = het_breuschpagan(model.resid, model.model.exog)
            shapiro_test = stats.shapiro(model.resid)

            metrics.append({
                "Model": name,
                "Adj_R2": round(model.rsquared_adj, 4),
                "AIC": round(model.aic, 2),
                "BIC": round(model.bic, 2),
                "Normality_p": round(shapiro_test.pvalue, 4),
                "Homoscedasticity_p": round(bp_test[1], 4),
            })
        return pd.DataFrame(metrics)

    def plot_diagnostics(self) -> None:
        """Generates publication-quality diagnostic visualizations."""
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        sns.set_theme(style="whitegrid")

        # Plot 1: Log-Log Species Area Curve
        sns.regplot(
            x="log_Area",
            y="log_Species",
            data=self.df,
            ax=axes[0],
            color="darkblue",
            line_kws={"color": "crimson", "linewidth": 2},
        )
        axes[0].set_title(
            "Log-Log Species-Area Model (Power Law)", fontsize=12
        )
        axes[0].set_xlabel("log10(Area)")
        axes[0].set_ylabel("log10(Species)")

        # Plot 2: QQ Plot of Residuals for Log-Log Model
        sm.qqplot(
            self.models["LogLog_PowerLaw"].resid,
            line="s",
            ax=axes[1],
            color="darkblue",
        )
        axes[1].set_title(
            "Q-Q Plot: Log-Log Model Residuals", fontsize=12
        )

        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    pipeline = GalapagosBiogeographyPipeline()
    metrics_df = pipeline.preprocess().fit_models().evaluate_models()

    print("MODEL PERFORMANCE & DIAGNOSTICS")
    print(metrics_df.to_string(index=False))

    pipeline.plot_diagnostics()