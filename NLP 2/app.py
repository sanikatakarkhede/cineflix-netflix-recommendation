"""
Flask Web Application for CineFlix AI.
Provides RESTful APIs for Netflix catalog browsing, hybrid recommendation generation,
CineBot conversational chat, user authentication, and interactive taste profile tracking.
"""

import os
import sys
import copy
import json
from typing import Optional, Dict, Any, List, Tuple
from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS

from engine.recommender import MovieRecommender, PERSONA_PROFILES
from engine.nlp_chat import CineBot
from engine.auth import UserManager
from engine.tmdb_client import TMDBClient

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

app = Flask(__name__)
app.secret_key = "cineflix-ai-netflix-secret-key-2026"
CORS(app)

# Initialize NLP, Recommender Engine, TMDB Client, and User Authentication Manager
recommender = MovieRecommender("data/netflix_catalog.json")
cinebot = CineBot(recommender)
user_manager = UserManager("data/users.json")
tmdb_client = TMDBClient()


def get_current_user_id() -> Optional[str]:
    """Returns authenticated user_id from session or None."""
    return session.get("user_id")


def get_current_profile() -> dict:
    """Retrieves active profile for recommendations and stats."""
    user_id = get_current_user_id()
    if user_id:
        return user_manager.get_user_profile(user_id)
    
    # Guest session fallback
    guest_session_id = session.get("guest_id", "guest_default")
    if "guest_profile" not in session:
        session["guest_profile"] = copy.deepcopy(PERSONA_PROFILES["clean_slate"])
    return session["guest_profile"]


def calculate_profile_stats(profile: dict) -> dict:
    """Computes genre distribution, mood counts, and favorite actors for visualization."""
    genre_counts = {}
    mood_counts = {}
    actor_counts = {}
    
    ratings = profile.get("ratings", {})
    watch_history = profile.get("watch_history", [])
    
    all_watched_ids = list(set(watch_history + list(ratings.keys())))
    watched_movies = []
    
    for m_id in all_watched_ids:
        movie = recommender.get_movie_by_id(m_id)
        if movie:
            m_data = dict(movie)
            m_data["user_rating"] = ratings.get(m_id, None)
            watched_movies.append(m_data)
            
            # Count genres
            for g in movie.get("genres", []):
                genre_counts[g] = genre_counts.get(g, 0) + 1
            # Count moods
            for m in movie.get("mood_tags", []):
                mood_counts[m] = mood_counts.get(m, 0) + 1
            # Count cast
            for c in movie.get("cast", [])[:2]:
                actor_counts[c] = actor_counts.get(c, 0) + 1

    total_genres = sum(genre_counts.values()) or 1
    genre_dist = [{"genre": g, "count": c, "pct": round((c / total_genres) * 100, 1)} 
                  for g, c in sorted(genre_counts.items(), key=lambda x: x[1], reverse=True)[:6]]

    top_moods = [{"mood": m, "count": c} 
                 for m, c in sorted(mood_counts.items(), key=lambda x: x[1], reverse=True)[:6]]

    top_actors = [{"actor": a, "count": c} 
                  for a, c in sorted(actor_counts.items(), key=lambda x: x[1], reverse=True)[:5]]

    has_history = len(ratings) > 0 or len(watch_history) > 0

    return {
        "has_history": has_history,
        "watched_count": len(watched_movies),
        "rated_count": len(ratings),
        "watched_movies": watched_movies,
        "genre_distribution": genre_dist,
        "top_moods": top_moods,
        "top_actors": top_actors,
        "sliders": profile.get("sliders", {"action_level": 50, "dark_tone": 50, "plot_depth": 50})
    }


# ==========================================
# Core Web Routes
# ==========================================

@app.route("/")
def index():
    return render_template("index.html")


# ==========================================
# Authentication REST API Endpoints
# ==========================================

@app.route("/api/auth/signup", methods=["POST"])
def auth_signup():
    """Register a new user account."""
    data = request.json or {}
    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    password = data.get("password", "")
    avatar = data.get("avatar", "👤")

    success, message, user_data = user_manager.create_user(
        name=name,
        email=email,
        password=password,
        avatar=avatar
    )

    if not success:
        return jsonify({"success": False, "error": message}), 400

    # Auto login on successful signup
    session["user_id"] = user_data["id"]
    return jsonify({
        "success": True,
        "message": message,
        "user": user_data
    })


@app.route("/api/auth/login", methods=["POST"])
def auth_login():
    """Authenticate existing user credentials."""
    data = request.json or {}
    email = data.get("email", "").strip()
    password = data.get("password", "")

    success, message, user_data = user_manager.authenticate_user(email, password)
    if not success:
        return jsonify({"success": False, "error": message}), 401

    session["user_id"] = user_data["id"]
    return jsonify({
        "success": True,
        "message": message,
        "user": user_data
    })


