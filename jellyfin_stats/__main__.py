from jellyfin_stats.jellyfin.raw_data import JellyfinRawData
from jellyfin_stats.jellyfin.data import JellyfinData
from jellyfin_stats.process.processor import DataProcessor
from jellyfin_stats.stats.basic import BasicStats
from jellyfin_stats.stats.combinations import CombinationsStats

from pathlib import Path
import pkgutil
import argparse

class SplitArgs(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values.split(','))

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
    all_kinds = [name for _, name, _ in pkgutil.iter_modules(['jellyfin_stats/stats'])]
    default_kinds = all_kinds
    stats_parser.add_argument('-k', '--kinds', default=default_kinds, action=SplitArgs, help="The various kinds of statistics", choices=all_kinds)
    
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

        if 'basic' in args.kinds:
            stats = BasicStats(data)

            stats.print()

        if 'combinations' in args.kinds:

            stats_comb = CombinationsStats(data)

            stats_comb.print()
