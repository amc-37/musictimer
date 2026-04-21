import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

REDIRECT = "http://127.0.0.1:8888/callback"
print("CLIENT_ID:", os.getenv("SPOTIPY_CLIENT_ID"))
print("REDIRECT_URI:", repr(REDIRECT))

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id="your_client_id",
        client_secret="your_client_secret",
        redirect_uri="http://127.0.0.1:8888/callback",
        scope="user-read-email",
        open_browser=True
    )
)

print(sp.current_user())

sp = spotipy.Spotify(auth_manager=auth)
print(sp.current_user())
