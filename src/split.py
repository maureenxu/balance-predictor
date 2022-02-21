from typing import Optional
import pandas as pd

from src.configuration import Config

# pylint: disable=too-few-public-methods
class DataSplitter:
    def __init__(self, config: Config, df: pd.DataFrame):
        self.config = config
        self.df = self._assign_tiers(df)

        self.df_train: Optional[pd.DataFrame] = None
        self.df_test: Optional[pd.DataFrame] = None

    def _assign_tiers(self, df: pd.DataFrame) -> pd.DataFrame:
        if self.config.TIER == "passive":
            lower = df[self.config.TARGET].quantile(0.3)
            return df.loc[df[self.config.TARGET] >= lower, :].copy()

        if self.config.TIER == "aggressive":
            upper = df[self.config.TARGET].quantile(0.7)
            return df.loc[df[self.config.TARGET] < upper, :].copy()

        lower = df[self.config.TARGET].quantile(0.05)
        upper = df[self.config.TARGET].quantile(0.95)
        return df.loc[
            (df[self.config.TARGET] >= lower) & (df[self.config.TARGET] < upper), :
        ]

    def split(self, split_ratio: float):
        split_idx = int(self.df.shape[0] * split_ratio)
        split_date = self.df.index[split_idx]

        self.df_train = self.df.loc[self.df.index <= split_date, :].copy()
        self.df_test = self.df.loc[self.df.index > split_date, :].copy()

        return self.df_train, self.df_test
