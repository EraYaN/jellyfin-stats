from jellyfin_stats.process import *
import pandas as pd

class DataProcessor():
    def __init__(self, data_source):
        self.df = data_source.df

        self.df_streams = data_source.df_streams

    def process(self):
        self.df["Type"] = self.df["Type"].astype(base_item_kind)
        self.df["VideoType"] = self.df["VideoType"].astype(video_type)
        self.df["IsoType"] = self.df["IsoType"].astype(iso_type)
        self.df["RunTime"] = pd.to_timedelta(self.df["RunTimeTicks"].divide(10e6),unit="S")

        self.df_streams["FrameRate"] = self.df_streams["RealFrameRate"].round(2)
        self.df_streams["Type"] = self.df_streams["Type"].astype(media_stream_type)
