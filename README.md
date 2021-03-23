# jellyfin-stats
A quick and dirty tool to get some media stats from your Jellyfin Server library

## Install (conda)

Use this is you have a working install of conda or mamba.

```
conda env create -f envrionment.yml
```

## Install (mkvirtualenv)

```
mkvirtualenv -r requirements.txt jellyfin-stats
```

## Install (venv+pip)

```
python -m venv ./jellyfin-stats
source ./jellyfin-stats/bin/activate
pip install -r requirements.txt
```

## Usage

Gather the data (using an API key)
```bash
python -m jellyfin_stats gatherdata -s http://localhost:8096 -k d50b9bab55c04804b587d372beb0259f -o ./data
```
Process and print the stats
```bash
python -m jellyfin_stats analyze -i ./data
```
