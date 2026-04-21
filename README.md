# musictimer
integrate with Spotify to start and stop playing music after customizable numbers of songs, or starts at specific times


*INSTRUCTIONS FOR SHARING/UPDATING FILES*

when you add something THEN

**in terminal:**

    git add .
    git commit -m "change msg"
    git push

    MAKE SURE TO DO THIS FOR EVERY FOLDER YOU'RE IN! Doing this only saves the stuff within your current 'cd' or location. So, if you edited something in statusFP and readme, save those separately! One in cd statusFP and one in cd /workspaces/musictimer/


**then other person does**

    git pull

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

**THE MEAT OF OUR PROJECT**

    Right now, our code is spread out across several files as we figure out how the two most important components of our project can work: the connection with spotify and the use of time libraries.

    What to run so far:
        you can connect to spotify using connect.py!
        you can try different time inputs in time.py!


