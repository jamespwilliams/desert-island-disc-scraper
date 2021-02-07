# desert-island-disc-scraper

See https://morph.io/jamespwilliams/desert-island-disc-scraper, which runs
the scraper every day.

## Usage

Python 3 is needed.

```shell
git clone https://github.com/jamespwilliams/desert-island-disc-scraper.git
cd desert-island-disc-scraper
```

If using `nix`:

```shell
nix-shell

python scraper.py
```

Otherwise:

```shell
. venv/bin/activate
pip install -r requirements.txt

python scraper.py
```

## Creating the playlist

```shell
export SPOTIFY_API_KEY="insert key"
export SPOTIFY_PLAYLIST_ID="insert playlist id"

python create_playlist.py
```
