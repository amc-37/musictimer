import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyPKCE

load_dotenv()

print("CLIENT_ID:", os.getenv("SPOTIPY_CLIENT_ID"))
print("REDIRECT_URI:", repr(os.getenv("SPOTIPY_REDIRECT_URI")))

sp = spotipy.Spotify(
    auth_manager=SpotifyPKCE(
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
        scope="user-read-email",
        open_browser=True,
    )
)

print(sp.current_user())
