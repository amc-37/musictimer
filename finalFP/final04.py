import os
import time
from datetime import datetime, timedelta
from pathlib import Path

from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.exceptions import SpotifyException


# Load .env from current folder first (finalFP/.env), then repo root fallback.
CURRENT_DIR = Path(__file__).resolve().parent
ENV_CANDIDATES = [
    CURRENT_DIR / ".env",
    CURRENT_DIR.parent / ".env",
]
for env_path in ENV_CANDIDATES:
    if env_path.exists():
        load_dotenv(env_path, override=True)
        break


SCOPES = "user-modify-playback-state user-read-playback-state playlist-read-private"


def get_spotify_client():
    return spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=os.getenv("SPOTIPY_CLIENT_ID"),
            client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
            redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
            scope=SCOPES,
            open_browser=True,
        )
    )


def get_active_device(sp):
    devices = sp.devices().get("devices", [])
    for device in devices:
        if device.get("is_active"):
            return device["id"]
    if devices:
        return devices[0]["id"]
    raise RuntimeError("No Spotify devices available.")


def extract_spotify_resource(resource_input):
    resource_input = resource_input.strip()

    if resource_input.startswith("spotify:"):
        parts = resource_input.split(":")
        if len(parts) >= 3:
            resource_type = parts[1]
            resource_id = parts[2]
            resource_uri = f"spotify:{resource_type}:{resource_id}"
            return resource_type, resource_id, resource_uri

    if "open.spotify.com/" in resource_input:
        path = resource_input.split("open.spotify.com/")[1].split("?")[0].strip("/")
        parts = path.split("/")
        if len(parts) >= 2:
            resource_type = parts[0]
            resource_id = parts[1]
            resource_uri = f"spotify:{resource_type}:{resource_id}"
            return resource_type, resource_id, resource_uri

    raise ValueError(
        "Please enter a valid Spotify URL or spotify: URI for a playlist, album, artist, track, or episode."
    )


def validate_resource(sp, resource_type, resource_id):
    playable_types = {"playlist", "album", "artist", "track", "episode"}

    if resource_type not in playable_types:
        raise ValueError(
            f"Unsupported Spotify resource type: {resource_type}. "
            "Supported types are playlist, album, artist, track, and episode."
        )

    try:
        if resource_type == "playlist":
            data = sp.playlist(resource_id)
            name = data.get("name", "Unknown playlist")
        elif resource_type == "album":
            data = sp.album(resource_id)
            name = data.get("name", "Unknown album")
        elif resource_type == "artist":
            data = sp.artist(resource_id)
            name = data.get("name", "Unknown artist")
        elif resource_type == "track":
            data = sp.track(resource_id)
            name = data.get("name", "Unknown track")
        elif resource_type == "episode":
            data = sp.episode(resource_id)
            name = data.get("name", "Unknown episode")
        else:
            raise ValueError("Unsupported resource type.")
    except SpotifyException as exc:
        raise ValueError(f"Spotify could not validate that resource: {exc}") from exc

    return data, name


def prompt_until_valid_resource(sp):
    while True:
        resource_input = input("Spotify URL or URI: ").strip()
        try:
            resource_type, resource_id, resource_uri = extract_spotify_resource(resource_input)
            data, name = validate_resource(sp, resource_type, resource_id)
            print(f"Valid Spotify {resource_type} detected: {name}")
            return resource_input, resource_type, resource_id, resource_uri, data
        except ValueError as exc:
            print(f"Input error: {exc}")
            print("Please try again.\n")


def get_current_playback(sp):
    try:
        return sp.current_playback()
    except SpotifyException:
        return None


def determine_premium_status(sp):
    """
    Premium-only player-control endpoints typically return HTTP 403 for non-Premium users.
    We use a harmless player-state call pattern and treat 403 as non-Premium.
    """
    try:
        sp.devices()
        sp.current_playback()
        return True
    except SpotifyException as exc:
        if exc.http_status == 403:
            return False
        raise


def print_playlist_contents(sp, playlist_id):
    results = sp.playlist_items(
        playlist_id,
        additional_types=("track",),
        fields="items(track(name,artists(name),album(name))),next",
    )

    print("\nPlaylist contents:")
    index = 1

    while results:
        for item in results.get("items", []):
            track = item.get("track")
            if not track:
                continue
            track_name = track.get("name", "Unknown track")
            artists = track.get("artists", [])
            artist_name = artists[0]["name"] if artists else "Unknown artist"
            album_name = track.get("album", {}).get("name", "Unknown album")
            print(f"{index}. {track_name} — {artist_name} [{album_name}]")
            index += 1

        if results.get("next"):
            results = sp.next(results)
        else:
            results = None