@app.route("/api/auth/logout", methods=["POST"])
def auth_logout():
    """Clear active user session."""
    session.pop("user_id", None)
    session["guest_profile"] = copy.deepcopy(PERSONA_PROFILES["clean_slate"])
    return jsonify({
        "success": True,
        "message": "Logged out successfully."
    })


@app.route("/api/auth/me", methods=["GET"])
def auth_me():
    """Check current authentication status and user details."""
    user_id = get_current_user_id()
    if user_id:
        safe_user = user_manager.get_safe_user(user_id)
        if safe_user:
            profile = user_manager.get_user_profile(user_id)
            stats = calculate_profile_stats(profile)
            return jsonify({
                "authenticated": True,
                "user": safe_user,
                "profile": profile,
                "stats": stats
            })

    # Unauthenticated / Guest state
    guest_profile = get_current_profile()
    stats = calculate_profile_stats(guest_profile)
    return jsonify({
        "authenticated": False,
        "user": None,
        "profile": guest_profile,
        "stats": stats
    })


@app.route("/api/auth/update-profile", methods=["POST"])
def auth_update_profile():
    """Update user account settings (name, avatar, bio)."""
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({"error": "Authentication required"}), 401

    data = request.json or {}
    success = user_manager.update_user_profile(user_id, data)
    if not success:
        return jsonify({"error": "Failed to update profile"}), 400

    safe_user = user_manager.get_safe_user(user_id)
    return jsonify({
        "success": True,
        "message": "Profile updated successfully.",
        "user": safe_user
    })


@app.route("/api/auth/forgot-password", methods=["POST"])
def auth_forgot_password():
    """Handle password reset request simulation."""
    data = request.json or {}
    email = data.get("email", "").strip().lower()
    if not email or "@" not in email:
        return jsonify({"error": "Please provide a valid email address."}), 400

    return jsonify({
        "success": True,
        "message": f"If an account exists for {email}, a password reset link has been dispatched."
    })


# ==========================================
# Movie Catalog & Details API
# ==========================================

@app.route("/api/movies", methods=["GET"])
def get_movies():
    """Browse catalog with search, filter, and pagination."""
    query = request.args.get("search", "").strip()
    genre = request.args.get("genre", "All")
    language = request.args.get("language", "All")
    country = request.args.get("country", "All")
    industry = request.args.get("industry", "All")
    type_filter = request.args.get("type", "All")
    sort_by = request.args.get("sort", "default")
    limit = int(request.args.get("limit", 100))
    offset = int(request.args.get("offset", 0))

    if query:
        movies = recommender.search_movies(query, top_n=150)
    else:
        movies = list(recommender.movies)

    # Filter by genre
    if genre and genre.lower() != "all":
        movies = [m for m in movies if genre.lower() in [g.lower() for g in m.get("genres", [])]]

    # Filter by language
    if language and language.lower() != "all":
        movies = [m for m in movies if m.get("language", "").lower() == language.lower()]

    # Filter by country
    if country and country.lower() != "all":
        movies = [m for m in movies if m.get("country", "").lower() == country.lower() or m.get("industry", "").lower() == country.lower()]

    # Filter by industry
    if industry and industry.lower() != "all":
        movies = [m for m in movies if m.get("industry", "").lower() == industry.lower()]

    # Filter by type
    if type_filter and type_filter.lower() != "all":
        movies = [m for m in movies if m.get("type", "").lower() == type_filter.lower()]

    # Sort
    if sort_by == "imdb":
        movies.sort(key=lambda x: x.get("imdb_score", 0), reverse=True)
    elif sort_by == "year":
        movies.sort(key=lambda x: x.get("releaseYear", x.get("release_year", 0)), reverse=True)
    elif sort_by == "title":
        movies.sort(key=lambda x: x.get("title", ""))

    total = len(movies)
    paginated = movies[offset:offset + limit]

    # Collect available facets dynamically
    all_genres = sorted(list(set(g for m in recommender.movies for g in m.get("genres", []))))
    all_languages = sorted(list(set(m.get("language") for m in recommender.movies if m.get("language"))))
    all_countries = sorted(list(set(m.get("country") for m in recommender.movies if m.get("country"))))
    all_industries = sorted(list(set(m.get("industry") for m in recommender.movies if m.get("industry"))))
    all_moods = sorted(list(set(t for m in recommender.movies for t in m.get("mood_tags", []))))

    return jsonify({
        "movies": paginated,
        "total": total,
        "genres": all_genres,
        "languages": all_languages,
        "countries": all_countries,
        "industries": all_industries,
        "mood_tags": all_moods
    })


