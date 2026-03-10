"""
Thin HTTP client for self-hosted Convex on Railway.

External: https://convex-backend-production-95d6.up.railway.app
Internal: http://convex-backend.railway.internal:3210
"""

import json
import logging
import os
from typing import Any, Dict, Optional

import requests

logger = logging.getLogger("compound_learning.convex")

# Default to internal Railway URL, fall back to external
DEFAULT_CONVEX_URL = "http://convex-backend.railway.internal:3210"
EXTERNAL_CONVEX_URL = "https://convex-backend-production-95d6.up.railway.app"


class ConvexClient:
    """HTTP client for self-hosted Convex backend on Railway."""

    def __init__(self, url: Optional[str] = None, token: Optional[str] = None):
        self.url = (
            url
            or os.environ.get("CONVEX_URL")
            or DEFAULT_CONVEX_URL
        ).rstrip("/")
        self.token = token or os.environ.get("OPENCLAW_CONVEX_SECRET")
        self._session = requests.Session()
        if self.token:
            self._session.headers["Authorization"] = f"Convex {self.token}"
        self._session.headers["Content-Type"] = "application/json"

    @property
    def available(self) -> bool:
        """Check if Convex is reachable (cached per-session)."""
        if not hasattr(self, "_available"):
            try:
                r = self._session.get(f"{self.url}/version", timeout=3)
                self._available = r.status_code == 200
            except Exception:
                self._available = False
        return self._available

    def mutation(self, function_name: str, args: Optional[Dict[str, Any]] = None) -> Any:
        """Call a Convex mutation.

        POST /api/mutation
        Body: {"path": "module:functionName", "args": {...}}
        """
        return self._call("mutation", function_name, args)

    def query(self, function_name: str, args: Optional[Dict[str, Any]] = None) -> Any:
        """Call a Convex query.

        POST /api/query
        Body: {"path": "module:functionName", "args": {...}}
        """
        return self._call("query", function_name, args)

    def action(self, function_name: str, args: Optional[Dict[str, Any]] = None) -> Any:
        """Call a Convex action.

        POST /api/action
        Body: {"path": "module:functionName", "args": {...}}
        """
        return self._call("action", function_name, args)

    def _call(self, kind: str, function_name: str, args: Optional[Dict[str, Any]] = None) -> Any:
        url = f"{self.url}/api/{kind}"
        payload = {
            "path": function_name,
            "args": args or {},
            "format": "json",
        }
        try:
            resp = self._session.post(url, json=payload, timeout=15)
            resp.raise_for_status()
            data = resp.json()
            if data.get("status") == "error":
                logger.error("Convex %s %s error: %s", kind, function_name, data.get("errorMessage"))
                return None
            return data.get("value")
        except requests.exceptions.ConnectionError:
            logger.warning("Convex unreachable at %s — skipping %s %s", self.url, kind, function_name)
            return None
        except requests.exceptions.Timeout:
            logger.warning("Convex timeout for %s %s", kind, function_name)
            return None
        except Exception as e:
            logger.error("Convex %s %s failed: %s", kind, function_name, e)
            return None
