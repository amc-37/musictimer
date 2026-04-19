# from radiohead.json
from datetime import datetime, timedelta
import time

def songs_path(inp):
    """given a link to a spotify playlist, communicates with spotify, and return
    the path to a spotify playlist and its queue in the form of a list of songs in the playlist"""
    path = ''
    q = ''
    # ask for input in the form of a url playlist link, and check that this is valid
    # for now, use radiohead.json to find path
    pass #maybe hard code this in for now
    return path, q
'''
def stop_type(inp):
    """given an input time, duration, or songs, determine either a time,
    a duration, or a number of songs and return it using datetime library"""
    t, d, s = ''
    pass
    return t, d, s
'''
class StartStop:
    def __init__(self, start, stop):
        """
        inherited attributes of all subclasses:
        ability to start and stop music in spotify

        each subclass has own methods for tracking passage of time and
        knowing when to invoke start stop function
        """
        self.start = start
        self.stop = stop
        pass

class Time(StartStop):
    def __init__(self, point_start, point_stop):
        self.point_start = point_start
        self.point_stop = point_stop

        point_start = input("what time do you want the music to start?")
        point_stop = input("what time do you want the music to stop?")

        pass

class Duration(StartStop):
    def __init__(self, length_start, length_stop):
        self.length_start = length_start
        self.length_stop = length_stop

        length_start = input("After how many minutes do you want the music to start?")
        length_stop = input("After how many minutes do you want the music to stop?")
        pass



class Songs(StartStop):
    def __init__(self, number_start, number_stop):
        self.number_start = number_start
        self.number_stop = number_stop

        number_start = input("After how many songs do you want the music to start?")
        number_stop = input("After how many songs do you want the music to stop?")
        pass

def main():
    # call function retrieving user input for spotify path to playlist
    playlist = input("enter your playlist") # whatever we want
    playlist_path, queue = songs_path(playlist)

    # call function asking for input about time, duration, or songs
    type = input("do you want to stop after time, duration, or songs?")
    #try execept structure to check that the input is valid and one of our 3 options
    # do work with time
    if type == "time":
        Time.point() #this will invoke methods of telling passage of time and start and stop the music
    # do work with duration
    elif type == "duration":
        Duration.length()
    elif type == "songs":
        Songs.number()


    # do work with songs

if __name__ == '__main__':
    main()
