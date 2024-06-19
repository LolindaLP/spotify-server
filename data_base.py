from datetime import datetime
import requests
import sqlite3
import pytz
import os
import base64
import dotenv

dotenv.load_dotenv()


def get_token():
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    r = requests.post(url, headers=headers, data=data)
    access_token = r.json()["access_token"]
    return access_token


def update_database():
    access_token = get_token()
    playlist_id = "37i9dQZEVXbMDoHDwVN2tF"
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        playlist_data = response.json()
        tracks = playlist_data.get('items', [])
        conn = sqlite3.connect('tracksdb/tracks.db')
        c = conn.cursor()
        for track in tracks:
            track_name = track['track']['name']
            track_artists = ', '.join([artist['name'] for artist in track['track']['artists']])
            track_image = track['track']['album']['images'][0]['url'] if track['track']['album']['images'] else None
            track_popularity = track['track']['popularity']
            track_date = datetime.now(pytz.utc).strftime('%Y-%m-%d')
            c.execute("SELECT COUNT(*) FROM tracks WHERE name = ? AND artists = ? AND date = ?",
                      (track_name, track_artists, track_date))
            data_exists = c.fetchone()[0] > 0
            if not data_exists:
                c.execute("INSERT INTO tracks (name, artists, image, popularity, date) VALUES (?, ?, ?, ?, ?)",
                          (track_name, track_artists, track_image, track_popularity, track_date))
        conn.commit()
        conn.close()


update_database()
