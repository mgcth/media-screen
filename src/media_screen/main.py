import sys
import time
from spotify import Spotify
from lastfm import LastFM
from screen import Screen


def main():
    """
    Main function.
    """

    try:
        delay = sys.argv[1]
        velocity = sys.argv[2]
    except:
        delay = 2
        velocity = 0

    spotify = Spotify()

    lastfm = LastFM()
    lastfm.get_currently_playing()

    with Screen() as screen:
        screen.draw(0, spotify, lastfm, 0, delay)

        while True:
            try:
                if spotify.check_if_new_track():
                    lastfm.get_currently_playing()
                    screen.draw(0, spotify, lastfm, 0, delay)

                # screen.draw_text(spotify, velocity)
                # screen.draw(1, delay)
            except:
                print("Error.")

            time.sleep(0.5)


def init():
    """
    Entry point to main.
    """

    if __name__ == "__main__":
        main()


init()
