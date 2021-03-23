# jellyfin-stats
A quick and dirty tool to get some codec info from your Jellyfin Server library

## Usage

Gather the data (using an API key)
```bash
python -m jellyfin_stats gatherdata -s http://localhost:8096 -k d50b9bab55c04804b587d372beb0259f -o ./data
```
Process and print the stats
```bash
python -m jellyfin_stats analyze -i ./data
```
