import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

load_dotenv(dotenv_path="../.env") # it doesn't matter what folder .env file is in now
print("CLIENT_ID:", os.getenv("SPOTIPY_CLIENT_ID"))

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
