"""
User Authentication & Profile Storage Manager for CineFlix AI.
Handles persistent user accounts, password hashing, session tokens,
and per-user preference vector profiles.
"""

import os
import json
import uuid
import copy
from datetime import datetime
from typing import Dict, Any, Optional, List, Tuple
from werkzeug.security import generate_password_hash, check_password_hash
from engine.recommender import PERSONA_PROFILES


class UserManager:
    def __init__(self, storage_path: str = "data/users.json"):
        self.storage_path = storage_path
        self.users: Dict[str, Dict[str, Any]] = {}
        self.email_to_id: Dict[str, str] = {}
        self.load_users()

    def load_users(self):
        """Loads user accounts from JSON storage or seeds default demo accounts."""
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    self.users = json.load(f)
                self.email_to_id = {u["email"].lower(): u["id"] for u in self.users.values() if "email" in u}
                return
            except Exception as e:
                print(f"Warning: Could not read {self.storage_path}, re-seeding: {e}")

        # Seed initial demo accounts from personas
        self.users = {}
        self._seed_default_accounts()
        self.save_users()

    def _seed_default_accounts(self):
        """Seeds standard demo accounts for instant evaluation."""
        demo_accounts = [
            {
                "id": "user_alex",
                "name": "Alex",
                "email": "alex@cineflix.ai",
                "password_hash": generate_password_hash("password123"),
                "avatar": "🚀",
                "bio": "Sci-Fi & Mind Benders Enthusiast",
                "created_at": datetime.now().isoformat(),
                "profile": copy.deepcopy(PERSONA_PROFILES["sci_fi_geek"])
            },
            {
                "id": "user_sarah",
                "name": "Sarah",
                "email": "sarah@cineflix.ai",
                "password_hash": generate_password_hash("password123"),
                "avatar": "🔍",
                "bio": "True Crime & Dark Thrillers Fanatic",
                "created_at": datetime.now().isoformat(),
                "profile": copy.deepcopy(PERSONA_PROFILES["true_crime_addict"])
            },
            {
                "id": "user_jordan",
                "name": "Jordan",
                "email": "jordan@cineflix.ai",
                "password_hash": generate_password_hash("password123"),
                "avatar": "🍿",
                "bio": "Feel-Good Comedies & Cozy Cinema",
                "created_at": datetime.now().isoformat(),
                "profile": copy.deepcopy(PERSONA_PROFILES["feel_good_fan"])
            },
            {
                "id": "user_marcus",
                "name": "Marcus",
                "email": "marcus@cineflix.ai",
                "password_hash": generate_password_hash("password123"),
                "avatar": "🔥",
                "bio": "Action & High-Stakes Blockbusters",
                "created_at": datetime.now().isoformat(),
                "profile": copy.deepcopy(PERSONA_PROFILES["adrenaline_junkie"])
            }
        ]

        for acc in demo_accounts:
            self.users[acc["id"]] = acc
            self.email_to_id[acc["email"].lower()] = acc["id"]

    def save_users(self):
        """Persists user dictionary to JSON file."""
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        try:
            with open(self.storage_path, "w", encoding="utf-8") as f:
                json.dump(self.users, f, indent=2)
        except Exception as e:
            print(f"Error saving users to {self.storage_path}: {e}")

    def create_user(
        self,
        name: str,
        email: str,
        password: str,
        avatar: str = "👤"
    ) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """Registers a new user with secure password hash and fresh clean profile."""
        email_clean = email.strip().lower()
        if not email_clean or "@" not in email_clean:
            return False, "Please enter a valid email address.", None

        if not name or len(name.strip()) < 2:
            return False, "Full name must be at least 2 characters.", None

        if not password or len(password) < 6:
            return False, "Password must be at least 6 characters.", None

        if email_clean in self.email_to_id:
            return False, "An account with this email already exists.", None

        user_id = f"user_{uuid.uuid4().hex[:10]}"
        clean_profile = copy.deepcopy(PERSONA_PROFILES["clean_slate"])
        clean_profile["id"] = user_id
        clean_profile["name"] = name.strip()
        clean_profile["avatar"] = avatar

        user_data = {
            "id": user_id,
            "name": name.strip(),
            "email": email_clean,
            "password_hash": generate_password_hash(password),
            "avatar": avatar,
            "bio": "CineFlix Film Enthusiast",
            "created_at": datetime.now().isoformat(),
            "profile": clean_profile
        }

        self.users[user_id] = user_data
        self.email_to_id[email_clean] = user_id
        self.save_users()

        return True, "Account created successfully!", self._safe_user_dict(user_data)

    def authenticate_user(self, email: str, password: str) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """Validates login credentials."""
        email_clean = email.strip().lower()
        if not email_clean or not password:
            return False, "Email and password are required.", None

        user_id = self.email_to_id.get(email_clean)
        if not user_id or user_id not in self.users:
            return False, "Invalid email or password.", None

        user = self.users[user_id]
        if not check_password_hash(user["password_hash"], password):
            return False, "Invalid email or password.", None

        return True, "Login successful!", self._safe_user_dict(user)

    def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves raw user record by user_id."""
        return self.users.get(user_id)

    def get_safe_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves public user data (excluding password hash)."""
        user = self.users.get(user_id)
        return self._safe_user_dict(user) if user else None

    def get_user_profile(self, user_id: str) -> Dict[str, Any]:
        """Retrieves the taste preference profile for recommendations."""
        user = self.users.get(user_id)
        if user and "profile" in user:
            return user["profile"]
        # Fallback to a default clean profile
        fallback = copy.deepcopy(PERSONA_PROFILES["clean_slate"])
        fallback["id"] = user_id or "guest"
        return fallback

    def update_user_profile(self, user_id: str, updates: Dict[str, Any]) -> bool:
        """Updates user account details or preferences."""
        user = self.users.get(user_id)
        if not user:
            return False

        if "name" in updates and updates["name"].strip():
            user["name"] = updates["name"].strip()
            user["profile"]["name"] = updates["name"].strip()

        if "avatar" in updates and updates["avatar"]:
            user["avatar"] = updates["avatar"]
            user["profile"]["avatar"] = updates["avatar"]

        if "bio" in updates:
            user["bio"] = updates["bio"]

        self.save_users()
        return True

    def record_interaction(
        self,
        user_id: str,
        action: str,
        movie_id: str,
        rating: Optional[int] = None
    ) -> Tuple[bool, str]:
        """Records movie rating, watch, dislike, or unwatch for the user."""
        user = self.users.get(user_id)
        if not user:
            return False, "User not found"

        profile = user.setdefault("profile", copy.deepcopy(PERSONA_PROFILES["clean_slate"]))
        ratings = profile.setdefault("ratings", {})
        watch_history = profile.setdefault("watch_history", [])
        disliked = profile.setdefault("disliked", [])

        if action == "rate":
            if rating is not None and 1 <= int(rating) <= 5:
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

        self.save_users()
        return True, f"Updated {action} successfully"

    def update_sliders(self, user_id: str, sliders: Dict[str, int]) -> bool:
        """Updates user taste tuning sliders."""
        user = self.users.get(user_id)
        if not user:
            return False

        profile = user.setdefault("profile", copy.deepcopy(PERSONA_PROFILES["clean_slate"]))
        profile["sliders"] = {
            "action_level": max(0, min(100, int(sliders.get("action_level", 50)))),
            "dark_tone": max(0, min(100, int(sliders.get("dark_tone", 50)))),
            "plot_depth": max(0, min(100, int(sliders.get("plot_depth", 50))))
        }
        self.save_users()
        return True

    def reset_profile(self, user_id: str) -> bool:
        """Resets user viewing and rating history to fresh clean slate."""
        user = self.users.get(user_id)
        if not user:
            return False

        user["profile"] = {
            "id": user_id,
            "name": user["name"],
            "avatar": user.get("avatar", "👤"),
            "description": "Personalized Taste Profile",
            "watch_history": [],
            "ratings": {},
            "disliked": [],
            "preferred_genres": [],
            "preferred_moods": [],
            "sliders": {"action_level": 50, "dark_tone": 50, "plot_depth": 50}
        }
        self.save_users()
        return True

    def _safe_user_dict(self, user: Dict[str, Any]) -> Dict[str, Any]:
        """Strips sensitive fields like password hash from returned object."""
        if not user:
            return {}
        u_copy = dict(user)
        u_copy.pop("password_hash", None)
        return u_copy