@app.route("/api/movie/<movie_id>", methods=["GET"])
def get_movie_detail(movie_id):
    """Retrieve single movie details and similar titles."""
    movie = recommender.get_movie_by_id(movie_id)
    if not movie:
        return jsonify({"error": "Movie not found"}), 404
    
    similar = recommender.get_similar_movies(movie_id, top_n=6)
    return jsonify({
        "movie": movie,
        "similar_movies": similar
    })


@app.route("/api/tmdb/search", methods=["GET"])
def tmdb_search_proxy():
    """Proxy search to TMDB API if configured."""
    q = request.args.get("query", "").strip()
    if not q:
        return jsonify({"results": []})
    results = tmdb_client.search_multi(q)
    return jsonify({"results": results})


@app.route("/api/tmdb/providers/<media_type>/<int:tmdb_id>", methods=["GET"])
def tmdb_providers_proxy(media_type, tmdb_id):
    """Retrieve watch provider availability for region IN from TMDB."""
    providers = tmdb_client.get_watch_providers(media_type, tmdb_id, region="IN")
    is_netflix = tmdb_client.is_netflix_available_in_india(media_type, tmdb_id)
    return jsonify({
        "tmdbId": tmdb_id,
        "mediaType": media_type,
        "region": "IN",
        "providers": providers,
        "netflixAvailable": is_netflix
    })


# ==========================================
# Recommendations & AI Explanation API
# ==========================================

@app.route("/api/recommendations", methods=["POST"])
def get_recommendations():
    """Generates personalized AI recommendations based on active user preference profile."""
    profile = get_current_profile()
    data = request.json or {}
    genre_filter = data.get("genre")
    type_filter = data.get("type")
    top_n = int(data.get("top_n", 12))

    recs = recommender.recommend_for_user(
        user_profile=profile,
        top_n=top_n,
        genre_filter=genre_filter,
        type_filter=type_filter
    )
    
    stats = calculate_profile_stats(profile)
    has_history = stats["has_history"]

    # If cold start (no history), adjust recommendation labels so we don't display fake 98% personalized matches
    if not has_history:
        for r in recs:
            r["is_cold_start"] = True
            r["match_score"] = int(min(96, max(75, int(float(r.get("imdb_score", 7.5)) * 10) + 5)))
            r["explanation"] = f"Top-rated Netflix title with {r.get('imdb_score', 8.0)} IMDb score and standout {r['genres'][0]} acclaim."

    # Also generate "Because you watched" row if there is a top rated movie
    because_you_watched = None
    if profile.get("ratings"):
        top_m_id = max(profile["ratings"].items(), key=lambda x: x[1])[0]
        fav_movie = recommender.get_movie_by_id(top_m_id)
        if fav_movie:
            sims = recommender.get_similar_movies(top_m_id, top_n=6)
            because_you_watched = {
                "source_movie": fav_movie,
                "recommendations": sims
            }

    user_id = get_current_user_id()
    safe_user = user_manager.get_safe_user(user_id) if user_id else None

    return jsonify({
        "is_cold_start": not has_history,
        "recommendations": recs,
        "because_you_watched": because_you_watched,
        "user_profile": {
            "id": profile.get("id"),
            "name": safe_user["name"] if safe_user else profile.get("name", "Guest"),
            "avatar": safe_user["avatar"] if safe_user else profile.get("avatar", "👤"),
            "stats": stats
        }
    })


# ==========================================
# Conversational CineBot Dialogue API
# ==========================================

@app.route("/api/chat", methods=["POST"])
def chat():
    """Conversational NLP dialogue endpoint with active user profile context."""
    profile = get_current_profile()
    data = request.json or {}
    preferences = data.get("preferences")

    if preferences:
        # Guided preference flow
        result = cinebot.get_guided_recommendations(
            preferences=preferences,
            user_profile=profile
        )
        return jsonify(result)

    message = data.get("message", "").strip()
    context = data.get("context", {})

    if not message:
        return jsonify({"error": "Message or preferences is required"}), 400

    chat_result = cinebot.process_message(
        message=message,
        user_profile=profile,
        context=context
    )
    
    return jsonify(chat_result)


@app.route("/api/chat/recommend", methods=["POST"])
def chat_guided_recommend():
    """Endpoint to get recommendations based on CineBot structured guided preferences."""
    profile = get_current_profile()
    data = request.json or {}
    preferences = data.get("preferences", data)

    result = cinebot.get_guided_recommendations(
        preferences=preferences,
        user_profile=profile
    )
    return jsonify(result)


# ==========================================
# User Taste Profile & Interactions API
# ==========================================

@app.route("/api/profile", methods=["GET"])
def get_profile():
    """Retrieve full taste profile data and analytics for active user."""
    profile = get_current_profile()
    stats = calculate_profile_stats(profile)
    return jsonify({
        "profile": profile,
        "stats": stats
    })


