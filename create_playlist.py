from dataclasses import dataclass
import os
import requests
import sqlite3
import time
from typing import List

API_KEY = os.getenv("SPOTIFY_API_KEY")
PLAYLIST_ID = os.getenv("SPOTIFY_PLAYLIST_ID")

API_URL = "https://api.spotify.com/v1"
SEARCH_ENDPOINT = API_URL + "/search"

def get_playlist_tracks_endpoint(playlist_id):
    return API_URL + "/playlists/" + playlist_id + "/tracks"

@dataclass
class Track:
    title: str
    artist: str

def get_spotify_id(track, api_key) -> str:
    """ Returns spotify URI of the first matching track """

    headers = {"Authorization": "Bearer " + api_key}
    def perform_query(query): 
        return requests.get(
            SEARCH_ENDPOINT, params={"q": query, "type": "track"}, headers=headers
        ).json()["tracks"]["items"]

    artist = track.artist or ""
    query = track.title + " " + artist

    items = perform_query(query)

    if len(items) == 0 and "(" in track.title:
        query = track.title[0:track.title.index("(")] + " " + artist
        items = perform_query(query)

    if len(items) == 0:
        time.sleep(5)
        items = perform_query(query)

    return items[0]["uri"]

def add_tracks_to_playlist(playlist_id, track_uris, api_key):
    if len(track_uris) > 100:
         raise "too many track_uris passed to add_tracks_to_playlist (max 100 can be passed)"

    headers = {"Authorization": "Bearer " + api_key}
    endpoint = get_playlist_tracks_endpoint(playlist_id)

    data = {"uris": track_uris}
    res = requests.post(endpoint, json=data, headers=headers)

def get_top_tracks(db_conn) -> List[Track]:
    return [
        Track(row[0], row[1]) for row in conn.execute('''
            SELECT title, artist, COUNT(*) FROM disc GROUP BY artist, title ORDER BY 3 DESC LIMIT 100;
        ''')
    ]

conn = sqlite3.connect('data.sqlite')
tracks = get_top_tracks(conn)

track_ids = [get_spotify_id(track, API_KEY) for track in tracks]
add_tracks_to_playlist(SPOTIFY_PLAYLIST_ID, track_ids, API_KEY)
