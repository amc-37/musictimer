# from radiohead.json
import datetime

def songs_path(inp):
    """ask for input in the form of a url, and return
    the path to a spotify playlist in the form of a list of songs in the playlist"""
    q = ''
    # ask for input in the form of a url playlist link, and check that this is valid
    # for now, use radiohead.json to find path
    pass #maybe hard code this in for now
    return q #

def stop_type(inp):
    """given an input time, duration, or songs, determine either a time,
    a duration, or a number of songs and return it using datetime library"""
    t, d, s = ''
    pass
    return t, d, s

def main():
    # call function retrieving user input for spotify path to playlist
    playlist = input("enter your playlist") # whatever we want
    queue = songs_path(playlist)

    # call function asking for input about time, duration, or songs
    type = input("do you want to stop after time, duration, or songs?")
    time, duration, songs = stop_type(type)
    # do work with time

    # do work with duration

    # do work with songs

if __name__ == '__main__':
    main()
