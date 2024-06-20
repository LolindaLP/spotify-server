from flask import Flask, render_template, request, jsonify
from datetime import datetime
import sqlite3

app = Flask(__name__)


def get_top_tracks_for_date(date, conn=None, database='tracksdb/tracks.db'):
    try:
        datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Invalid date format. Expected format: YYYY-MM-DD")
    if conn is None:
        conn = sqlite3.connect(database)
    cursor = conn.cursor()
    query = """
    SELECT name, artists, image
    FROM tracks
    WHERE date = ?
    ORDER BY popularity DESC
    LIMIT 50
    """
    cursor.execute(query, (date,))
    tracks = cursor.fetchall()
    if conn != sqlite3.connect(database):
        conn.close()
    return tracks


def get_available_dates(conn=None, database='tracks.db'):
    if conn is None:
        conn = sqlite3.connect(database)
    
    cursor = conn.cursor()
    
    query = "SELECT DISTINCT date FROM tracks ORDER BY date"
    cursor.execute(query)
    all_dates = [row[0] for row in cursor.fetchall()]
    
    # Close the connection if it was created in this function
    if conn != sqlite3.connect(database):
        conn.close()
    
    return all_dates


def get_top_artists(cursor, limit=5):
    cursor.execute("SELECT artists FROM tracks")
    all_artists = cursor.fetchall()
    artist_count = {}
    for artists_str in all_artists:
        artists = artists_str[0].split(", ")
        for artist in artists:
            artist_count[artist] = artist_count.get(artist, 0) + 1
    top_artists = sorted(artist_count.items(),
                         key=lambda x: x[1], reverse=True)[:limit]
    return top_artists


def get_data_for_plot(cursor, top_artists):
    dates = []
    artist_data = {artist: [] for artist, _ in top_artists}
    song_data = {artist: {} for artist, _ in top_artists}  # New variable
    cursor.execute("SELECT DISTINCT date FROM tracks ORDER BY date")
    all_dates = cursor.fetchall()
    for date in all_dates:
        dates.append(date[0])
        for artist, _ in top_artists:
            cursor.execute("SELECT COUNT(*) FROM tracks WHERE artists LIKE ? AND date = ?",
                           ('%'+artist+'%', date[0]))
            count = cursor.fetchone()[0]
            artist_data[artist].append(count)
            cursor.execute("SELECT name FROM tracks WHERE artists LIKE ? AND date = ?",
                           ('%'+artist+'%', date[0]))
            song_titles = [row[0] for row in cursor.fetchall()]
            song_data[artist][date[0]] = song_titles
    return dates, artist_data, song_data


@app.route('/')
def index():
    conn = sqlite3.connect('tracksdb/tracks.db')
    cursor = conn.cursor()
    today = datetime.today().strftime('%Y-%m-%d')
    today_top_tracks = get_top_tracks_for_date(today)
    top_artists = get_top_artists(cursor)
    dates, artist_data, song_data = get_data_for_plot(cursor, top_artists)
    available_dates = get_available_dates()

    return render_template('index.html', dates=dates, artist_data=artist_data, today_top_tracks=today_top_tracks, song_data=song_data, available_dates=available_dates)


@app.route('/available-dates')
def available_dates():
    all_dates = get_available_dates()
    return jsonify(all_dates)


@app.route('/top-tracks', methods=['GET'])
def top_tracks():
    date = request.args.get('date')
    tracks = get_top_tracks_for_date(date)
    return jsonify(tracks)



if __name__ == '__main__':
    app.run(debug=True)
