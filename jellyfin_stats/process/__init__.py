from pandas.api.types import CategoricalDtype
from jellyfin_stats.enums import *

base_item_kind = CategoricalDtype(categories=BaseItemKind, ordered=False)
video_type = CategoricalDtype(categories=VideoType, ordered=False)
iso_type = CategoricalDtype(categories=IsoType, ordered=False)

media_stream_type = CategoricalDtype(categories=MediaStreamType, ordered=True)