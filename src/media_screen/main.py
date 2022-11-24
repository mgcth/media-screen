import time
from media_screen.lastfm import LastFM
from media_screen.screen import Screen


def main():
    """
    Main function defining the run loop.
    """
    delay = 2
    velocity = 0

    lastfm = LastFM()
    lastfm.currently_playing

    with Screen() as screen:
        screen.draw(0, lastfm, 0, delay)

        while True:
            if lastfm.new_track:
                continue

            lastfm.currently_playing
            screen.draw(0, lastfm, 0, delay)

            time.sleep(30)


def init():
    """
    Entry point to main.
    """
    if __name__ == "__main__":
        main()


init()
