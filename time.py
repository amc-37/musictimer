import time

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

def main():

    min = int(input('please give a number of seconds'))
    #sec = min*60
    print(min)

    wait_then_stop(min)

    

if __name__ == '__main__':
    main()
