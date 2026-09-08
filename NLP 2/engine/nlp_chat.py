"""
Conversational NLP Dialogue Manager (CineBot) for CineFlix AI.
Handles intent classification, entity extraction (actors, directors, genres, moods, eras),
sentiment/mood detection, multi-turn conversation memory, and conversational recommendations.
"""

import re
from typing import Dict, Any, List, Optional, Tuple
from engine.recommender import MovieRecommender


class CineBot:
    def __init__(self, recommender: MovieRecommender):
        self.recommender = recommender
        
        # Entity vocabularies
        self.genres_map = {
            "sci-fi": "Sci-Fi", "scifi": "Sci-Fi", "science fiction": "Sci-Fi",
            "action": "Action", "thriller": "Thriller", "suspense": "Thriller",
            "crime": "Crime", "mystery": "Mystery", "detective": "Mystery",
            "drama": "Drama", "comedy": "Comedy", "funny": "Comedy", "humor": "Comedy",
            "romance": "Romance", "romantic": "Romance", "love": "Romance", "romcom": "Romance",
            "horror": "Horror", "scary": "Horror", "spooky": "Horror", "creepy": "Horror",
            "animation": "Animation", "animated": "Animation", "anime": "Animation",
            "documentary": "Documentary", "docuseries": "Documentary",
            "adventure": "Adventure", "fantasy": "Fantasy", "biography": "Biography", "history": "History"
        }

        self.languages_map = {
            "hindi": "Hindi", "bollywood": "Hindi",
            "tamil": "Tamil", "kollywood": "Tamil",
            "telugu": "Telugu", "tollywood": "Telugu",
            "malayalam": "Malayalam", "mollywood": "Malayalam",
            "kannada": "Kannada", "sandalwood": "Kannada",
            "marathi": "Marathi", "bengali": "Bengali", "punjabi": "Punjabi", "gujarati": "Gujarati",
            "korean": "Korean", "kdrama": "Korean", "k-drama": "Korean",
            "japanese": "Japanese", "anime": "Japanese",
            "spanish": "Spanish", "french": "French", "german": "German",
            "english": "English", "hollywood": "English"
        }
        
        self.moods_map = {
            "mind-bending": "Mind-bending", "mind bending": "Mind-bending", "trippy": "Mind-bending", "cerebral": "Cerebral",
            "dark": "Dark", "gritty": "Gritty", "bleak": "Bleak", "disturbing": "Disturbing", "chilling": "Chilling",
            "heartwarming": "Heartwarming", "wholesome": "Wholesome", "feel-good": "Feel-Good", "feel good": "Feel-Good",
            "uplifting": "Uplifting", "sweet": "Sweet", "comforting": "Comforting",
            "intense": "Intense", "fast-paced": "Fast-Paced", "adrenaline": "Adrenaline", "explosive": "Explosive",
            "emotional": "Emotional", "tearjerker": "Emotional", "sad": "Emotional", "bittersweet": "Bittersweet",
            "witty": "Witty", "clever": "Clever", "satirical": "Satirical", "quirky": "Quirky",
            "epic": "Epic", "visually stunning": "Visually Stunning", "atmospheric": "Atmospheric",
            "inspirational": "Inspirational", "patriotic": "Patriotic"
        }
        
        self.known_directors = [
            "Christopher Nolan", "David Fincher", "Denis Villeneuve", "Martin Scorsese",
            "Damien Chazelle", "Bong Joon Ho", "Hayao Miyazaki", "Quentin Tarantino",
            "Rajkumar Hirani", "Nitesh Tiwari", "Zoya Akhtar", "Sriram Raghavan", "Nishikant Kamat",
            "Ashutosh Gowariker", "S.S. Rajamouli", "Sukumar", "Rishab Shetty", "Prashanth Neel",
            "Lokesh Kanagaraj", "Nelson Dilipkumar", "Nagraj Manjule", "Satyajit Ray", "Hansal Mehta",
            "Anurag Kashyap", "Farhan Akhtar", "Aamir Khan", "Vince Gilligan", "The Duffer Brothers",
            "Imtiaz Ali", "Ayan Mukerji", "Shoojit Sircar", "Vidhu Vinod Chopra"
        ]
        
        self.known_actors = [
            "Aamir Khan", "Shah Rukh Khan", "Salman Khan", "Ranbir Kapoor", "Ranveer Singh",
            "Hrithik Roshan", "Ajay Devgn", "Ayushmann Khurrana", "Rajkummar Rao", "Pankaj Tripathi",
            "Nawazuddin Siddiqui", "Manoj Bajpayee", "Vicky Kaushal", "Prabhas", "Allu Arjun",
            "Ram Charan", "N.T. Rama Rao Jr.", "Yash", "Rishab Shetty", "Kamal Haasan",
            "Rajinikanth", "Vijay", "Vijay Sethupathi", "Fahadh Faasil", "Dulquer Salmaan",
            "Nivin Pauly", "Soubin Shahir", "Nana Patekar", "Deepika Padukone", "Alia Bhatt",
            "Kareena Kapoor", "Tabu", "Kangana Ranaut", "Katrina Kaif", "Kiara Advani",
            "Shraddha Kapoor", "Leonardo DiCaprio", "Christian Bale", "Matthew McConaughey",
            "Cillian Murphy", "Brad Pitt", "Tom Hanks", "Al Pacino", "Marlon Brando", "Keanu Reeves",
            "Bryan Cranston", "Bob Odenkirk", "Song Kang-ho", "Millie Bobby Brown", "Jitendra Kumar"
        ]

    def extract_entities(self, text: str) -> Dict[str, Any]:
        """Extracts genres, languages, moods, actors, directors, eras, and mentioned titles from natural query."""
        text_lower = text.lower()
        entities = {
            "genres": [],
            "languages": [],
            "moods": [],
            "directors": [],
            "actors": [],
            "type": None,
            "era": None,
            "mentioned_titles": []
        }

        # Match genres
        for token, genre_name in self.genres_map.items():
            if re.search(r'\b' + re.escape(token) + r'\b', text_lower):
                if genre_name not in entities["genres"]:
                    entities["genres"].append(genre_name)

        # Match languages / industries
        for token, lang_name in self.languages_map.items():
            if re.search(r'\b' + re.escape(token) + r'\b', text_lower):
                if lang_name not in entities["languages"]:
                    entities["languages"].append(lang_name)

        # Match moods
        for token, mood_name in self.moods_map.items():
            if re.search(r'\b' + re.escape(token) + r'\b', text_lower):
                if mood_name not in entities["moods"]:
                    entities["moods"].append(mood_name)

        # Match directors
        for director in self.known_directors:
            if director.lower() in text_lower or director.split()[-1].lower() in text_lower.split():
                entities["directors"].append(director)

        # Match actors
        for actor in self.known_actors:
            if actor.lower() in text_lower or actor.split()[-1].lower() in text_lower.split():
                entities["actors"].append(actor)

        # Match exact 4-digit year (e.g. 2020, 2024, 1994, 1820)
        year_match = re.search(r'\b(1[89]\d{2}|20\d{2})\b', text)
        if year_match:
            exact_yr = int(year_match.group(1))
            entities["exact_year"] = exact_yr
            entities["era"] = (exact_yr, exact_yr)
        else:
            entities["exact_year"] = None

        # Content type
        if any(w in text_lower for w in ["tv show", "tv series", "series", "show", "seasons", "shows"]):
            entities["type"] = "TV Show"
        elif any(w in text_lower for w in ["movie", "film", "movies", "films", "cinema"]):
            entities["type"] = "Movie"

        # Era / Decade
        if any(w in text_lower for w in ["90s", "1990s", "nineties"]):
            entities["era"] = (1990, 1999)
        elif any(w in text_lower for w in ["80s", "1980s", "eighties"]):
            entities["era"] = (1980, 1989)
        elif any(w in text_lower for w in ["2000s", "00s"]):
            entities["era"] = (2000, 2009)
        elif any(w in text_lower for w in ["2010s", "tens"]):
            entities["era"] = (2010, 2019)
        elif any(w in text_lower for w in ["recent", "latest", "2020s", "new"]) and not entities.get("exact_year"):
            entities["era"] = (2020, 2026)

        # Check for known movie titles in the prompt
        for movie in self.recommender.movies:
            title = movie["title"].lower()
            if len(title) > 3 and re.search(r'\b' + re.escape(title) + r'\b', text_lower):
                entities["mentioned_titles"].append(movie)

        return entities

    def classify_intent(self, text: str, entities: Dict[str, Any]) -> str:
        """Classifies high-level conversational intent."""
        text_lower = text.lower().strip()
        
        # Greetings & General
        if any(text_lower.startswith(g) for g in ["hi", "hello", "hey", "hola", "sup", "greetings"]):
            if len(text_lower.split()) <= 3:
                return "GREETING"
                
        if any(w in text_lower for w in ["how do you work", "help", "what can you do", "who are you"]):
            return "HELP"

        # Profile / History based
        if any(phrase in text_lower for phrase in ["my taste", "my profile", "based on my history", "what should i watch", "recommend for me"]):
            return "PROFILE_RECOMMEND"

        # Similarity to specific movie
        if any(phrase in text_lower for phrase in ["like ", "similar to", "if i liked", "loved ", "same as", "reminds me of"]) or entities["mentioned_titles"]:
            return "SIMILARITY"

        # Director / Actor lookup
        if entities["directors"] or entities["actors"]:
            return "PERSON_BASED"

        # Mood / Genre / Semantic query
        if entities["moods"] or entities["genres"] or entities.get("era") or entities.get("exact_year") or entities.get("languages"):
            return "FILTER_AND_MOOD"

        return "SEMANTIC_SEARCH"

    def get_guided_recommendations(
        self,
        preferences: Dict[str, Any],
        user_profile: Dict[str, Any],
        top_n: int = 8
    ) -> Dict[str, Any]:
        """
        Executes strict multi-criteria filtering for CineBot interactive recommendation flow.
        Applies Language, Cinema, Genre(s), Exact Year / Era, Type, and Duration filters,
        then ranks using user preference vector / TF-IDF similarity.
        """
        pref_lang = (preferences.get("language") or "").strip()
        pref_cinema = (preferences.get("cinema") or "").strip()
        pref_genres = preferences.get("genres") or []
        if isinstance(pref_genres, str):
            pref_genres = [pref_genres]
        pref_year = preferences.get("year")
        pref_type = (preferences.get("type") or "").strip()
        pref_duration = (preferences.get("duration") or "").strip()

        candidates = list(self.recommender.movies)

        # 1. Exact Year / Year Filter
        exact_year = None
        if pref_year is not None:
            yr_str = str(pref_year).strip().lower()
            if yr_str not in ["all", "any", "any year", ""]:
                if yr_str == "latest releases":
                    candidates = [m for m in candidates if (m.get("releaseYear") or m.get("release_year") or 0) >= 2023]
                elif yr_str in ["2000s", "00s"]:
                    candidates = [m for m in candidates if 2000 <= (m.get("releaseYear") or m.get("release_year") or 0) <= 2009]
                elif yr_str in ["1990s", "90s"]:
                    candidates = [m for m in candidates if 1990 <= (m.get("releaseYear") or m.get("release_year") or 0) <= 1999]
                elif yr_str in ["1980s", "80s"]:
                    candidates = [m for m in candidates if 1980 <= (m.get("releaseYear") or m.get("release_year") or 0) <= 1989]
                else:
                    # Parse as exact integer (supports numbers or string years like "2020", "1820")
                    match = re.search(r'\b(1[89]\d{2}|20\d{2})\b', yr_str)
                    if yr_str.isdigit():
                        exact_year = int(yr_str)
                    elif match:
                        exact_year = int(match.group(1))

                    if exact_year is not None:
                        candidates = [m for m in candidates if (m.get("releaseYear") or m.get("release_year") or 0) == exact_year]
                        if not candidates:
                            # Exact year rule: do not silently remove year filter
                            return {
                                "success": False,
                                "not_found_year": True,
                                "year": exact_year,
                                "response": f"Sorry, no matching titles are available for **{exact_year}**.\n\nNot available for this year.",
                                "movies": [],
                                "fallback_options": ["Try Nearby Years", "Choose Another Year", "Any Year"]
                            }

        # 2. Language Filter
        if pref_lang and pref_lang.lower() not in ["all", "all languages", "any"]:
            candidates = [
                m for m in candidates
                if m.get("language", "").lower() == pref_lang.lower()
                or pref_lang.lower() in m.get("language", "").lower()
            ]

        # 3. Cinema / Industry Filter
        if pref_cinema and pref_cinema.lower() not in ["all", "all cinema", "any"]:
            clean_cinema = pref_cinema.lower().replace(" cinema", "").strip()
            if clean_cinema in ["south indian", "south india", "south"]:
                candidates = [
                    m for m in candidates
                    if m.get("language", "").lower() in ["tamil", "telugu", "malayalam", "kannada"]
                    or any(s in m.get("industry", "").lower() for s in ["kollywood", "tollywood", "mollywood", "sandalwood", "tamil", "telugu", "malayalam", "kannada", "south"])
                ]
            elif clean_cinema in ["international", "world"]:
                candidates = [
                    m for m in candidates
                    if m.get("language", "").lower() not in ["hindi", "marathi", "tamil", "telugu", "malayalam", "kannada", "bengali", "punjabi", "gujarati"]
                    or m.get("country", "").lower() not in ["india"]
                ]
            elif clean_cinema == "marathi":
                candidates = [
                    m for m in candidates
                    if m.get("language", "").lower() == "marathi" or "marathi" in m.get("industry", "").lower()
                ]
            elif clean_cinema in ["bollywood", "hindi"]:
                candidates = [
                    m for m in candidates
                    if m.get("language", "").lower() == "hindi" or "bollywood" in m.get("industry", "").lower()
                ]
            elif clean_cinema in ["hollywood", "english"]:
                candidates = [
                    m for m in candidates
                    if m.get("language", "").lower() == "english" or "hollywood" in m.get("industry", "").lower() or m.get("country", "").lower() in ["united states", "usa", "united kingdom", "uk"]
                ]
            elif clean_cinema in ["korean", "korea"]:
                candidates = [
                    m for m in candidates
                    if m.get("language", "").lower() == "korean" or "korean" in m.get("industry", "").lower() or "korea" in m.get("country", "").lower()
                ]
            elif clean_cinema in ["japanese", "japan"]:
                candidates = [
                    m for m in candidates
                    if m.get("language", "").lower() == "japanese" or "japanese" in m.get("industry", "").lower() or "japan" in m.get("country", "").lower()
                ]
            else:
                candidates = [
                    m for m in candidates
                    if clean_cinema in m.get("industry", "").lower()
                    or clean_cinema in m.get("language", "").lower()
                    or clean_cinema in m.get("country", "").lower()
                ]

        # 4. Content Type Filter
        if pref_type and pref_type.lower() not in ["both", "all", "any", ""]:
            if "movie" in pref_type.lower():
                candidates = [m for m in candidates if m.get("type", "").lower() == "movie"]
            elif "tv" in pref_type.lower() or "series" in pref_type.lower():
                candidates = [m for m in candidates if m.get("type", "").lower() == "tv show"]

        # 5. Genre Filter (supports multiple genres or single)
        clean_genres = [g for g in pref_genres if g.lower() not in ["any", "any genre", "all", ""]]
        if clean_genres:
            # Score each candidate by number of genre matches
            def genre_match_score(m):
                m_genres = [g.lower() for g in m.get("genres", [])] + [t.lower() for t in m.get("mood_tags", [])]
                return sum(1 for target in clean_genres if target.lower() in m_genres)

            # Filter candidates that have at least one matching genre
            candidates_with_genre = [m for m in candidates if genre_match_score(m) > 0]
            if candidates_with_genre:
                candidates = candidates_with_genre

        # 6. Duration Filter
        if pref_duration and pref_duration.lower() not in ["any", "any duration", "all", ""]:
            dur_lower = pref_duration.lower()
            def passes_duration(m):
                d_str = str(m.get("duration", "")).lower()
                # Parse minutes
                min_match = re.search(r'(\d+)\s*min', d_str)
                minutes = int(min_match.group(1)) if min_match else None
                
                if "under 90" in dur_lower:
                    return minutes is not None and minutes < 90
                elif "90" in dur_lower and "120" in dur_lower:
                    return minutes is not None and 90 <= minutes <= 120
                elif "120" in dur_lower and "150" in dur_lower:
                    return minutes is not None and 120 <= minutes <= 150
                elif "150" in dur_lower:
                    return minutes is not None and minutes >= 150
                elif "tv series" in dur_lower or "series" in dur_lower:
                    return m.get("type", "").lower() == "tv show" or "season" in d_str
                return True

            dur_filtered = [m for m in candidates if passes_duration(m)]
            if dur_filtered:
                candidates = dur_filtered

        if not candidates:
            # Fallback if other combinations yield 0
            return {
                "success": False,
                "not_found_year": False,
                "response": "Sorry, no exact titles matched all combined criteria. Try broadening your preferences or choosing another genre!",
                "movies": [],
                "fallback_options": ["Any Genre", "Any Year", "Reset Preferences"]
            }

        # 7. Rank filtered candidates using user preference vector / similarity & IMDb
        user_vector = self.recommender.build_user_preference_vector(user_profile)
        scored_candidates = []

        for m in candidates:
            m_id = m["id"]
            content_sim = 0.5
            if user_vector is not None and m_id in self.recommender.id_to_idx:
                idx = self.recommender.id_to_idx[m_id]
                content_sim = float(self.recommender.tfidf_matrix[idx].dot(user_vector))

            imdb_score = float(m.get("imdb_score", 7.0))
            imdb_factor = imdb_score / 10.0
            
            # Combine ranking score
            rank_score = (content_sim * 0.45) + (imdb_factor * 0.55)
            match_pct = int(min(99, max(76, int((rank_score) * 100) + 15)))

            m_copy = dict(m)
            m_copy["match_score"] = match_pct
            
            # Formulate dynamic rationale
            genres_label = ", ".join(m.get("genres", [])[:2])
            mood_label = m.get("mood_tags", ["Acclaimed"])[0]
            m_copy["explanation"] = f"{mood_label} {m.get('language', '')} {genres_label} title rated ⭐ {imdb_score} on IMDb."
            
            scored_candidates.append((rank_score, m_copy))

        scored_candidates.sort(key=lambda x: x[0], reverse=True)
        top_movies = [item[1] for item in scored_candidates[:top_n]]

        # Build response message
        pref_summary_parts = []
        if pref_lang and pref_lang.lower() not in ["all", "all languages", "any"]:
            pref_summary_parts.append(pref_lang)
        if pref_cinema and pref_cinema.lower() not in ["all", "all cinema", "any"]:
            pref_summary_parts.append(pref_cinema)
        if clean_genres:
            pref_summary_parts.append("/".join(clean_genres))
        if pref_year and str(pref_year).lower() not in ["all", "any", "any year", ""]:
            pref_summary_parts.append(str(pref_year))

        tag_summary = " • ".join(pref_summary_parts) if pref_summary_parts else "your selected preferences"
        response_text = f"🍿 Here are the top Netflix picks curated for **{tag_summary}**:"

        return {
            "success": True,
            "not_found_year": False,
            "response": response_text,
            "movies": top_movies,
            "total_found": len(scored_candidates)
        }

    def process_message(
        self,
        message: str,
        user_profile: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Main dialogue processing pipeline:
        Takes user prompt, parses intent + entities, queries recommender, and builds AI response.
        """
        entities = self.extract_entities(message)
        intent = self.classify_intent(message, entities)
        
        # Multi-turn memory carryover if current message is a short refinement
        if context and len(message.split()) <= 5:
            if not entities["genres"] and context.get("genres"):
                entities["genres"] = context["genres"]
            if not entities["type"] and context.get("type"):
                entities["type"] = context["type"]

        response_text = ""
        recommended_movies: List[Dict[str, Any]] = []
        suggestions: List[str] = []

        if intent == "GREETING":
            response_text = (
                "👋 Hey there! I'm **CineBot**, your personal Netflix AI Curator.\n\n"
                "Tell me what you're in the mood for, your favorite titles, or ask me for a recommendation! "
                "For example:\n"
                "• *'I want a mind-bending sci-fi movie with plot twists'*\n"
                "• *'Recommend something like Stranger Things and Dark'*\n"
                "• *'Give me feel-good comedy series for a cozy night'*"
            )
            suggestions = [
                "🧠 Mind-Bending Sci-Fi",
                "🔍 Gritty Crime Thrillers",
                "🍿 Feel-Good Comedies",
                "🔥 Action Blockbusters"
            ]

        elif intent == "HELP":
            response_text = (
                "🎯 **Here's what I can do for you:**\n\n"
                "1. **Personalized Taste Matching**: Analyze your watch history & star ratings to find hidden Netflix gems.\n"
                "2. **Mood & Vibe Search**: Search by tone (*'dark'*, *'heartwarming'*, *'nail-biting'*, *'whimsical'*).\n"
                "3. **Similarity Engine**: Ask for titles similar to your favorites (*'like Inception and Shutter Island'*).\n"
                "4. **Cast & Director Match**: Explore films by Christopher Nolan, Denis Villeneuve, David Fincher, etc."
            )
            suggestions = [
                "What should I watch today?",
                "Films like Inception",
                "Best 90s Thrillers",
                "Show top rated anime"
            ]

        elif intent == "PROFILE_RECOMMEND":
            recs = self.recommender.recommend_for_user(user_profile, top_n=6)
            watched_count = len(user_profile.get("watch_history", []))
            ratings_count = len(user_profile.get("ratings", {}))
            
            if watched_count > 0 or ratings_count > 0:
                response_text = (
                    f"🎬 Based on your taste profile ({watched_count} watched titles, {ratings_count} ratings), "
                    f"here are the highest match-rate films curated specifically for you on Netflix:"
                )
            else:
                response_text = (
                    "✨ Since your profile is brand new, here are top-tier Netflix crowd favorites and critical masterpieces to start your journey!"
                )
            recommended_movies = recs
            suggestions = [
                "Only show Movies",
                "Only show TV Series",
                "Something darker",
                "Something funny"
            ]

        elif intent == "SIMILARITY":
            mentioned = entities["mentioned_titles"]
            if mentioned:
                target = mentioned[0]
                recs = self.recommender.get_similar_movies(target["id"], top_n=5)
                response_text = (
                    f"🔮 If you enjoyed **{target['title']}** ({target['genres'][0]}, {target.get('releaseYear') or target.get('release_year')}), "
                    f"you'll definitely love these Netflix titles that share its {target['mood_tags'][0].lower()} atmosphere and narrative style:"
                )
                recommended_movies = recs
            else:
                # Semantic search for similarity query
                cleaned_query = re.sub(r'(like|similar to|same as|if i liked|loved)', '', message, flags=re.IGNORECASE).strip()
                recs = self.recommender.search_movies(cleaned_query, top_n=5)
                response_text = f"✨ Here are the closest Netflix titles matching the vibe of **'{cleaned_query}'**:"
                recommended_movies = recs
            
            suggestions = [
                "Show more like this",
                "Something with more action",
                "Different genre please"
            ]

        elif intent == "PERSON_BASED":
            person = (entities["directors"] + entities["actors"])[0]
            # Search by person
            results = []
            for m in self.recommender.movies:
                directors = m.get("director", "")
                cast = m.get("cast", [])
                if person.lower() in directors.lower() or any(person.lower() in c.lower() for c in cast):
                    m_copy = dict(m)
                    m_copy["match_score"] = 95
                    m_copy["explanation"] = f"Features work by {person}."
                    results.append(m_copy)
            
            if results:
                response_text = f"🌟 Found **{len(results)}** Netflix titles connected to **{person}**:"
                recommended_movies = results[:6]
            else:
                recs = self.recommender.search_movies(person, top_n=5)
                response_text = f"🔍 Here are top matching titles for **{person}** on Netflix:"
                recommended_movies = recs
            
            suggestions = [
                "Top Christopher Nolan films",
                "Denis Villeneuve movies",
                "David Fincher thrillers"
            ]

        else: # FILTER_AND_MOOD / SEMANTIC_SEARCH
            # Filter & Semantic Blend
            genre_filter = entities["genres"][0] if entities["genres"] else None
            lang_filter = entities["languages"][0] if entities.get("languages") else None
            type_filter = entities["type"] if entities["type"] else None
            exact_year = entities.get("exact_year")
            
            # Start with semantic search
            search_recs = self.recommender.search_movies(message, top_n=30)
            
            # Apply language/industry filter if present
            if lang_filter:
                search_recs = [m for m in search_recs if m.get("language", "").lower() == lang_filter.lower() or m.get("industry", "").lower() == lang_filter.lower()]
                if not search_recs:
                    search_recs = [m for m in self.recommender.movies if m.get("language", "").lower() == lang_filter.lower() or m.get("industry", "").lower() == lang_filter.lower()]

            # Apply exact year filter if present (Rule 19)
            if exact_year:
                search_recs = [m for m in search_recs if (m.get("releaseYear") or m.get("release_year") or 0) == exact_year]
                if not search_recs:
                    # Also check entire catalog for exact year
                    search_recs = [m for m in self.recommender.movies if (m.get("releaseYear") or m.get("release_year") or 0) == exact_year]
                    if lang_filter:
                        search_recs = [m for m in search_recs if m.get("language", "").lower() == lang_filter.lower()]
                    if genre_filter:
                        search_recs = [m for m in search_recs if genre_filter.lower() in [g.lower() for g in m.get("genres", [])]]
            elif entities.get("era"):
                start_yr, end_yr = entities["era"]
                search_recs = [m for m in search_recs if start_yr <= (m.get("releaseYear") or m.get("release_year") or 2000) <= end_yr]
            
            # Apply type filter if present
            if type_filter:
                search_recs = [m for m in search_recs if m.get("type", "").lower() == type_filter.lower()]
                
            # Apply genre filter if present
            if genre_filter:
                search_recs = [m for m in search_recs if genre_filter.lower() in [g.lower() for g in m.get("genres", [])]]

            if exact_year and not search_recs:
                response_text = f"Sorry, no matching titles are available for **{exact_year}**.\n\nNot available for this year."
                suggestions = [
                    "Try Nearby Years",
                    "Choose Another Year",
                    "Any Year"
                ]
                return {
                    "response": response_text,
                    "movies": [],
                    "suggestions": suggestions,
                    "not_found_year": True,
                    "year": exact_year,
                    "detected_entities": entities,
                    "intent": intent,
                    "updated_context": {
                        "genres": entities["genres"],
                        "type": entities["type"],
                        "last_intent": intent
                    }
                }

            if not search_recs:
                # Fallback to general search without strict filter
                search_recs = self.recommender.search_movies(message, top_n=6)

            tags_str = ", ".join(entities["languages"] + entities["moods"] + entities["genres"])
            if exact_year:
                tags_str = f"{tags_str} ({exact_year})" if tags_str else str(exact_year)

            if tags_str:
                response_text = f"🍿 Here are the best Netflix recommendations tuned for **{tags_str}**:"
            else:
                response_text = f"🍿 Here are the top Netflix picks matching your request:"

            # Add match score & explanation
            for m in search_recs:
                if "match_score" not in m:
                    m["match_score"] = int(min(98, max(75, 75 + float(m.get("imdb_score", 7.0)) * 2.5)))
                if "explanation" not in m:
                    mood_desc = m["mood_tags"][0] if m.get("mood_tags") else "Thrilling"
                    m["explanation"] = f"{mood_desc} {m['genres'][0]} title with a {m.get('imdb_score', 8.0)} IMDb score."
            
            recommended_movies = search_recs[:6]
            suggestions = [
                "Show only high IMDb scores",
                "Something more lighthearted",
                "Give me TV series instead"
            ]

        return {
            "response": response_text,
            "movies": recommended_movies,
            "suggestions": suggestions,
            "detected_entities": entities,
            "intent": intent,
            "updated_context": {
                "genres": entities["genres"],
                "type": entities["type"],
                "last_intent": intent
            }
        }
