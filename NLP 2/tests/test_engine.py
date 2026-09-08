"""
Automated unit and integration test suite for CineFlix.
Tests the TF-IDF recommendation engine, user preference vector modeling,
conversational NLP CineBot, UserManager authentication, per-user isolation,
and Flask API endpoints.
"""

import unittest
import json
import os
import shutil
from engine.recommender import MovieRecommender, PERSONA_PROFILES
from engine.nlp_chat import CineBot
from engine.auth import UserManager
from app import app, recommender


class TestRecommenderEngine(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.recommender = MovieRecommender("data/netflix_catalog.json")
        cls.cinebot = CineBot(cls.recommender)

    def test_catalog_loaded(self):
        self.assertGreater(len(self.recommender.movies), 50, "Catalog should have at least 50 titles")
        self.assertIsNotNone(self.recommender.tfidf_matrix)
        self.assertIsNotNone(self.recommender.similarity_matrix)

    def test_similar_movies(self):
        # Inception should be similar to Interstellar / Tenet / Shutter Island
        inception = self.recommender.find_movie_by_title("Inception")
        self.assertIsNotNone(inception)
        similars = self.recommender.get_similar_movies(inception["id"], top_n=5)
        self.assertEqual(len(similars), 5)
        titles = [m["title"] for m in similars]
        self.assertTrue(any(t in titles for t in ["Interstellar", "Tenet", "The Matrix", "Shutter Island", "The Prestige"]))

    def test_user_preference_profiling(self):
        # Sci-Fi Persona should receive Sci-Fi / Thriller recommendations
        sci_fi_profile = PERSONA_PROFILES["sci_fi_geek"]
        recs = self.recommender.recommend_for_user(sci_fi_profile, top_n=6)
        self.assertEqual(len(recs), 6)
        # Should contain high-concept Sci-Fi titles not already watched
        rec_genres = [g for m in recs for g in m["genres"]]
        self.assertIn("Sci-Fi", rec_genres)

    def test_cold_start_profile(self):
        # Clean slate profile with 0 ratings
        clean_profile = PERSONA_PROFILES["clean_slate"]
        recs = self.recommender.recommend_for_user(clean_profile, top_n=8)
        self.assertEqual(len(recs), 8)
        # Verify valid match score within expected bounds
        for r in recs:
            self.assertTrue(50 <= r["match_score"] <= 100)

    def test_cinebot_entity_and_intent(self):
        # Test 1: Mood query
        msg = "I'm stressed, give me a feel-good romantic comedy"
        res = self.cinebot.process_message(msg, PERSONA_PROFILES["clean_slate"])
        self.assertIn("response", res)
        self.assertGreater(len(res["movies"]), 0)
        self.assertIn("Comedy", [g for m in res["movies"] for g in m["genres"]])

        # Test 2: Actor query
        msg2 = "Show me movies with Leonardo DiCaprio"
        res2 = self.cinebot.process_message(msg2, PERSONA_PROFILES["clean_slate"])
        self.assertGreater(len(res2["movies"]), 0)
        
        # Test 3: Title similarity query
        msg3 = "Something similar to Stranger Things and Dark"
        res3 = self.cinebot.process_message(msg3, PERSONA_PROFILES["clean_slate"])
        self.assertGreater(len(res3["movies"]), 0)


class TestUserManager(unittest.TestCase):
    def setUp(self):
        self.test_storage = "data/test_users.json"
        if os.path.exists(self.test_storage):
            os.remove(self.test_storage)
        self.um = UserManager(self.test_storage)

    def tearDown(self):
        if os.path.exists(self.test_storage):
            os.remove(self.test_storage)

    def test_user_creation_and_auth(self):
        success, msg, user = self.um.create_user("Sanika Takarkhede", "sanika@example.com", "secure123")
        self.assertTrue(success)
        self.assertIsNotNone(user)
        self.assertEqual(user["email"], "sanika@example.com")
        self.assertNotIn("password_hash", user)

        # Successful auth
        auth_ok, auth_msg, auth_user = self.um.authenticate_user("sanika@example.com", "secure123")
        self.assertTrue(auth_ok)
        self.assertEqual(auth_user["name"], "Sanika Takarkhede")

        # Wrong password
        bad_auth, bad_msg, _ = self.um.authenticate_user("sanika@example.com", "wrongpass")
        self.assertFalse(bad_auth)

    def test_user_interaction_isolation(self):
        # Create User A & User B
        _, _, user_a = self.um.create_user("User A", "usera@example.com", "pass123")
        _, _, user_b = self.um.create_user("User B", "userb@example.com", "pass123")

        # User A rates Inception (m1) 5 stars
        self.um.record_interaction(user_a["id"], "rate", "m1", 5)

        # User B rates La La Land (m31) 5 stars
        self.um.record_interaction(user_b["id"], "rate", "m31", 5)

        prof_a = self.um.get_user_profile(user_a["id"])
        prof_b = self.um.get_user_profile(user_b["id"])

        self.assertIn("m1", prof_a["ratings"])
        self.assertNotIn("m31", prof_a["ratings"])

        self.assertIn("m31", prof_b["ratings"])
        self.assertNotIn("m1", prof_b["ratings"])


class TestFlaskAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()

    def test_index_route(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        html = response.data.decode("utf-8")
        self.assertIn("CINE", html)
        self.assertIn("FLIX", html)
        # Ensure AI badge is NOT part of CineFlix logo
        self.assertNotIn('<span class="logo-badge"><i class="fa-solid fa-brain"></i> AI</span>', html)
        # Ensure promotional badge and feature preview strip are completely removed
        self.assertNotIn("Netflix Movie Recommendation Engine & CineBot Curator", html)
        self.assertNotIn("Hybrid NLP & Preference Vector Filtering", html)
        self.assertNotIn("CineBot Conversational Curator", html)
        self.assertNotIn("Curated Netflix Movies & TV Series Catalog", html)
        # Ensure footer descriptive text is removed
        self.assertNotIn("Intelligent Natural Language Movie Recommendation Engine for Netflix.", html)
        self.assertNotIn("Hybrid Content-Based & Preference Vector Filtering", html)
        self.assertNotIn("Powered by TF-IDF, Cosine Similarity & CineBot NLP", html)

    def test_auth_signup_and_login_flow(self):
        import uuid
        email = f"test_{uuid.uuid4().hex[:8]}@cineflix.ai"
        # Signup
        signup_res = self.client.post("/api/auth/signup", json={
            "name": "Integration Tester",
            "email": email,
            "password": "password123"
        })
        self.assertEqual(signup_res.status_code, 200)
        signup_data = signup_res.get_json()
        self.assertTrue(signup_data["success"])

        # Check me
        me_res = self.client.get("/api/auth/me")
        me_data = me_res.get_json()
        self.assertTrue(me_data["authenticated"])
        self.assertEqual(me_data["user"]["email"], email)

        # Logout
        logout_res = self.client.post("/api/auth/logout")
        self.assertEqual(logout_res.status_code, 200)

        # Check me again (now unauthenticated)
        me_res2 = self.client.get("/api/auth/me")
        self.assertFalse(me_res2.get_json()["authenticated"])

        # Login
        login_res = self.client.post("/api/auth/login", json={
            "email": email,
            "password": "password123"
        })
        self.assertEqual(login_res.status_code, 200)
        self.assertTrue(login_res.get_json()["success"])

    def test_api_movies(self):
        response = self.client.get("/api/movies?genre=Sci-Fi")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("movies", data)
        self.assertGreater(len(data["movies"]), 0)

    def test_api_recommendations(self):
        response = self.client.post(
            "/api/recommendations",
            json={"top_n": 8}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("recommendations", data)
        self.assertEqual(len(data["recommendations"]), 8)

    def test_api_chat(self):
        response = self.client.post(
            "/api/chat",
            json={"message": "Recommend dark psychological thrillers"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("response", data)
        self.assertIn("movies", data)

    def test_guided_recommendations_and_exact_year(self):
        # Test 1: Guided preferences
        prefs = {
            "language": "Hindi",
            "cinema": "Bollywood",
            "genres": ["Comedy"],
            "year": "Any Year",
            "type": "Movie",
            "duration": "Any Duration"
        }
        res = self.client.post("/api/chat/recommend", json={"preferences": prefs})
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data["success"])
        self.assertGreater(len(data["movies"]), 0)
        for m in data["movies"]:
            self.assertEqual(m["language"], "Hindi")

        # Test 2: Exact year filter rule (e.g. year with no movies)
        fake_year_prefs = {
            "language": "Hindi",
            "year": 1820
        }
        res_fake = self.client.post("/api/chat/recommend", json={"preferences": fake_year_prefs})
        self.assertEqual(res_fake.status_code, 200)
        data_fake = res_fake.get_json()
        self.assertTrue(data_fake.get("not_found_year", False))
        self.assertEqual(len(data_fake["movies"]), 0)
        self.assertIn("fallback_options", data_fake)

    def test_api_profile_interact(self):
        first_movie_id = recommender.movies[0]["id"]
        response = self.client.post(
            "/api/profile/interact",
            json={"action": "rate", "movie_id": first_movie_id, "rating": 5}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["status"], "success")

    def test_all_requirement_searches(self):
        """Part 19 verification test across all key regional, international, actor, and genre search queries."""
        test_queries = [
            ("marathi", ["Sairat", "Natsamrat", "Katyar Kaljat Ghusali", "Duniyadari", "Pawankhind"]),
            ("marathi movie", ["Sairat", "Natsamrat", "Katyar Kaljat Ghusali", "Timepass", "Faster Fene"]),
            ("hindi", ["3 Idiots", "Dangal", "PK", "Lagaan", "Swades"]),
            ("bollywood", ["3 Idiots", "Dangal", "PK", "Shershaah", "Jawan"]),
            ("tamil", ["Vikram", "Leo", "Jailer", "Master", "96"]),
            ("telugu", ["RRR", "Baahubali", "Pushpa", "Kantara", "Salaar"]),
            ("malayalam", ["Premam", "Drishyam", "Kumbalangi Nights", "Manjummel Boys"]),
            ("kannada", ["K.G.F", "Kantara", "777 Charlie", "Lucia"]),
            ("3 idiots", ["3 Idiots"]),
            ("dangal", ["Dangal"]),
            ("sairat", ["Sairat"]),
            ("natsamrat", ["Natsamrat"]),
            ("amir khan", ["3 Idiots", "Dangal", "PK", "Lagaan", "Taare Zameen Par"]),
            ("shah rukh khan", ["Jawan", "Pathaan", "Swades", "Chak De! India", "Devdas"]),
            ("nolan", ["Inception", "Interstellar", "The Dark Knight", "Oppenheimer", "The Prestige"]),
            ("inception", ["Inception"]),
            ("breaking bad", ["Breaking Bad"]),
            ("thriller", ["Andhadhun", "Drishyam", "Gone Girl", "Se7en", "The Invisible Guest"]),
            ("romance", ["Dilwale Dulhania Le Jayenge", "Jab We Met", "La La Land", "Kal Ho Naa Ho"]),
            ("comedy", ["3 Idiots", "Hera Pheri", "The Office", "Brooklyn Nine-Nine", "Friends"]),
            ("korean", ["Parasite", "Train to Busan", "Oldboy", "Squid Game"]),
            ("japanese", ["Your Name", "Spirited Away", "Demon Slayer", "Suzume"]),
            ("mara", ["Sairat", "Natsamrat", "Duniyadari"]),
            ("3 id", ["3 Idiots"]),
            ("inter", ["Interstellar"])
        ]

        for query, expected_any in test_queries:
            results = recommender.search_movies(query, top_n=20)
            self.assertGreater(len(results), 0, f"Query '{query}' returned 0 results")
            result_titles = [m["title"] for m in results]
            matched = any(any(exp.lower() in t.lower() for exp in expected_any) for t in result_titles)
            self.assertTrue(matched, f"Query '{query}' did not match any of {expected_any}. Top results: {result_titles[:5]}")


if __name__ == "__main__":
    unittest.main()
