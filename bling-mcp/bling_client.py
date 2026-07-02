import base64
import json
import os
import time
from pathlib import Path
from urllib.parse import urlencode

import httpx

BASE_URL = "https://www.bling.com.br"
AUTHORIZE_PATH = "/Api/v3/oauth/authorize"
TOKEN_PATH = "/Api/v3/oauth/token"
TOKENS_FILE = Path(__file__).parent / ".bling_tokens.json"

CLIENT_ID = os.environ.get("BLING_CLIENT_ID", "")
CLIENT_SECRET = os.environ.get("BLING_CLIENT_SECRET", "")
REDIRECT_URI = os.environ.get("BLING_REDIRECT_URI", "http://localhost:8765/callback")


def _basic_auth_header() -> str:
    raw = f"{CLIENT_ID}:{CLIENT_SECRET}".encode("utf-8")
    return "Basic " + base64.b64encode(raw).decode("ascii")


def build_authorize_url(state: str) -> str:
    params = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "state": state,
    }
    return f"{BASE_URL}{AUTHORIZE_PATH}?{urlencode(params)}"


def _save_tokens(tokens: dict) -> None:
    tokens["obtained_at"] = time.time()
    TOKENS_FILE.write_text(json.dumps(tokens, indent=2), encoding="utf-8")


def _load_tokens() -> dict | None:
    if not TOKENS_FILE.is_file():
        return None
    return json.loads(TOKENS_FILE.read_text(encoding="utf-8"))


def exchange_code(code: str) -> dict:
    resp = httpx.post(
        f"{BASE_URL}{TOKEN_PATH}",
        headers={
            "Authorization": _basic_auth_header(),
            "Accept": "1.0",
            "Content-Type": "application/json",
        },
        json={"grant_type": "authorization_code", "code": code},
        timeout=30,
    )
    resp.raise_for_status()
    tokens = resp.json()
    _save_tokens(tokens)
    return tokens


def _refresh(refresh_token: str) -> dict:
    resp = httpx.post(
        f"{BASE_URL}{TOKEN_PATH}",
        headers={
            "Authorization": _basic_auth_header(),
            "Accept": "1.0",
            "Content-Type": "application/json",
        },
        json={"grant_type": "refresh_token", "refresh_token": refresh_token},
        timeout=30,
    )
    resp.raise_for_status()
    tokens = resp.json()
    _save_tokens(tokens)
    return tokens


def get_access_token() -> str:
    tokens = _load_tokens()
    if not tokens:
        raise RuntimeError(
            "No Bling tokens found. Run authorize.py once locally to complete the "
            "OAuth flow before using this MCP server."
        )
    expires_in = tokens.get("expires_in", 0)
    obtained_at = tokens.get("obtained_at", 0)
    if time.time() >= obtained_at + expires_in - 60:
        tokens = _refresh(tokens["refresh_token"])
    return tokens["access_token"]


def api_request(method: str, path: str, params: dict | None = None, json_body: dict | None = None) -> dict:
    token = get_access_token()
    resp = httpx.request(
        method,
        f"{BASE_URL}{path}",
        headers={"Authorization": f"Bearer {token}", "Accept": "application/json"},
        params=params,
        json=json_body,
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json() if resp.content else {}
