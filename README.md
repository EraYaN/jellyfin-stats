# jellyfin-stats
A quick and dirty tool to get some media stats from your Jellyfin Server library and to run simple queries on that data.

## Install (conda)

Use this is you have a working install of conda or mamba.

```
conda env create -f environment.yml
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
python -m jellyfin_stats analyze -i ./data --kinds basic,combinations,specific
```

Search for specific files
```bash
python -m jellyfin_stats search -i ./data expr [expr ...]
```

And expressions need to conform to this form:
```
col = [A-Za-z_]
value = [^=]
data := base streams
op := == != < > <= >=
expr := data.col=value
```

To get all posiibilities use the basic stats from above.

Example: Find all videos with a height greater then or equal to 11440 pixels.

```bash
python -m jellyfin_stats search -i ./data streams.Type==Video streams.Height>=1440
```
This command support many of the output formats pandas supports (detected from the file extension), but you might need to install optional dependencies for some formats.

Currently: TXT, CSV, XLSX, HTML, MARKDOWN, SQL, JSON, PICKLE, PARQUET
