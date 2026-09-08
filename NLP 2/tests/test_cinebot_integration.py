import unittest
import json
import re
from app import app

class CineBotIntegrationTest(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_index_html_has_all_cinebot_elements(self):
        """Verify index.html contains all necessary CineBot elements and IDs"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)

        self.assertIn('id="chat-drawer"', html)
        self.assertIn('id="chat-messages"', html)
        self.assertIn('id="chat-input-form"', html)
        self.assertIn('id="chat-input"', html)
        self.assertIn('id="chat-close-btn"', html)
        self.assertIn('id="chat-clear-btn"', html)
        self.assertIn('id="chat-expand-btn"', html)
        self.assertIn('id="floating-chat-trigger"', html)
        self.assertIn('id="nav-chat-btn"', html)

    def test_app_js_cinebot_constants_and_flow(self):
        """Verify static/js/app.js has the exact requested language, cinema, genre, year, type arrays"""
        response = self.client.get('/static/js/app.js')
        self.assertEqual(response.status_code, 200)
        js = response.get_data(as_text=True)

        # Check languages
        expected_languages = [
            "All Languages", "Hindi", "English", "Marathi", "Tamil",
            "Telugu", "Malayalam", "Kannada", "Korean", "Japanese", "Spanish"
        ]
        for lang in expected_languages:
            self.assertIn(f'"{lang}"', js)

        # Check cinemas
        expected_cinemas = [
            "All Cinema", "Bollywood", "Marathi Cinema", "Hollywood",
            "South Indian", "Korean", "Japanese", "International"
        ]
        for cin in expected_cinemas:
            self.assertIn(f'"{cin}"', js)

        # Check genres / mood vibes
        expected_genres = [
            "Romance", "Comedy", "Action", "Horror", "Thriller",
            "Mystery", "Drama", "Sci-Fi", "Fantasy", "Crime", "Feel-Good", "Any Genre"
        ]
        for gen in expected_genres:
            self.assertIn(f'"{gen}"', js)

        # Check Year options
        expected_years = [
            "Any Year", "Latest Releases", "2026", "2025", "2024", "2023",
            "2022", "2021", "2020", "2010s", "2000s", "1990s", "1980s"
        ]
        for yr in expected_years:
            self.assertIn(f'"{yr}"', js)

        # Check Movie / TV options
        self.assertIn('"Movies"', js)
        self.assertIn('"TV Series"', js)

        # Check Initial Welcome greeting
        self.assertIn("Hi! I'm CineBot AI", js)
        self.assertIn("Which language do you prefer?", js)
        self.assertIn("Which cinema do you prefer?", js)
        self.assertIn("What are you in the mood for?", js)
        self.assertIn("What year are you interested in?", js)
        self.assertIn("What do you want to watch?", js)

    def test_api_chat_recommend_all_options(self):
        """Verify POST /api/chat/recommend returns valid recommendations across diverse options"""
        test_payloads = [
            {
                "preferences": {
                    "language": "Hindi",
                    "cinema": "Bollywood",
                    "genres": ["Comedy"],
                    "year": "2024",
                    "type": "Movie",
                    "duration": "90–120 min"
                }
            },
            {
                "preferences": {
                    "language": "All",
                    "cinema": "South Indian",
                    "genres": ["Action"],
                    "year": "Any Year",
                    "type": "Movie",
                    "duration": "Any Duration"
                }
            },
            {
                "preferences": {
                    "language": "Marathi",
                    "cinema": "Marathi Cinema",
                    "genres": ["Drama"],
                    "year": "Latest Releases",
                    "type": "Both",
                    "duration": "Any Duration"
                }
            },
            {
                "preferences": {
                    "language": "English",
                    "cinema": "Hollywood",
                    "genres": ["Sci-Fi"],
                    "year": "2020s",
                    "type": "Movie",
                    "duration": "120–150 min"
                }
            },
            {
                "preferences": {
                    "language": "Korean",
                    "cinema": "Korean",
                    "genres": ["Romance"],
                    "year": "Any Year",
                    "type": "TV Show",
                    "duration": "Any Duration"
                }
            },
            {
                "preferences": {
                    "language": "All",
                    "cinema": "All",
                    "genres": ["Any Genre"],
                    "year": "1800",  # Edge case: non-existent year
                    "type": "Both",
                    "duration": "Any Duration"
                }
            }
        ]

        for payload in test_payloads:
            res = self.client.post('/api/chat/recommend',
                                   data=json.dumps(payload),
                                   content_type='application/json')
            self.assertEqual(res.status_code, 200)
            data = res.get_json()

            if payload['preferences']['year'] == '1800':
                self.assertTrue(data.get('not_found_year', False))
            else:
                self.assertTrue(data.get('success', False))
                self.assertIn('movies', data)
                self.assertIn('response', data)
                self.assertGreater(len(data['movies']), 0)

if __name__ == '__main__':
    unittest.main()
