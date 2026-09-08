"""
TMDB API Integration Layer for CineFlix AI.
Provides real-time search, movie/TV discovery, watch-provider verification for India (watch_region="IN"),
and trailer metadata lookup using the TMDB v3 API.
API credentials are securely read from the TMDB_API_KEY environment variable.
"""

import os
import time
import urllib.request
import urllib.parse
import json
from typing import Dict, Any, List, Optional, Tuple

TMDB_API_BASE = "https://api.themoviedb.org/3"
TMDB_IMAGE_BASE_W500 = "https://image.tmdb.org/t/p/w500"
TMDB_IMAGE_BASE_ORIGINAL = "https://image.tmdb.org/t/p/original"
NETFLIX_PROVIDER_ID = 8  # TMDB Provider ID for Netflix
DEFAULT_WATCH_REGION = "IN"  # India

# In-memory query response cache (TTL: 1 hour)
_CACHE: Dict[str, Tuple[float, Any]] = {}
CACHE_TTL = 3600


class TMDBClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("TMDB_API_KEY", "").strip()
        self.watch_region = DEFAULT_WATCH_REGION

    @property
    def is_configured(self) -> bool:
        """Returns True if a valid API key is present."""
        return bool(self.api_key)

    def _make_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """Executes a GET request to the TMDB API with error handling and caching."""
        if not self.is_configured:
            return None

        params = params or {}
        params["api_key"] = self.api_key

        cache_key = f"{endpoint}?{urllib.parse.urlencode(sorted(params.items()))}"
        now = time.time()
        if cache_key in _CACHE:
            cached_time, cached_data = _CACHE[cache_key]
            if now - cached_time < CACHE_TTL:
                return cached_data

        url = f"{TMDB_API_BASE}/{endpoint.lstrip('/')}?{urllib.parse.urlencode(params)}"
        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "CineFlixAI/2.0 (Netflix India Recommendation Engine)"}
            )
            with urllib.request.urlopen(req, timeout=6) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode("utf-8"))
                    _CACHE[cache_key] = (now, data)
                    return data
        except Exception as e:
            print(f"[TMDB Client] Request error for {endpoint}: {e}")
            return None
        return None

    def search_multi(self, query: str, page: int = 1) -> List[Dict[str, Any]]:
        """Performs multi-search across movies, TV shows, and people on TMDB."""
        if not query or not self.is_configured:
            return []

        res = self._make_request("search/multi", {
            "query": query,
            "page": page,
            "include_adult": "false"
        })
        if not res or "results" not in res:
            return []
        return res["results"]

    def search_movies(self, query: str, page: int = 1) -> List[Dict[str, Any]]:
        """Search movies specifically."""
        if not query or not self.is_configured:
            return []

        res = self._make_request("search/movie", {
            "query": query,
            "page": page,
            "include_adult": "false"
        })
        return res.get("results", []) if res else []

    def search_tv(self, query: str, page: int = 1) -> List[Dict[str, Any]]:
        """Search TV series specifically."""
        if not query or not self.is_configured:
            return []

        res = self._make_request("search/tv", {
            "query": query,
            "page": page,
            "include_adult": "false"
        })
        return res.get("results", []) if res else []

    def get_watch_providers(self, media_type: str, tmdb_id: int) -> Dict[str, Any]:
        """
        Retrieves streaming watch providers for a movie/tv title.
        Checks for Netflix availability specifically in region IN (India).
        """
        if not self.is_configured:
            return {"netflixAvailable": False, "watchRegion": self.watch_region, "providers": []}

        endpoint = f"{media_type}/{tmdb_id}/watch/providers"
        res = self._make_request(endpoint)
        if not res or "results" not in res:
            return {"netflixAvailable": False, "watchRegion": self.watch_region, "providers": []}

        in_providers = res["results"].get(self.watch_region, {})
        flatrate = in_providers.get("flatrate", [])
        
        is_on_netflix = any(p.get("provider_id") == NETFLIX_PROVIDER_ID for p in flatrate)
        provider_names = [p.get("provider_name") for p in flatrate]

        return {
            "netflixAvailable": is_on_netflix,
            "watchRegion": self.watch_region,
            "providers": provider_names
        }

    def get_videos(self, media_type: str, tmdb_id: int) -> Optional[str]:
        """Fetches the official YouTube trailer video ID if available."""
        if not self.is_configured:
            return None

        endpoint = f"{media_type}/{tmdb_id}/videos"
        res = self._make_request(endpoint)
        if not res or "results" not in res:
            return None

        videos = res["results"]
        # Prefer Official Trailer on YouTube
        for v in videos:
            if v.get("site") == "YouTube" and v.get("type") in ["Trailer", "Teaser"] and v.get("official"):
                return v.get("key")
        for v in videos:
            if v.get("site") == "YouTube":
                return v.get("key")
        return None