@app.route("/api/profile/interact", methods=["POST"])
def interact_movie():
    """Record user interaction (rating, watch, dislike, unwatch)."""
    user_id = get_current_user_id()
    data = request.json or {}
    action = data.get("action")  # 'rate', 'watch', 'dislike', 'unwatch'
    movie_id = data.get("movie_id")
    rating = data.get("rating")  # 1-5

    if not movie_id or movie_id not in recommender.movie_dict:
        return jsonify({"error": "Valid movie_id is required"}), 400

    if user_id:
        success, msg = user_manager.record_interaction(user_id, action, movie_id, rating)
        profile = user_manager.get_user_profile(user_id)
    else:
        # Guest in-session storage
        profile = session.setdefault("guest_profile", copy.deepcopy(PERSONA_PROFILES["clean_slate"]))
        ratings = profile.setdefault("ratings", {})
        watch_history = profile.setdefault("watch_history", [])
        disliked = profile.setdefault("disliked", [])

        if action == "rate":
            if rating is not None:
                ratings[movie_id] = int(rating)
                if movie_id not in watch_history:
                    watch_history.append(movie_id)
                if movie_id in disliked:
                    disliked.remove(movie_id)
            else:
                ratings.pop(movie_id, None)
        elif action == "watch":
            if movie_id not in watch_history:
                watch_history.append(movie_id)
        elif action == "unwatch":
            if movie_id in watch_history:
                watch_history.remove(movie_id)
            ratings.pop(movie_id, None)
        elif action == "dislike":
            if movie_id not in disliked:
                disliked.append(movie_id)
            ratings.pop(movie_id, None)
            if movie_id in watch_history:
                watch_history.remove(movie_id)
        session.modified = True

    stats = calculate_profile_stats(profile)
    return jsonify({
        "status": "success",
        "message": f"Updated {action} for {recommender.movie_dict[movie_id]['title']}",
        "stats": stats
    })


@app.route("/api/profile/sliders", methods=["POST"])
def update_sliders():
    """Update taste dial sliders."""
    user_id = get_current_user_id()
    data = request.json or {}
    
    if user_id:
        user_manager.update_sliders(user_id, data)
        profile = user_manager.get_user_profile(user_id)
    else:
        profile = session.setdefault("guest_profile", copy.deepcopy(PERSONA_PROFILES["clean_slate"]))
        profile["sliders"] = {
            "action_level": int(data.get("action_level", 50)),
            "dark_tone": int(data.get("dark_tone", 50)),
            "plot_depth": int(data.get("plot_depth", 50))
        }
        session.modified = True

    return jsonify({"status": "success", "sliders": profile["sliders"]})


@app.route("/api/profile/reset", methods=["POST"])
def reset_profile():
    """Reset profile to clean slate."""
    user_id = get_current_user_id()
    if user_id:
        user_manager.reset_profile(user_id)
    else:
        session["guest_profile"] = copy.deepcopy(PERSONA_PROFILES["clean_slate"])
        session.modified = True

    return jsonify({
        "status": "success",
        "message": "Taste profile reset to clean slate."
    })


# ==========================================
# Persona Switcher for Quick Demo / Testing
# ==========================================

@app.route("/api/personas", methods=["GET"])
def get_personas():
    """List available demo personas."""
    current = get_current_profile()
    active_id = current.get("id", "sci_fi_geek")
    
    personas_list = []
    for p_id, p_data in PERSONA_PROFILES.items():
        personas_list.append({
            "id": p_id,
            "name": p_data["name"],
            "avatar": p_data["avatar"],
            "description": p_data["description"],
            "is_active": (p_id == active_id)
        })
    return jsonify({"personas": personas_list})


@app.route("/api/personas/select", methods=["POST"])
def select_persona():
    """Quickly apply a demo persona to current session for testing."""
    data = request.json or {}
    persona_id = data.get("persona_id")
    
    if persona_id not in PERSONA_PROFILES:
        return jsonify({"error": "Persona not found"}), 404
        
    user_id = get_current_user_id()
    if user_id:
        # Load persona data into active user profile
        user = user_manager.get_user_by_id(user_id)
        if user:
            user["profile"] = copy.deepcopy(PERSONA_PROFILES[persona_id])
            user["profile"]["id"] = user_id
            user_manager.save_users()
            return jsonify({
                "status": "success",
                "message": f"Applied persona: {PERSONA_PROFILES[persona_id]['name']}",
                "profile": user["profile"]
            })

    session["guest_profile"] = copy.deepcopy(PERSONA_PROFILES[persona_id])
    session.modified = True
    return jsonify({
        "status": "success",
        "message": f"Applied demo persona: {PERSONA_PROFILES[persona_id]['name']}",
        "profile": session["guest_profile"]
    })


if __name__ == "__main__":
    print("🎬 CineFlix Netflix Recommender Server starting on http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
