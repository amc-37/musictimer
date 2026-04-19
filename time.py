import time
import datetime

def wait_then_stop(duration_seconds):
    """Wait for duration_seconds, then stop."""
    print("Starting...")
    start = time.perf_counter()

    # Wait until the elapsed time reaches the duration
    while True:
        elapsed = time.perf_counter() - start
        if elapsed >= duration_seconds:
            break
        # Optional: print progress
        # print(f"Elapsed: {elapsed:.1f} s", end="\r")
        time.sleep(0.1)  # small sleep so we don't burn CPU

    print("Time is up! Stopping now.")


def run_until_time(target_str, start_action, stop_action):
    """
    target_str: time of day as 'HH:MM' (24h, e.g. '21:30')
    start_action: function to call immediately (e.g., start music)
    stop_action: function to call when target time is reached
    """
    # Parse the target time for *today*
    today = datetime.date.today()
    target_time = datetime.datetime.strptime(target_str, "%H:%M").time()
    target_dt = datetime.datetime.combine(today, target_time)

    now = datetime.datetime.now()

    # OPTIONAL: if target time already passed today, you can either:
    # - return immediately, or
    # - schedule for tomorrow. Here we just return.
    if target_dt <= now:
        print("Target time has already passed.")
        return

    # Start now
    start_action()

    # Compute seconds until target
    seconds_to_target = (target_dt - now).total_seconds()
    print(f"Will stop in {seconds_to_target:.0f} seconds (at {target_dt.time()}).")

    # Sleep until then
    time.sleep(seconds_to_target)

    # Stop
    stop_action()

def start_music():
    print("Music started")

def stop_music():
    print("Music stopped")




def main():

    min = int(input('please give a number of seconds'))
    #sec = min*60
    print(min)

    wait_then_stop(min)

    time = f"{input('give a time in 24 hrs and min')}"

    run_until_time(time, start_music, stop_music)



if __name__ == '__main__':
    main()
