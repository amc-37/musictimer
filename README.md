# musictimer
integrate with Spotify to start and stop playing music after customizable numbers of songs, duration of time, or a specific time on the clock


# *INSTRUCTIONS FOR SHARING/UPDATING FILES*

when you add something THEN

**in terminal:**

    git add .
    git commit -m "change msg"
    git push

    MAKE SURE TO DO THIS FOR EVERY FOLDER YOU'RE IN! Doing this only saves the stuff within your current 'cd' or location. So, if you edited something in statusFP and readme, save those separately! One in cd statusFP and one in cd /workspaces/musictimer/


**then other person does**

    git pull

------------------------------------------------------------------
# Spotify Music Timer – Setup Guide

This guide explains how to run the project locally so it can control Spotify playback (start/stop) using the Spotify Web API.

---

## Overview

This project:

* Connects to Spotify using OAuth
* Starts playback of a playlist
* Stops playback based on time or duration

⚠️ Important: This must be run **locally on your laptop**, not in GitHub Codespaces or a remote server.

---

## 1. Clone the Repository

```bash
git clone https://github.com/amc-37/musictimer.git
cd musictimer
```

If prompted to log in:

```bash
gh auth login
```

---

## 2. Install Python + Virtual Environment

Check Python:

```bash
python3 --version
```

If `venv` is missing (Linux/Ubuntu):

```bash
sudo apt update
sudo apt install python3-venv
```

Create and activate virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install spotipy python-dotenv
```

---

## 4. Create a Spotify Developer App

Go to:
[https://developer.spotify.com/dashboard](https://developer.spotify.com/dashboard)

Click **Create App** and fill in:

* **App Name:** anything (e.g. "Music Timer")
* **API:** Web API

Then go to **Settings → Redirect URIs** and add:

```text
http://127.0.0.1:8888/callback
```

Save.

---

## 5. Create `.env` File

In the root of the repo (`musictimer/`), create a file named `.env`:

```env
SPOTIPY_CLIENT_ID=your_client_id_here
SPOTIPY_CLIENT_SECRET=your_client_secret_here
SPOTIPY_REDIRECT_URI=http://127.0.0.1:8888/callback
```

⚠️ Rules:

* No quotes
* No spaces around `=`
* Must match redirect URI exactly

---

## 6. Ensure `.env` is Loaded Correctly

If running scripts inside `statusFP/`, make sure the code loads the root `.env`:

```python
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")
```

---

## 7. Test Spotify Authentication

Create `statusFP/test.py`:

```python
import os
from pathlib import Path
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

print("CLIENT_ID:", os.getenv("SPOTIPY_CLIENT_ID"))
print("REDIRECT_URI:", os.getenv("SPOTIPY_REDIRECT_URI"))

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
        scope="user-read-email",
        open_browser=True,
    )
)

print(sp.current_user())
```

Run it:

```bash
cd statusFP
python3 test.py
```

Expected:

1. Browser opens
2. Log into Spotify
3. Redirect occurs
4. Terminal prints your user info

---

## 8. Run the Main Program

After auth works:

```bash
python3 your_main_script.py
```

---

## 9. Common Errors

### `No client_id`

* `.env` not found or not loaded

### `redirect_uri: Not matching configuration`

* Mismatch between `.env` and Spotify dashboard

### `127.0.0.1 refused to connect`

* Running in Codespaces instead of local machine

### `repo not found`

* Wrong repo name or no access permissions

---

## 10. Important Notes

* Do NOT commit `.env` to GitHub
* Each user can create their own Spotify app OR share one
* Must use **Spotify Premium** for playback control

---

## 11. One-Command Setup (Recommended)

You can automate most of the setup with one command.

### Create setup script

In the root of the repo, create a file:

```bash
nano setup.sh
```

Paste this:

```bash
#!/usr/bin/env bash

set -e

echo "Setting up Spotify Music Timer..."

