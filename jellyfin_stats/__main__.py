from jellyfin_stats.jellyfin.raw_data import JellyfinRawData
from jellyfin_stats.jellyfin.data import JellyfinData
from jellyfin_stats.process.processor import DataProcessor
from jellyfin_stats.stats.basic import BasicStats
from jellyfin_stats.stats.combinations import CombinationsStats
from jellyfin_stats.stats.specific import SpecificStats
from jellyfin_stats.process.search import SearchExpr
from jellyfin_stats.common import DEBUG

from pathlib import Path
import pandas as pd
import pkgutil
import argparse

class SplitArgs(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values.split(','))

class Expr(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, list(map(lambda v:SearchExpr(v),values)))

if __name__ == "__main__":
 

    parser = argparse.ArgumentParser(description='Make some pretty stats about your Jellyfin library.')
    

    subparsers = parser.add_subparsers(help='sub-command help', dest="command")

    gather_data_parser = subparsers.add_parser("gatherdata", description="Gather the data from the Jellyfin server")
    gather_data_parser.add_argument('-o', '--output-dir', default=Path("."), metavar="DIR", type=Path, help="The output directory.")
    gather_data_parser.add_argument('-s','--server', type=str,
                        help='Your jellyfin server URL', default="http://localhost:8096")
    gather_data_parser.add_argument('-k','--apikey', metavar="APIKEY", type=str, required=True,
                        help='A working API key.')

    stats_parser = subparsers.add_parser("analyze", description="Analyzes and outputs all stats from saved data.")
    stats_parser.add_argument('-i', '--input-dir', default=Path("."), metavar="DIR", type=Path, help="The input directory.")
    all_kinds = [name for _, name, _ in pkgutil.iter_modules(['jellyfin_stats/stats'])] + ['none']
    default_kinds = all_kinds
    stats_parser.add_argument('-k', '--kinds', default=default_kinds, action=SplitArgs, help=f"The various kinds of statistics ({', '.join(all_kinds)})")

    search_parser = subparsers.add_parser("search", description="Searches processed data based on stream or item columns.")
    search_parser.add_argument('-i', '--input-dir', default=Path("."), metavar="DIR", type=Path, help="The input directory.")
    search_parser.add_argument('expr', nargs='+', metavar="EXPR", action=Expr, help="Multiple (AND) base.<col>=value or streams.<col>=value")
    
    args = parser.parse_args()

    if args.command == 'gatherdata':
        raw_data = JellyfinRawData(api_key=args.apikey, hostname=args.server)

        raw_data.gather()

        data = JellyfinData()

        data.ingest(raw_data_source=raw_data)

        data.dump(args.output_dir)

    elif args.command == 'analyze':
        data = JellyfinData.load(args.input_dir)

        data = DataProcessor(data)

        data.process()

        if DEBUG:
            print("The DTypes of the two data frames")
            print("base", data.df.dtypes)

            print("streams",data.df_streams.dtypes)

        if 'basic' in args.kinds:
            stats = BasicStats(data)

            stats.print()

        if 'combinations' in args.kinds:

            stats_comb = CombinationsStats(data)

            stats_comb.print()

        if 'specific' in args.kinds:

            stats_specific = SpecificStats(data)

            stats_specific.print()
    elif args.command == 'search':
        data = JellyfinData.load(args.input_dir)

        data = DataProcessor(data)

        data.process()

        for expr in args.expr:
            data = expr.apply(data)
            if DEBUG:
                print("Result after applying expression",expr)
                print("Left DF:\n",data.df)
                print("Right DF:\n",data.df_streams)
            

        #df_streams_grouped = data.df_streams.groupby(level="Id")

        if DEBUG:
            print("Left DF:\n",data.df)
            print("Right DF:\n",data.df_streams)

        merged = pd.merge(
            data.df,
            data.df_streams,
            how="inner",
            on="IdIdx",
            suffixes = ('', '_stream'),
            validate="one_to_many")

        print(merged)

