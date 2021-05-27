import pandas as pd

import configuration as config


class DataSpliter:
    def __init__(self, df: pd.DataFrame, split_ratio: float):
        self.df = self._assign_tiers(df)
        self.split_ratio = split_ratio

    def _assign_tiers(self, df: pd.DataFrame) -> pd.DataFrame:
        if config.TIER == 'passive':
            lower = df[config.TARGET].quantile(0.3)
            return df.loc[df[config.TARGET] >= lower, :].copy()
        elif config.TIER == 'aggressive':
            upper = df[config.TARGET].quantile(0.7)
            return df.loc[df[config.TARGET] < upper, :].copy()
        else:
            lower = df[config.TARGET].quantile(0.05)
            upper = df[config.TARGET].quantile(0.95)
            return df.loc[(df[config.TARGET] >= lower) & (df[config.TARGET] < upper), :]

    def split(self):
        split_idx = int(self.df.shape[0] * self.split_ratio)
        split_date = self.df.index[split_idx]

        self.df_train = self.df.loc[self.df.index <= split_date, :].copy()
        self.df_test = self.df.loc[self.df.index > split_date, :].copy()

        return self.df_train, self.df_test