# Install venv if missing (Linux/Ubuntu)
if ! python3 -m venv --help > /dev/null 2>&1; then
  echo "Installing python3-venv..."
  sudo apt update
  sudo apt install -y python3-venv
fi

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install spotipy python-dotenv

echo "
Setup complete."
echo "Next steps:"
echo "1. Create a .env file with your Spotify credentials"
echo "2. Run: source .venv/bin/activate"
echo "3. Run: python3 statusFP/test.py"
```

Save and exit (`Ctrl+O`, Enter, `Ctrl+X`).

### Make it executable

```bash
chmod +x setup.sh
```

### Run it

```bash
./setup.sh
```

---

## Done

If authentication works, the rest of the project (playlist + timer logic) will run correctly.
------------------------------------------------

**THE MEAT OF OUR PROJECT**

    Right now, our code is spread out across several files as we figure out how the two most important components of our project can work: the connection with spotify and the use of time libraries to track the passage of time.

    What to run so far:
        you can connect to spotify using connect.py!
        you can try different time inputs in time.py!


-------------------------------------------


**REPOSITORY GUIDE**

*Folder: designFP*

**design.py**

    here we have our initial design idea, where we used classes to divide our code into our three different stop/start types

**design.txt**

    some notes/pseudocode made during our design phase

**FP_Design.py**

    a copy of design.py

**radiohead.json**

    example json file gotten from Spotify to begin understanding how to connect to specific songs and albums

*Folder: statusFP*

**status01.py**

    this is code written by Harvard's AI sandbox when we asked it to help us with our project. Most importantly, it showed us how to begin to connect to the Spotify API, and showed us that we needed to move away from our idea of using classes. Instead, making many functions will be more effective and make more sense for our project. This also gives us an idea of how to structure our main function. We paid little attention to the time functions here, because we explored time functions more in depth in 'time.py'.
    This code does not actually work. The connection with spotify does not work, so we have spent much time going back and forth with the AI on how to fix it. See 'connect.py' for our actual connection!

**connect.py**

    FILL THIS IN

**test.py**

    here, we are working back and forth with Harvard's AI sandbox to figure out how to connect to the Spotify API
    In this file, we simply try to form a connection with spotify

**test2.py**

    same as test.py -- part of our back and forth with the AI Sandbox

**time.py**

    time.py contains a collage of different fucntions related to the time aspect of our project that we asked Harvard's AI Sandbox to help us build

    we are testing different functions that allow us to stop and start an action after a duration of time and a specific time on the clock

    we began by importing the time and datetime library

    then we tested various different functions:

    wait_then_stop(duration_seconds)

        this fxn was written by the AI Sandbox and accepts as input a number of seconds. Then, it simply starts. After the number of seconds has passed, it stops and prints 'stopping now'. This function helped us understand how to get the code to track the passage of time according to an input, but didn't yet start and stop an action

    run_until_time(target_str, start_action, stop_action)

        then we asked the AI to help us make a time function that would stop and start an action, which made us realize that we also had to make separate   functions for starting and stopping the music (see below)
        now, we have a function that calls a start action (which we input in main as start_music()) and a stop action (in main, inputted stop_music())
        this function also tests another one of our stop types: time on the clock
        it uses the datetime library to follow the clock and calculate the time between when one calls the function and the time that one inputs as the target time

    run_until_time_loop(target_str, start_action, stop_action)

        we also consulted with the AI sandbox to construct this function, which is basically the same as run_until_time, with one key difference. It puts the important actions of the function in a while loop, so that it can have a print statement that prints out how much time has passed as the loop goes through!

    start_music()

        simply prints "music started" for now, since we haven't combined this file with our connection yet. But, we are able to know that the function is being called

    stop_music()

        same as above, but prints "music stopped"

    main()

        in our main function, we tested different inputs and called our new functions in different ways to begin familiarizing ourselves with these functions and how they might interact with the rest of our code


*Other:*

**README.md**

    you're readin' me right now :D

    come here for descriptions of our files, project, and code

**TODO.md**

    keeping track of our tasks!

------------------------------------------------------------------



