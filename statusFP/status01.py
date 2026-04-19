import os
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

SCOPES = "user-modify-playback-state user-read-playback-state playlist-read-private"

def get_spotify_client():
    return spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=os.getenv("SPOTIPY_CLIENT_ID"),
            client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
            redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
            scope=SCOPES,
            open_browser=True
        )
    )

def get_active_device(sp):
    devices = sp.devices()["devices"]
    for d in devices:
        if d["is_active"]:
            return d["id"]
    if devices:
        return devices[0]["id"]
    raise RuntimeError("No Spotify devices available.")

def extract_playlist_uri(playlist_url_or_uri):
    if "playlist/" in playlist_url_or_uri:
        playlist_id = playlist_url_or_uri.split("playlist/")[1].split("?")[0]
        return f"spotify:playlist:{playlist_id}"
    if playlist_url_or_uri.startswith("spotify:playlist:"):
        return playlist_url_or_uri
    raise ValueError("Invalid playlist link or URI.")

def start_playlist(sp, playlist_uri, device_id):
    sp.start_playback(device_id=device_id, context_uri=playlist_uri)

def pause(sp, device_id):
    sp.pause_playback(device_id=device_id)

def stop_after_duration(sp, device_id, minutes):
    time.sleep(minutes * 60)
    pause(sp, device_id)

def stop_at_clock_time(sp, device_id, stop_time_str):
    now = datetime.now()
    stop_dt = datetime.strptime(stop_time_str, "%H:%M").replace(
        year=now.year, month=now.month, day=now.day
    )
    if stop_dt <= now:
        stop_dt += timedelta(days=1)
    seconds = (stop_dt - now).total_seconds()
    time.sleep(seconds)
    pause(sp, device_id)

def main():
    sp = get_spotify_client()
    playlist = input("Playlist URL or URI: ").strip()
    mode = input("Stop mode (duration/time): ").strip().lower()

    playlist_uri = extract_playlist_uri(playlist)
    device_id = get_active_device(sp)

    start_playlist(sp, playlist_uri, device_id)

    if mode == "duration":
        minutes = int(input("Stop after how many minutes? "))
        stop_after_duration(sp, device_id, minutes)
    elif mode == "time":
        stop_time = input("Stop at what time? (HH:MM 24h) ")
        stop_at_clock_time(sp, device_id, stop_time)
    else:
        print("Songs mode needs track-progress logic and is harder to do reliably.")

if __name__ == "__main__":
    main()
