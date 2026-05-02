import os
import re
import time
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import urlparse

import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth


env_path = Path(__file__).resolve().parent / ".env"
if not env_path.exists():
    env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path, override=True)

SCOPES = (
    "user-modify-playback-state "
    "user-read-playback-state "
    "playlist-read-private"
)
PLAYABLE_CONTEXT_TYPES = {"playlist", "album", "artist"}
PLAYABLE_URI_TYPES = {"track", "episode"}
SUPPORTED_TYPES = PLAYABLE_CONTEXT_TYPES | PLAYABLE_URI_TYPES


def get_spotify_client():
    """Return an authenticated Spotify client."""
    return spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=os.getenv("SPOTIPY_CLIENT_ID"),
            client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
            redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
            scope=SCOPES,
            open_browser=True,
        )
    )


def get_available_device_id(spotify_client):
    """Return the active device ID, or the first available device if needed."""
    devices = spotify_client.devices().get("devices", [])

    for device in devices:
        if device.get("is_active"):
            return device["id"]

    if devices:
        return devices[0]["id"]

    raise RuntimeError("No Spotify devices available. Open Spotify on a device first.")


def parse_spotify_input(playable_input):
    """
    Parse a Spotify URL or URI and return (resource_type, resource_id).

    Accepts links and URIs for playlist, album, artist, track, and episode.
    Raises ValueError for unsupported or invalid input.
    """
    cleaned_input = playable_input.strip()
    if not cleaned_input:
        raise ValueError("Input cannot be empty.")

    if cleaned_input.startswith("spotify:"):
        parts = cleaned_input.split(":")
        if len(parts) < 3:
            raise ValueError("Invalid Spotify URI.")
        resource_type = parts[1].lower().strip()
        resource_id = parts[2].strip()
    else:
        parsed = urlparse(cleaned_input)
        if parsed.scheme not in {"http", "https"}:
            raise ValueError("Please enter a Spotify URL or Spotify URI.")
        if parsed.netloc not in {"open.spotify.com", "play.spotify.com"}:
            raise ValueError("Please enter a Spotify URL, not another website.")

        path_parts = [part for part in parsed.path.split("/") if part]
        if len(path_parts) < 2:
            raise ValueError("That Spotify URL is missing a playable resource.")

        if path_parts[0].startswith("intl-") and len(path_parts) >= 3:
            resource_type = path_parts[1].lower().strip()
            resource_id = path_parts[2].strip()
        else:
            resource_type = path_parts[0].lower().strip()
            resource_id = path_parts[1].strip()

    if not resource_id:
        raise ValueError("That Spotify link is missing an ID.")

    if resource_type not in SUPPORTED_TYPES:
        raise ValueError(
            "Unsupported Spotify resource. Please enter a playlist, album, artist, track, or episode link."
        )

    return resource_type, resource_id


def validate_playable_input(spotify_client, playable_input):
    """
    Validate user input and return a normalized playback target.

    Returns a dict with keys:
    - kind: 'context' or 'uris'
    - resource_type: playlist/album/artist/track/episode
    - uri: normalized Spotify URI
    - display_name: human-readable name for status messages
    """
    resource_type, resource_id = parse_spotify_input(playable_input)

    if resource_type == "playlist":
        resource_data = spotify_client.playlist(resource_id, fields="name,uri")
    elif resource_type == "album":
        resource_data = spotify_client.album(resource_id)
    elif resource_type == "artist":
        resource_data = spotify_client.artist(resource_id)
    elif resource_type == "track":
        resource_data = spotify_client.track(resource_id)
    elif resource_type == "episode":
        resource_data = spotify_client.episode(resource_id)
    else:
        raise ValueError("That Spotify resource type is not supported.")

    if not resource_data or not resource_data.get("uri"):
        raise ValueError("Spotify did not return a playable resource for that link.")

    resource_uri = resource_data["uri"]
    display_name = resource_data.get("name", resource_uri)

    return {
        "kind": "context" if resource_type in PLAYABLE_CONTEXT_TYPES else "uris",
        "resource_type": resource_type,
        "uri": resource_uri,
        "display_name": display_name,
    }


def prompt_for_playable_input(spotify_client):
    """Keep prompting until the user enters a valid playable Spotify link or URI."""
    while True:
        playable_input = input(
            "Enter a Spotify playlist, album, artist, track, or episode link/URI: "
        ).strip()

        try:
            playback_target = validate_playable_input(spotify_client, playable_input)
            print(
                f"Valid Spotify {playback_target['resource_type']} detected: {playback_target['display_name']}"
            )
            return playback_target
        except spotipy.SpotifyException:
            print("Spotify could not open that resource. Please enter a playable Spotify link or URI.")
        except ValueError as exc:
            print(f"Input error: {exc}")


def get_current_playback_state(spotify_client):
    """
    Return a compact summary of current playback state.

    Confirms whether Spotify exposes enough information to resume correctly by
    retrieving:
    - is_playing
    - progress_ms
    - current item URI
    - current context URI
    """
    playback_data = spotify_client.current_playback(additional_types="episode")
    if not playback_data:
        return None

    current_item = playback_data.get("item") or {}
    current_context = playback_data.get("context") or {}
    device = playback_data.get("device") or {}

    return {
        "is_playing": bool(playback_data.get("is_playing")),
        "progress_ms": playback_data.get("progress_ms"),
        "item_uri": current_item.get("uri"),
        "context_uri": current_context.get("uri"),
        "device_id": device.get("id"),
        "raw": playback_data,
    }


