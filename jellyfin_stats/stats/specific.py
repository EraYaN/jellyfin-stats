import logging
import pandas as pd

class SpecificStats():
    def __init__(self, data_source):
        self.data = data_source

    def print(self):

        is_video_stream = self.data.df_streams['Type']=="Video"
        is_audio_stream = self.data.df_streams['Type']=="Audio"

        # Video resulitions
        print(f"\nStatistics about video resolution")
        print(self.data.df_streams[is_video_stream]['Height'].value_counts())