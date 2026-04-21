import os
from pathlib import Path
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

print("CLIENT_ID:", os.getenv("SPOTIPY_CLIENT_ID"))
print("CLIENT_SECRET exists:", os.getenv("SPOTIPY_CLIENT_SECRET") is not None)
print("REDIRECT_URI:", repr(os.getenv("SPOTIPY_REDIRECT_URI")))

REDIRECT = "http://127.0.0.1:8888/callback"
print("CLIENT_ID:", os.getenv("SPOTIPY_CLIENT_ID"))
print("REDIRECT_URI:", repr(REDIRECT))

auth = SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=REDIRECT,
    scope="user-read-email",
    open_browser=True,
    show_dialog=True,
)

print("AUTH URL:", auth.get_authorize_url())

sp = spotipy.Spotify(auth_manager=auth)
print(sp.current_user())

print("Connected!")
