import logging
import pandas as pd
from pathlib import Path

class JellyfinData():
    def __init__(self):
        self.columns = ['Id', 'Name', 'Container', 'Type', 'RunTimeTicks', 'VideoType','IsoType','LocationType','HasSubtitles','OfficialRating','ProductionYear']
        self.columns_streams =  ['AspectRatio', 'AverageFrameRate', 'BitDepth',
                            'BitRate','Codec','CodecTimeBase',
                            'DisplayTitle', 'Height', 'Index',
                            'IsAVC', 'IsDefault', 'IsExternal',
                            'IsForced', 'IsInterlaced', 'IsTextSubtitleStream',
                            'Language', 'Level', 'NalLengthSize',
                            'PixelFormat', 'Profile', 'RealFrameRate',
                            'RefFrames', 'SupportsExternalStream', 'TimeBase',
                            'Type', 'VideoRange', 'Width']


        self.index_col = 'Id'
        self.index_stream_col = 'Index'
        self.df = None

        self.df_streams = None

    def ingest(self, raw_data_source):
        for itemtype in raw_data_source.all_items:
            logging.info("Ingesting data for type %s", itemtype)
            processed = map(lambda x: {k:v for k,v in x.items() if k in self.columns}, raw_data_source.all_items[itemtype])

            index = pd.Index([x[self.index_col] for x in raw_data_source.all_items[itemtype]], name="IdIdx")
            if self.df is None:
                self.df = pd.DataFrame(processed, columns=self.columns, index=index)
            else:
                self.df = self.df.append(pd.DataFrame(processed, columns=self.columns, index=index),sort=True)

            flat_streamlist = [{**item, self.index_col:sublist[self.index_col]} for sublist in raw_data_source.all_items[itemtype] if 'MediaStreams' in sublist for item in sublist['MediaStreams']]
            index_streams_id = [x[self.index_col] for x in flat_streamlist]
            index_streams_streams = [x[self.index_stream_col] for x in flat_streamlist]

            index_streams = pd.MultiIndex.from_arrays([index_streams_id,index_streams_streams], names=('IdIdx', 'IndexIdx'))
            processed_streams = map(lambda x: {k:v for k,v in x.items() if k in self.columns_streams}, flat_streamlist)

            if self.df_streams is None:
                self.df_streams = pd.DataFrame(processed_streams, columns=self.columns_streams, index=index_streams)
            else:
                self.df_streams = self.df_streams.append(pd.DataFrame(processed_streams, columns=self.columns_streams, index=index_streams), sort=True)
                
        self.df = self.df.convert_dtypes()
        self.df_streams = self.df_streams.convert_dtypes()

    def dump(self, outputdir:Path):
        outputdir.mkdir(parents=True,exist_ok=True)
        self.df.to_pickle(outputdir / "base.pkl")
        self.df_streams.to_pickle(outputdir / "streams.pkl")

    @classmethod
    def load(cls, inputdir:Path):
        obj = cls()
        obj.df = pd.read_pickle(inputdir / "base.pkl")
        obj.df_streams = pd.read_pickle(inputdir / "streams.pkl")
        return obj
