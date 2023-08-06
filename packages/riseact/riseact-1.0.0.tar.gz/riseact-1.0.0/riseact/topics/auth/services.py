import base64
import hashlib
import random
import string
import urllib.parse
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Optional

import requests

from riseact import SETTINGS, ui
from riseact.topics.auth.data import (
    AccessToken,
    OAuthParams,
    OAuthRefreshTokenPayload,
    OAuthTokenPayload,
)
from riseact.topics.settings.services import settings_store_credentials


def auth_generate_oauth_url() -> tuple[str, str]:
    code_challenge, code_verifier = auth_generate_pkce_codes()

    base_url = f"{SETTINGS.accounts_host}/oauth/authorize/?"

    params: OAuthParams = {
        "response_type": "code",
        "code_challenge_method": "S256",
        "code_challenge": code_challenge,
        "client_id": SETTINGS.client_id,
        "redirect_uri": SETTINGS.redirect_uri,
    }

    url = base_url + urllib.parse.urlencode(params)

    return url, code_verifier


def auth_generate_pkce_codes() -> tuple[str, str]:
    # stringa random
    code_verifier = "".join(
        random.choice(string.ascii_uppercase + string.digits)
        for _ in range(random.randint(43, 128))
    )

    # encode string in utf-8
    code_verifier = code_verifier.encode("utf-8")

    # base64 della stringa
    code_verifier = base64.b64encode(code_verifier)

    # hash sha256 della stringa in base64
    code_challenge = hashlib.sha256(code_verifier).digest()

    # urlencode dell'hash sha256
    code_challenge = (
        base64.urlsafe_b64encode(code_challenge).decode("utf-8").replace("=", "")
    )

    return code_challenge, code_verifier.decode("utf-8")


def auth_wait_for_auth_code() -> Optional[str]:
    auth_code = None

    class OAuthCodeRequestHandler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:
            o = urllib.parse.urlparse(self.path)
            params = urllib.parse.parse_qs(o.query)
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"You can now close this window")

            if params.get("code"):
                self.server.query_params = params  # type: ignore

        def log_message(self, *args, **kwargs):
            return

    server = HTTPServer(("", 55443), OAuthCodeRequestHandler)
    server.handle_request()

    if "code" in server.query_params:  # type: ignore
        auth_code = server.query_params["code"][0]  # type: ignore

    return auth_code


def auth_get_access_token(auth_code: str, code_verifier: str) -> Optional[AccessToken]:
    base_url = f"{SETTINGS.accounts_host}/oauth/token/"

    payload: OAuthTokenPayload = {
        "client_id": SETTINGS.client_id,
        "code_verifier": code_verifier,
        "code": auth_code,
        "redirect_uri": SETTINGS.redirect_uri,
        "grant_type": "authorization_code",
    }

    response = requests.post(base_url, data=payload)

    try:
        response.raise_for_status()
        data = response.json()
    except Exception:  # FIX ME
        return None  # FIX ME

    return AccessToken(
        access_token=data["access_token"],
        refresh_token=data["refresh_token"],
    )


def auth_refresh_access_token(refresh_token: str) -> Optional[AccessToken]:
    base_url = f"{SETTINGS.accounts_host}/oauth/token/"
    payload: OAuthRefreshTokenPayload = {
        "client_id": SETTINGS.client_id,
        "refresh_token": refresh_token,
        "redirect_uri": SETTINGS.redirect_uri,
        "grant_type": "refresh_token",
    }

    response = requests.post(base_url, data=payload)

    try:
        response.raise_for_status()
        data = response.json()
    except Exception:  # FIX ME
        return None  # FIX ME

    return AccessToken(
        access_token=data["access_token"],
        refresh_token=data["refresh_token"],
    )


def auth_login():
    with ui.console.status("[magenta]Opening browser tab...") as status:
        auth_url, code_verifier = auth_generate_oauth_url()
        webbrowser.open((auth_url))

        status.update(status="[magenta]Waiting for OAuth code from browser...")
        auth_code = auth_wait_for_auth_code()
        if auth_code is None:
            ui.console.print("[bold red]Authentication failed.")
            return

        status.update(status="[magenta]Obtaining access token...")
        oauth_response = auth_get_access_token(auth_code, code_verifier)
        if not oauth_response:
            ui.console.print("[bold red]Authentication failed.")
            return

        status.update(status="[magenta]Storing tokens...")
        settings_store_credentials(
            access_token=oauth_response.access_token,
            refresh_token=oauth_response.refresh_token,
        )

    ui.success("Logged in.")
