import re
import pandas as pd
from jellyfin_stats.common import DEBUG
import logging

class RemuxTargets():
    def __init__(self, languages):
        self.data = None
        self.languages = languages
        if len(self.languages) == 0:
            self.languages = ['eng','jpn','ja','kor','ko','en','und']
        logging.info("Init Remux Targets: %s", self.__dict__)

    def apply(self, data):
        self.data = data
        self.data = self.apply_to_df(self.data)
        return self.data
        
    def is_remux_target(self, row):
        if row["Language"] not in self.languages and row["Type"] != "Video":
            itemid = row["Id"]
            streamtype = row["Type_stream"]
            all_streams = self.data.loc[itemid]
            
            same_type_streams = all_streams[all_streams["Type_stream"]==streamtype]
            
            if len(same_type_streams) < 2:
                # only one stream of this type, no remux
                return False
            return True
        else:
            return False
        
    def apply_to_df(self, df):
        df["Language"] = df["Language"].fillna('und')
        filtered = df.apply(self.is_remux_target, axis=1)
        print(filtered)
        return df[filtered]

