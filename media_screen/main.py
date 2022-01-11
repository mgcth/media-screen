from spotify import Spotify
from screen import Screen
import sys
import time


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
    spotify.update()

    eink_screen = Screen()
    with eink_screen as screen:
        screen.draw_text(spotify, 0)
        screen.draw_cover_art(spotify)
        screen.draw(0, delay)

        while True:
            if spotify.check_if_new_track():
                screen.reset_x_movement()
                screen.reset_time()
                screen.draw_text(spotify, 0)
                screen.draw_cover_art(spotify)
                screen.draw(0, delay)

            # screen.draw_text(spotify, velocity)
            # screen.draw(1, delay)
            time.sleep(0.5)


def init():
    """
    Entry point to main.
    """

    if __name__ == "__main__":
        main()


init()
