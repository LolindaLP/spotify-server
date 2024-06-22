import unittest
import sqlite3
import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
import sys
from app import get_top_tracks_for_date, get_top_artists, get_data_for_plot
from data_base import get_token, update_database

class TestGetTopTracksForDate(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # Create a temporary database in memory
        cls.conn = sqlite3.connect(':memory:')
        cls.cursor = cls.conn.cursor()

        # Create the tracks table schema
        cls.cursor.execute('''
            CREATE TABLE tracks (
                id INTEGER PRIMARY KEY,
                name TEXT,
                artists TEXT,
                image TEXT,
                date DATE,
                popularity INTEGER
            )
        ''')

        cls.conn.commit()
        
        # Insert test data
        cls.test_data = [
            ('Song 1', 'Artist A', 'image1.jpg', '2023-05-22', 100),
            ('Song 2', 'Artist B', 'image2.jpg', '2023-05-22', 95),
            ('Song 3', 'Artist A, Artist C', 'image3.jpg', '2023-05-21', 80),
            ('Song 4', 'Artist D', 'image4.jpg', '2023-05-20', 70),
            ('Song 5', 'Artist A, Artist B', 'image5.jpg', '2023-05-19', 85)
        ]
        cls.cursor.executemany('''
            INSERT INTO tracks (name, artists, image, date, popularity)
            VALUES (?, ?, ?, ?, ?)
        ''', cls.test_data)
        cls.conn.commit()
    
    @classmethod
    def tearDownClass(cls):
        cls.conn.close()
    
    def test_get_top_tracks_for_valid_date(self):
        # Test with a valid date that exists in the database
        date = '2023-05-22'
        expected_tracks = [
            ('Song 1', 'Artist A', 'image1.jpg'),
            ('Song 2', 'Artist B', 'image2.jpg')
        ]
        result = get_top_tracks_for_date(date, conn=self.conn, database=':memory:')
        self.assertEqual(result, expected_tracks)
    
    def test_get_top_tracks_for_non_existent_date(self):
        # Test with a valid date that does not exist in the database
        date = '2022-01-01'
        expected_tracks = []
        result = get_top_tracks_for_date(date)
        self.assertEqual(result, expected_tracks)
    
    def test_get_top_tracks_for_invalid_date(self):
        # Test with an invalid date format
        date = 'invalid-date'
        with self.assertRaises(ValueError):
            get_top_tracks_for_date(date)


    def test_get_top_artists_default_limit(self):
        # Test with default limit
        expected_artists = [
            ('Artist A', 3),
            ('Artist B', 2),
            ('Artist C', 1),
            ('Artist D', 1)
        ]
        result = get_top_artists(self.cursor)
        self.assertEqual(result, expected_artists[:5])

    
    def test_get_top_artists_no_artists(self):
        new_conn = sqlite3.connect(':memory:')
        new_cursor = new_conn.cursor()
        new_cursor.execute('''
            CREATE TABLE tracks (
                artists TEXT
            )
        ''')
        new_conn.commit()
        
        expected_artists = []
        result = get_top_artists(new_cursor)
        self.assertEqual(result, expected_artists)
        new_conn.close()
        

    def test_get_data_for_plot(self):

        top_artists = [('Artist A', 3), ('Artist B', 2), ('Artist C', 1), ('Artist D', 1)]

        dates, artist_data, song_data = get_data_for_plot(self.cursor, top_artists)

        expected_dates = ['2023-05-19', '2023-05-20', '2023-05-21', '2023-05-22']
        expected_artist_data = {
            'Artist A': [1, 0, 1, 1],
            'Artist B': [1, 0, 0, 1],
            'Artist C': [0, 0, 1, 0],
            'Artist D': [0, 1, 0, 0],
        }

        self.assertEqual(dates, expected_dates)
        self.assertEqual(artist_data, expected_artist_data)



class TestSpotifyDatabaseUpdate(unittest.TestCase):
    
    @patch('data_base.requests.post')
    @patch('data_base.os.getenv')
    def test_get_token(self, mock_getenv, mock_post):
        # Mock environment variables
        mock_getenv.side_effect = lambda key: {'CLIENT_ID': 'fake_client_id', 'CLIENT_SECRET': 'fake_client_secret'}.get(key)
        
        # Mock response of requests.post
        mock_response = MagicMock()
        mock_response.json.return_value = {"access_token": "fake_access_token"}
        mock_post.return_value = mock_response
        
        token = get_token()
        
        # Assertions
        self.assertEqual(token, "fake_access_token")
        mock_getenv.assert_any_call("CLIENT_ID")
        mock_getenv.assert_any_call("CLIENT_SECRET")
        mock_post.assert_called_once()
        
    @patch('data_base.requests.get')
    @patch('data_base.get_token', return_value="fake_access_token")
    def test_update_database(self, mock_get_token, mock_get):
        # Mock response of requests.get
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'items': [
                {
                    'track': {
                        'name': 'Fake Track',
                        'artists': [{'name': 'Fake Artist'}],
                        'album': {'images': [{'url': 'http://fakeimage.com'}]},
                        'popularity': 50
                    }
                }
            ]
        }
        mock_get.return_value = mock_response
        
        # Redirect stdout to capture print statements
        captured_output = StringIO()
        sys.stdout = captured_output

        # Run the function
        update_database()
        
        # Revert redirect.
        sys.stdout = sys.__stdout__
        
        # Connect to the database and check if the data was inserted
        conn = sqlite3.connect('/home/ec2-user/spotify-server/tracksdb/tracks.db')
        c = conn.cursor()
        
        c.execute("SELECT * FROM tracks WHERE name = 'Fake Track' AND artists = 'Fake Artist'")
        tracks = c.fetchall()
        
        # Assertions
        self.assertEqual(len(tracks), 1)
        self.assertEqual(tracks[0][1], 'Fake Track')
        self.assertEqual(tracks[0][2], 'Fake Artist')
        self.assertEqual(tracks[0][3], 'http://fakeimage.com')
        self.assertEqual(tracks[0][4], 50)
        
        # Delete test artist from database
        c.execute("DELETE FROM tracks WHERE name = 'Fake Track' AND artists = 'Fake Artist'")
        conn.commit()

        conn.close()



if __name__ == '__main__':
    unittest.main()