def show_resource_contents(sp, resource_type, resource_id, resource_data):
    if resource_type == "playlist":
        print(f"\nShowing playlist contents for: {resource_data.get('name', 'Unknown playlist')}")
        print_playlist_contents(sp, resource_id)
        return

    if resource_type == "album":
        album_name = resource_data.get("name", "Unknown album")
        artists = resource_data.get("artists", [])
        artist_name = artists[0]["name"] if artists else "Unknown artist"
        print(f"\nAlbum: {album_name}")
        print(f"Artist: {artist_name}")
        tracks = resource_data.get("tracks", {}).get("items", [])
        if tracks:
            print("Tracks:")
            for i, track in enumerate(tracks, start=1):
                print(f"{i}. {track.get('name', 'Unknown track')}")
        return

    if resource_type == "artist":
        print(f"\nArtist: {resource_data.get('name', 'Unknown artist')}")
        followers = resource_data.get("followers", {}).get("total")
        if followers is not None:
            print(f"Followers: {followers}")
        genres = resource_data.get("genres", [])
        if genres:
            print("Genres: " + ", ".join(genres))
        return

    if resource_type == "track":
        track_name = resource_data.get("name", "Unknown track")
        artists = resource_data.get("artists", [])
        artist_name = artists[0]["name"] if artists else "Unknown artist"
        album_name = resource_data.get("album", {}).get("name", "Unknown album")
        print(f"\nTrack: {track_name}")
        print(f"Artist: {artist_name}")
        print(f"Album: {album_name}")
        return

    if resource_type == "episode":
        print(f"\nEpisode: {resource_data.get('name', 'Unknown episode')}")
        show = resource_data.get("show", {}).get("name", "Unknown show")
        print(f"Show: {show}")
        return


def context_matches(playback, resource_uri):
    if not playback:
        return False

    context = playback.get("context")
    if context and context.get("uri") == resource_uri:
        return True

    item = playback.get("item")
    if item and item.get("uri") == resource_uri:
        return True

    return False


def start_or_resume_playback(sp, playback, resource_type, resource_uri, device_id):
    if playback and context_matches(playback, resource_uri):
        if playback.get("is_playing"):
            print("Requested Spotify resource is already playing. Leaving playback unchanged.")
            return

        print("Requested Spotify resource matches current playback. Resuming from current position.")
        sp.start_playback(device_id=device_id)
        return

    if resource_type in {"playlist", "album", "artist"}:
        print("Starting requested Spotify context from the beginning.")
        sp.start_playback(device_id=device_id, context_uri=resource_uri)
        return

    if resource_type in {"track", "episode"}:
        print("Starting requested Spotify item from the beginning.")
        sp.start_playback(device_id=device_id, uris=[resource_uri])
        return

    raise ValueError(f"Unsupported playable resource type: {resource_type}")


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
    print(f"Will stop in {int(seconds)} seconds (at {stop_dt.strftime('%H:%M')}).")
    time.sleep(seconds)
    pause(sp, device_id)


def main():
    sp = get_spotify_client()
    print("Connected to Spotify!")

    resource_input, resource_type, resource_id, resource_uri, resource_data = prompt_until_valid_resource(sp)

    print("\nResource details:")
    show_resource_contents(sp, resource_type, resource_id, resource_data)

    is_premium = determine_premium_status(sp)

    if not is_premium:
        print("\nPlayback control requires Spotify Premium.")
        print("Showing resource contents instead.")
        return

    try:
        playback = get_current_playback(sp)
        device_id = get_active_device(sp)
        start_or_resume_playback(sp, playback, resource_type, resource_uri, device_id)
    except (RuntimeError, SpotifyException) as exc:
        print(f"\nPlayback control is unavailable right now: {exc}")
        print("Showing resource contents instead.")
        return

    mode = input("Stop mode (duration/time/none): ").strip().lower()
    if mode == "duration":
        minutes = int(input("Stop after how many minutes? ").strip())
        stop_after_duration(sp, device_id, minutes)
    elif mode == "time":
        stop_time = input("Stop at what time? (HH:MM 24h) ").strip()
        stop_at_clock_time(sp, device_id, stop_time)
    elif mode == "none":
        print("No automatic stop selected.")
    else:
        print("Unsupported stop mode. Playback will continue.")


if __name__ == "__main__":
    main()
