import logging
import pandas as pd

class CombinationsStats():
    def __init__(self, data_source):

        self.combinations = [
            ['Container', 'Type']
        ]

        self.combinations_streams = [
            ['Type', 'Height'],
            ['Type', 'Codec', 'Profile']
        ]
        
        self.data = data_source

    def print(self):
        for comb in self.combinations:
            print(f"\nStatistics for combination of columns {comb}")
            print(self.data.df.value_counts(comb))

        for comb in self.combinations_streams:
            print(f"\nStatistics for combination of streams columns {comb}")
            print(self.data.df_streams.value_counts(comb))