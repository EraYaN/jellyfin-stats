import logging
import pandas as pd

class BasicStats():
    def __init__(self, data_source):
        self.data = data_source

    def print(self):
        print(f"\nStatistics for data frame")
        print(self.data.df.describe())

        for col in self.data.df:
            print(f"\nStatistics for column {col}")
            print(self.data.df[col].value_counts())

        print(f"\nStatistics for streams data frame")
        print(self.data.df_streams.describe())

        for col in self.data.df_streams:
            print(f"\nStatistics for streams column {col}")
            print(self.data.df_streams[col].value_counts())
