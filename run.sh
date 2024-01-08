#!/bin/bash
# This script is used to run the program

python3 -m jellyfin_stats gatherdata -s https://<server> -o ./data -k <key>

#python3 -m jellyfin_stats analyze -i ./data -k combinations

#python3 -m jellyfin_stats search -i ./data -o ./data/found.txt streams.Language!='eng' streams.Type=='Audio'