def describe_current_playback(playback_state):
    """Return a short printable description of current playback visibility."""
    if playback_state is None:
        return "No current Spotify playback detected."

    progress_ms = playback_state.get("progress_ms")
    if progress_ms is None:
        progress_text = "unknown position"
    else:
        progress_text = f"{progress_ms / 1000:.1f}s"

    return (
        "Playback visibility confirmed: "
        f"is_playing={playback_state.get('is_playing')}, "
        f"progress={progress_text}, "
        f"item={playback_state.get('item_uri')}, "
        f"context={playback_state.get('context_uri')}"
    )


def playback_matches_target(playback_target, playback_state):
    """Return True if current playback already matches the requested target."""
    if playback_state is None:
        return False

    if playback_target["kind"] == "context":
        return playback_state.get("context_uri") == playback_target["uri"]

    return playback_state.get("item_uri") == playback_target["uri"]


def ensure_requested_playback(spotify_client, playback_target, device_id):
    """
    Start or resume playback intelligently.

    Behavior:
    - if there is no current playback, start the requested target from the beginning
    - if the current playback matches the target and is already playing, leave it alone
    - if the current playback matches the target and is paused, resume from the current position
    - if the current playback is on something else, start the requested target from the beginning
    """
    playback_state = get_current_playback_state(spotify_client)
    print(describe_current_playback(playback_state))

    if playback_matches_target(playback_target, playback_state):
        if playback_state.get("is_playing"):
            print("Requested Spotify resource is already playing. Leaving playback as-is.")
            return "already_playing"

        spotify_client.start_playback(device_id=device_id)
        print("Requested Spotify resource matched current playback. Resumed from the current position.")
        return "resumed"

    if playback_target["kind"] == "context":
        spotify_client.start_playback(device_id=device_id, context_uri=playback_target["uri"])
    else:
        spotify_client.start_playback(device_id=device_id, uris=[playback_target["uri"]])

    print("Started requested Spotify resource from the beginning.")
    return "started_fresh"


def pause(spotify_client, device_id):
    """Pause playback on the target device."""
    spotify_client.pause_playback(device_id=device_id)


def stop_after_duration(spotify_client, device_id, duration_minutes):
    """Stop playback after the requested number of minutes."""
    sleep_seconds = duration_minutes * 60
    print(f"Will stop in {sleep_seconds:.0f} seconds.")
    time.sleep(sleep_seconds)
    pause(spotify_client, device_id)
    print("Playback paused successfully.")


def stop_at_clock_time(spotify_client, device_id, stop_time_input):
    """Stop playback at the next matching HH:MM clock time."""
    current_datetime = datetime.now()
    stop_datetime = datetime.strptime(stop_time_input, "%H:%M").replace(
        year=current_datetime.year,
        month=current_datetime.month,
        day=current_datetime.day,
    )

    if stop_datetime <= current_datetime:
        stop_datetime += timedelta(days=1)

    sleep_seconds = (stop_datetime - current_datetime).total_seconds()
    print(f"Will stop in {sleep_seconds:.0f} seconds (at {stop_datetime.time()}).")
    time.sleep(sleep_seconds)
    pause(spotify_client, device_id)
    print("Playback paused successfully.")


def prompt_for_stop_mode():
    """Prompt until the user enters a supported stop mode."""
    while True:
        stop_mode = input("Stop mode (duration/time): ").strip().lower()
        if stop_mode in {"duration", "time"}:
            return stop_mode
        print("Invalid stop mode. Please enter 'duration' or 'time'.")


def prompt_for_duration_minutes():
    """Prompt until the user enters a positive number of minutes."""
    while True:
        raw_input_value = input("Stop after how many minutes? ").strip()
        try:
            duration_minutes = float(raw_input_value)
        except ValueError:
            print("Please enter a number of minutes, such as 15 or 22.5.")
            continue

        if duration_minutes <= 0:
            print("Please enter a positive number of minutes.")
            continue

        return duration_minutes


def prompt_for_stop_time():
    """Prompt until the user enters a valid HH:MM 24-hour time."""
    while True:
        stop_time_input = input("Stop at what time? (HH:MM 24h) ").strip()
        if re.fullmatch(r"\d{2}:\d{2}", stop_time_input) is None:
            print("Please enter time in HH:MM 24-hour format, for example 21:30.")
            continue

        try:
            datetime.strptime(stop_time_input, "%H:%M")
            return stop_time_input
        except ValueError:
            print("That is not a real 24-hour time. Try something like 08:05 or 21:30.")


def main():
    try:
        spotify_client = get_spotify_client()
        print("Spotify authentication successful.")

        playback_target = prompt_for_playable_input(spotify_client)
        stop_mode = prompt_for_stop_mode()
        device_id = get_available_device_id(spotify_client)

        playback_action = ensure_requested_playback(spotify_client, playback_target, device_id)
        print(
            f"Playback action for {playback_target['display_name']}: {playback_action} on device {device_id}."
        )

        if stop_mode == "duration":
            duration_minutes = prompt_for_duration_minutes()
            print(f"Duration mode selected: {duration_minutes} minute(s).")
            stop_after_duration(spotify_client, device_id, duration_minutes)
        else:
            stop_time_input = prompt_for_stop_time()
            print(f"Time mode selected: stopping at {stop_time_input}.")
            stop_at_clock_time(spotify_client, device_id, stop_time_input)

    except RuntimeError as exc:
        print(f"Runtime error: {exc}")
    except spotipy.SpotifyException as exc:
        print(f"Spotify API error: {exc}")
    except Exception as exc:
        print(f"Unexpected error: {exc}")


if __name__ == "__main__":
    main()
