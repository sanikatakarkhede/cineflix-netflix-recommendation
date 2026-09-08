"""
NLP & Hybrid Recommendation Engine for CineFlix AI.
Implements TF-IDF feature engineering, cosine similarity, dynamic user preference modeling,
hybrid scoring, and explainable AI recommendation rationale across diverse international
and Indian Netflix cinema.
"""

import json
import os
import re
from typing import List, Dict, Any, Optional, Tuple
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class MovieRecommender:
    def __init__(self, catalog_path: str = "data/netflix_catalog.json"):
        self.catalog_path = catalog_path
        self.movies: List[Dict[str, Any]] = []
        self.movie_dict: Dict[str, Dict[str, Any]] = {}
        self.title_to_id: Dict[str, str] = {}
        self.vectorizer: Optional[TfidfVectorizer] = None
        self.tfidf_matrix: Optional[np.ndarray] = None
        self.similarity_matrix: Optional[np.ndarray] = None
        self.id_to_idx: Dict[str, int] = {}
        self.idx_to_id: Dict[int, str] = {}
        
        self.load_catalog()
        self.fit_vectorizer()

    def load_catalog(self):
        """Loads Netflix movies catalog from JSON file."""
        if not os.path.exists(self.catalog_path):
            raise FileNotFoundError(f"Catalog file not found: {self.catalog_path}")
        
        with open(self.catalog_path, "r", encoding="utf-8") as f:
            self.movies = json.load(f)
            
        for m in self.movies:
            yr = m.get("releaseYear") or m.get("release_year")
            if yr:
                m["releaseYear"] = yr
                m["release_year"] = yr
            poster = m.get("poster") or m.get("poster_url")
            if poster:
                m["poster"] = poster
                m["poster_url"] = poster
            backdrop = m.get("backdrop") or m.get("backdrop_url")
            if backdrop:
                m["backdrop"] = backdrop
                m["backdrop_url"] = backdrop

        self.movie_dict = {m["id"]: m for m in self.movies}
        self.title_to_id = {m["title"].strip().lower(): m["id"] for m in self.movies}
        self.id_to_idx = {m["id"]: i for i, m in enumerate(self.movies)}
        self.idx_to_id = {i: m["id"] for i, m in enumerate(self.movies)}

    @staticmethod
    def _create_metadata_soup(movie: Dict[str, Any]) -> str:
        """Constructs weighted metadata soup for TF-IDF extraction."""
        title = movie.get("title", "")
        director = " ".join([d.replace(" ", "_") for d in movie.get("director", "").split(", ")])
        cast = " ".join([c.replace(" ", "_") for c in movie.get("cast", [])])
        cast_plain = " ".join(movie.get("cast", []))
        genres = " ".join(movie.get("genres", []))
        language = movie.get("language", "")
        country = movie.get("country", "")
        industry = movie.get("industry", "")
        mood_tags = " ".join([m.replace(" ", "_") for m in movie.get("mood_tags", [])])
        keywords = " ".join(movie.get("keywords", []))
        description = movie.get("description", "")
        
        # Multiply high-signal tokens (title, language, industry, genres, director, cast, mood_tags, keywords)
        soup = f"{title} {title} {language} {language} {country} {industry} {genres} {genres} {director} {director} {cast} {cast_plain} {mood_tags} {mood_tags} {keywords} {keywords} {description}"
        return soup.lower()

    def fit_vectorizer(self):
        """Builds TF-IDF matrix and cosine similarity matrix."""
        soups = [self._create_metadata_soup(m) for m in self.movies]
        self.vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2),
            sublinear_tf=True,
            max_features=6000
        )
        self.tfidf_matrix = self.vectorizer.fit_transform(soups).toarray()
        self.similarity_matrix = cosine_similarity(self.tfidf_matrix, self.tfidf_matrix)

    def get_movie_by_id(self, movie_id: str) -> Optional[Dict[str, Any]]:
        return self.movie_dict.get(movie_id)

    def find_movie_by_title(self, query: str) -> Optional[Dict[str, Any]]:
        """Fuzzy match movie by title."""
        query_norm = query.strip().lower()
        if query_norm in self.title_to_id:
            return self.movie_dict[self.title_to_id[query_norm]]
        
        # Substring search
        for title_norm, movie_id in self.title_to_id.items():
            if query_norm in title_norm or title_norm in query_norm:
                return self.movie_dict[movie_id]
        return None

    def get_similar_movies(self, movie_id: str, top_n: int = 6) -> List[Dict[str, Any]]:
        """Returns top_n most similar movies based on content cosine similarity."""
        if movie_id not in self.id_to_idx:
            return []
        
        idx = self.id_to_idx[movie_id]
        sim_scores = list(enumerate(self.similarity_matrix[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        # Exclude self
        sim_scores = [s for s in sim_scores if s[0] != idx][:top_n]
        
        results = []
        target_movie = self.movies[idx]
        for s_idx, score in sim_scores:
            candidate = dict(self.movies[s_idx])
            match_pct = int(min(99, max(65, 65 + score * 45)))
            candidate["match_score"] = match_pct
            candidate["explanation"] = self._generate_item_explanation(target_movie, candidate)
            results.append(candidate)
        return results

    def _generate_item_explanation(self, source: Dict[str, Any], target: Dict[str, Any]) -> str:
        """Generates clear explainable rationale between two items."""
        shared_genres = set(source.get("genres", [])) & set(target.get("genres", []))
        shared_moods = set(source.get("mood_tags", [])) & set(target.get("mood_tags", []))
        shared_cast = set(source.get("cast", [])) & set(target.get("cast", []))
        
        reasons = []
        if shared_cast:
            reasons.append(f"stars {', '.join(list(shared_cast)[:2])}")
        if source.get("director") and source.get("director") == target.get("director"):
            reasons.append(f"directed by {source['director']}")
        if shared_moods:
            reasons.append(f"shares the '{', '.join(list(shared_moods)[:2])}' vibe")
        if shared_genres:
            reasons.append(f"matches the {', '.join(list(shared_genres)[:2])} tone of {source['title']}")
            
        if not reasons:
            reasons.append(f"similar thematic pacing and storytelling style to {source['title']}")
            
        return "Because you liked " + source["title"] + ", which " + "; and ".join(reasons) + "."

    def build_user_preference_vector(self, user_profile: Dict[str, Any]) -> Optional[np.ndarray]:
        """
        Synthesizes a dynamic user taste vector from ratings, watch history, liked/disliked items,
        and explicit genre preferences.
        """
        if self.tfidf_matrix is None:
            return None
        
        num_features = self.tfidf_matrix.shape[1]
        user_vector = np.zeros(num_features)
        total_weight = 0.0

        ratings = user_profile.get("ratings", {})
        watch_history = user_profile.get("watch_history", [])
        disliked = set(user_profile.get("disliked", []))

        rating_multipliers = {5: 2.0, 4: 1.3, 3: 0.7, 2: -0.5, 1: -1.5}

        for movie_id, rating in ratings.items():
            if movie_id in self.id_to_idx:
                idx = self.id_to_idx[movie_id]
                weight = rating_multipliers.get(int(rating), 1.0)
                user_vector += weight * self.tfidf_matrix[idx]
                total_weight += abs(weight)

        for item in watch_history:
            movie_id = item if isinstance(item, str) else item.get("id")
            if movie_id and movie_id in self.id_to_idx and movie_id not in ratings:
                idx = self.id_to_idx[movie_id]
                user_vector += 0.8 * self.tfidf_matrix[idx]
                total_weight += 0.8

        for movie_id in disliked:
            if movie_id in self.id_to_idx:
                idx = self.id_to_idx[movie_id]
                user_vector -= 1.8 * self.tfidf_matrix[idx]
                total_weight += 1.8

        pref_genres = user_profile.get("preferred_genres", [])
        pref_moods = user_profile.get("preferred_moods", [])
        if pref_genres or pref_moods:
            text_query = " ".join(pref_genres * 2 + pref_moods * 2)
            query_vec = self.vectorizer.transform([text_query]).toarray()[0]
            user_vector += 1.5 * query_vec
            total_weight += 1.5

        if total_weight > 0 and np.linalg.norm(user_vector) > 0:
            return user_vector / np.linalg.norm(user_vector)
        return None

    def recommend_for_user(
        self,
        user_profile: Dict[str, Any],
        top_n: int = 12,
        genre_filter: Optional[str] = None,
        type_filter: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Generates personalized Netflix recommendations based on dynamic user preference profile.
        Combines preference vector similarity, genre affinity, mood synergy, and IMDb popularity prior.
        """
        user_vector = self.build_user_preference_vector(user_profile)
        
        watched_ids = set()
        for item in user_profile.get("watch_history", []):
            m_id = item if isinstance(item, str) else item.get("id")
            if m_id:
                watched_ids.add(m_id)
        watched_ids.update(user_profile.get("ratings", {}).keys())
        watched_ids.update(user_profile.get("disliked", []))

        # Compute similarity scores
        if user_vector is not None:
            user_sims = cosine_similarity([user_vector], self.tfidf_matrix)[0]
        else:
            user_sims = np.zeros(len(self.movies))

        # Extract top user genres & moods for synergy calculation
        user_genre_counts: Dict[str, float] = {}
        user_mood_counts: Dict[str, float] = {}
        for m_id, rating in user_profile.get("ratings", {}).items():
            movie = self.movie_dict.get(m_id)
            if movie and int(rating) >= 3:
                w = float(rating) / 5.0
                for g in movie.get("genres", []):
                    user_genre_counts[g] = user_genre_counts.get(g, 0) + w
                for m in movie.get("mood_tags", []):
                    user_mood_counts[m] = user_mood_counts.get(m, 0) + w

        scored_candidates = []
        for i, movie in enumerate(self.movies):
            movie_id = movie["id"]
            if movie_id in watched_ids:
                continue
            
            if genre_filter and genre_filter.lower() != "all":
                if genre_filter.lower() not in [g.lower() for g in movie.get("genres", [])]:
                    continue

            if type_filter and type_filter.lower() != "all":
                if type_filter.lower() != movie.get("type", "").lower():
                    continue

            content_sim = float(user_sims[i]) if user_vector is not None else 0.5
            imdb_prior = float(movie.get("imdb_score", 7.0)) / 10.0

            # Genre synergy
            genre_synergy = 0.0
            for g in movie.get("genres", []):
                genre_synergy += user_genre_counts.get(g, 0.0)
            genre_synergy = min(1.0, genre_synergy / 3.0) if user_genre_counts else 0.5

            # Mood synergy
            mood_synergy = 0.0
            for m in movie.get("mood_tags", []):
                mood_synergy += user_mood_counts.get(m, 0.0)
            mood_synergy = min(1.0, mood_synergy / 2.0) if user_mood_counts else 0.5

            # Dynamic weight sliders
            sliders = user_profile.get("sliders", {})
            action_pref = sliders.get("action_level", 50) / 100.0
            dark_pref = sliders.get("dark_tone", 50) / 100.0

            modifier = 0.0
            if "Action" in movie.get("genres", []):
                modifier += (action_pref - 0.5) * 0.15
            if any(t in ["Dark", "Chilling", "Grim", "Bleak"] for t in movie.get("mood_tags", [])):
                modifier += (dark_pref - 0.5) * 0.15

            # Hybrid score computation
            if user_vector is not None:
                final_score = (0.45 * content_sim) + (0.25 * genre_synergy) + (0.15 * mood_synergy) + (0.15 * imdb_prior) + modifier
                match_pct = int(min(99, max(68, int(final_score * 100) + 18)))
            else:
                final_score = (0.60 * imdb_prior) + (0.40 * 0.5) + modifier
                match_pct = int(min(98, max(75, int(imdb_prior * 90) + 10)))

            explanation = self._generate_profile_explanation(user_profile, movie, user_genre_counts, user_mood_counts)
            
            cand_copy = dict(movie)
            cand_copy["match_score"] = match_pct
            cand_copy["explanation"] = explanation
            scored_candidates.append((final_score, cand_copy))

        scored_candidates.sort(key=lambda x: x[0], reverse=True)
        return [c[1] for c in scored_candidates[:top_n]]

    def _generate_profile_explanation(
        self,
        user_profile: Dict[str, Any],
        movie: Dict[str, Any],
        user_genres: Dict[str, float],
        user_moods: Dict[str, float]
    ) -> str:
        """Generates dynamic explanation for user profile recommendations."""
        favorite_titles = []
        for m_id, r in user_profile.get("ratings", {}).items():
            if int(r) >= 4 and m_id in self.movie_dict:
                favorite_titles.append(self.movie_dict[m_id])

        matched_fav = None
        for fav in favorite_titles:
            shared = set(fav.get("genres", [])) & set(movie.get("genres", []))
            if fav.get("director") == movie.get("director") or len(shared) >= 2:
                matched_fav = fav
                break

        if matched_fav:
            return f"Recommended because you loved {matched_fav['title']} and this shares its high-stakes storytelling and {movie['genres'][0]} style."

        if user_genres:
            top_genre = max(user_genres.items(), key=lambda x: x[1])[0]
            if top_genre in movie.get("genres", []):
                mood_str = movie["mood_tags"][0] if movie.get("mood_tags") else "thrilling"
                return f"Tailored to your love for {top_genre} with a {mood_str.lower()} atmosphere."

        mood_tag = movie["mood_tags"][0] if movie.get("mood_tags") else "Cinematic"
        return f"{mood_tag} Netflix standout featuring top-rated {movie['genres'][0]} performances."

    def search_movies(self, query: str, top_n: int = 100) -> List[Dict[str, Any]]:
        """
        Deep multi-field universal search combining exact/partial token matches
        across title, cast, director, genres, language, country, industry, keywords,
        moods, and descriptions with TF-IDF cosine semantic similarity.
        """
        if not query or not query.strip():
            return list(self.movies[:top_n])
        
        raw_query = query.strip()
        query_norm = raw_query.lower()
        
        # Detect type intent keywords
        type_intent = None
        if "movie" in query_norm or "film" in query_norm:
            type_intent = "Movie"
        elif "tv" in query_norm or "series" in query_norm or "show" in query_norm:
            type_intent = "TV Show"
            
        # Strip generic stopwords for core keyword matching, but keep for type scoring
        cleaned_query = re.sub(r'\b(movie|movies|film|films|series|tv|show|shows)\b', '', query_norm).strip()
        if not cleaned_query:
            cleaned_query = query_norm

        query_tokens = [t for t in re.findall(r'\w+', cleaned_query) if len(t) > 1]
        
        # TF-IDF similarity scores
        tfidf_scores = np.zeros(len(self.movies))
        if self.vectorizer is not None and hasattr(self, 'tfidf_matrix') and self.tfidf_matrix is not None:
            try:
                query_vec = self.vectorizer.transform([cleaned_query]).toarray()
                tfidf_scores = cosine_similarity(query_vec, self.tfidf_matrix)[0]
            except Exception:
                pass

        # Normalized actor/director alias mappings
        alias_map = {
            "amir": "aamir khan",
            "amir khan": "aamir khan",
            "srk": "shah rukh khan",
            "king khan": "shah rukh khan",
            "big b": "amitabh bachchan",
            "amitabh": "amitabh bachchan",
            "nolan": "christopher nolan",
            "rajamouli": "s.s. rajamouli",
            "lokesh": "lokesh kanagaraj",
            "vijay": "thalapathy vijay",
            "kdrama": "korean",
            "k-drama": "korean",
            "anime": "japanese animation",
            "tollywood": "telugu",
            "kollywood": "tamil",
            "mollywood": "malayalam",
            "sandalwood": "kannada"
        }

        # Check if query matches an alias
        effective_query = query_norm
        for alias, target in alias_map.items():
            if alias in query_norm:
                effective_query = f"{effective_query} {target}"

        scored_results = []
        for idx, movie in enumerate(self.movies):
            score = float(tfidf_scores[idx]) * 3.0  # Base TF-IDF weight
            
            title = movie.get("title", "").lower()
            original_title = movie.get("originalTitle", "").lower()
            director = movie.get("director", "").lower()
            cast_list = [c.lower() for c in movie.get("cast", [])]
            cast_str = " ".join(cast_list)
            genres_list = [g.lower() for g in movie.get("genres", [])]
            language = movie.get("language", "").lower()
            country = movie.get("country", "").lower()
            industry = movie.get("industry", "").lower()
            keywords_list = [k.lower() for k in movie.get("keywords", [])]
            keywords_str = " ".join(keywords_list)
            mood_list = [m.lower() for m in movie.get("mood_tags", [])]
            desc = movie.get("description", "").lower()
            m_type = movie.get("type", "")

            # Exact or prefix match on title
            if query_norm == title or query_norm == original_title:
                score += 30.0
            elif title.startswith(query_norm) or original_title.startswith(query_norm):
                score += 20.0
            elif query_norm in title or query_norm in original_title:
                score += 15.0
            elif cleaned_query in title or cleaned_query in original_title:
                score += 12.0

            # Language & Industry match
            if language and (language == query_norm or query_norm.startswith(language) or language.startswith(query_norm)):
                score += 25.0
            elif language and language in query_norm:
                score += 18.0

            if industry and (industry == query_norm or industry in query_norm or query_norm in industry):
                score += 20.0

            if country and (country == query_norm or country in query_norm):
                score += 10.0

            # Genre match
            for g in genres_list:
                if g == query_norm or query_norm == g:
                    score += 20.0
                elif g in query_norm or query_norm in g:
                    score += 12.0

            # Director match
            if director and (query_norm in director or director in query_norm or any(t in director for t in query_tokens)):
                score += 18.0

            # Cast match
            if any(query_norm in c for c in cast_list) or query_norm in cast_str:
                score += 20.0

            # Type alignment bonus
            if type_intent and type_intent == m_type:
                score += 3.0

            # Token-level field matching
            token_matches = 0
            for token in query_tokens:
                matched = False
                if token in title or token in original_title:
                    score += 5.0
                    matched = True
                if token in cast_str:
                    score += 4.5
                    matched = True
                if token in director:
                    score += 4.5
                    matched = True
                if token == language or token in language:
                    score += 6.0
                    matched = True
                if token == industry or token in industry:
                    score += 5.0
                    matched = True
                if any(token == g or token in g for g in genres_list):
                    score += 4.5
                    matched = True
                if any(token in m for m in mood_list):
                    score += 3.0
                    matched = True
                if any(token in k for k in keywords_list):
                    score += 3.5
                    matched = True
                if token in desc:
                    score += 1.5
                    matched = True
                
                if matched:
                    token_matches += 1
            
            # Multi-token synergy bonus if all query tokens appear in record
            if query_tokens and token_matches >= len(query_tokens):
                score += 8.0

            # Special case prefix searches e.g. "mara" -> Marathi, "3 id" -> 3 Idiots, "inter" -> Interstellar
            if len(query_norm) >= 3:
                if title.startswith(query_norm) or any(w.startswith(query_norm) for w in title.split()):
                    score += 10.0
                if language.startswith(query_norm) or industry.startswith(query_norm):
                    score += 12.0
                if any(c.startswith(query_norm) or any(w.startswith(query_norm) for w in c.split()) for c in cast_list):
                    score += 8.0

            if score > 0.05:
                m_copy = dict(movie)
                m_copy["search_relevance"] = round(score, 3)
                scored_results.append((score, m_copy))

        scored_results.sort(key=lambda x: x[0], reverse=True)
        return [item[1] for item in scored_results[:top_n]]


# Built-in User Personas for quick testing & demonstration
PERSONA_PROFILES = {
    "sci_fi_geek": {
        "id": "sci_fi_geek",
        "name": "Alex (Sci-Fi & Mind Benders)",
        "avatar": "🚀",
        "description": "Loves Christopher Nolan, time loops, deep psychological mysteries, and high-concept Sci-Fi.",
        "watch_history": ["h1", "h2", "tv3", "h7", "h4"],
        "ratings": {
            "h1": 5,  # Inception
            "h2": 5,  # Interstellar
            "tv3": 5, # Dark
            "h7": 5,  # The Matrix
            "h4": 4   # The Prestige
        },
        "disliked": ["b23", "tv5"],
        "preferred_genres": ["Sci-Fi", "Mystery", "Thriller"],
        "preferred_moods": ["Mind-bending", "Cerebral", "Atmospheric"],
        "sliders": {"action_level": 70, "dark_tone": 80, "plot_depth": 95}
    },
    "true_crime_addict": {
        "id": "true_crime_addict",
        "name": "Sarah (True Crime & Dark Thrillers)",
        "avatar": "🔍",
        "description": "Binge-watches gritty crime sagas, mind games, and intense investigative police procedurals.",
        "watch_history": ["tv1", "tv10", "tv13", "b10", "b11"],
        "ratings": {
            "tv1": 5,  # Breaking Bad
            "tv10": 5, # Peaky Blinders
            "tv13": 5, # Sacred Games
            "b10": 5,  # Andhadhun
            "b11": 4   # Drishyam
        },
        "disliked": ["b27", "tv23"],
        "preferred_genres": ["Crime", "Drama", "Thriller", "Mystery"],
        "preferred_moods": ["Dark", "Psychological", "Chilling", "Gritty"],
        "sliders": {"action_level": 40, "dark_tone": 95, "plot_depth": 90}
    },
    "feel_good_fan": {
        "id": "feel_good_fan",
        "name": "Jordan (Feel-Good & Cozy Rom-Coms)",
        "avatar": "🍿",
        "description": "Looking for heartwarming laughs, witty banter, comforting series, and charming romantic comedies.",
        "watch_history": ["b1", "b7", "b8", "tv22", "tv23"],
        "ratings": {
            "b1": 5,   # 3 Idiots
            "b7": 5,   # ZNMD
            "b8": 5,   # Queen
            "tv22": 5, # The Office
            "tv23": 5  # Friends
        },
        "disliked": ["h13", "int6"], # Fight Club, The Platform
        "preferred_genres": ["Comedy", "Romance", "Drama"],
        "preferred_moods": ["Wholesome", "Hilarious", "Heartwarming", "Feel-Good"],
        "sliders": {"action_level": 20, "dark_tone": 10, "plot_depth": 60}
    },
    "adrenaline_junkie": {
        "id": "adrenaline_junkie",
        "name": "Marcus (Action & High-Stakes Blockbusters)",
        "avatar": "🔥",
        "description": "Thrives on explosive stuntwork, adrenaline-fueled shootouts, superhero epics, and high-octane blockbusters.",
        "watch_history": ["si1", "si2", "si6", "si9", "h3"],
        "ratings": {
            "si1": 5,  # RRR
            "si2": 5,  # Baahubali
            "si6": 5,  # KGF
            "si9": 5,  # Vikram
            "h3": 5    # The Dark Knight
        },
        "disliked": ["mr9", "mr10"], # Court, Killa
        "preferred_genres": ["Action", "Adventure", "Thriller"],
        "preferred_moods": ["Non-Stop Action", "Adrenaline", "Epic", "Explosive"],
        "sliders": {"action_level": 95, "dark_tone": 60, "plot_depth": 65}
    },
    "clean_slate": {
        "id": "clean_slate",
        "name": "Guest (New Profile)",
        "avatar": "✨",
        "description": "Fresh profile with no past history. Interact with titles to teach CineFlix your taste!",
        "watch_history": [],
        "ratings": {},
        "disliked": [],
        "preferred_genres": [],
        "preferred_moods": [],
        "sliders": {"action_level": 50, "dark_tone": 50, "plot_depth": 50}
    }
}
