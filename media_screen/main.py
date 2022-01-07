from spotify import Spotify
from screen import Screen
import time


def main():
    """
    Main function.
    """

    spotify = Spotify()
    spotify.update()

    screen = Screen()
    with screen as s:
        screen.update_full(spotify)
        screen.draw()
        screen.update_partial(spotify)
        screen.draw()

        while True:
            if spotify.check_if_new_track():
                screen.update_full(spotify)
                screen.reset_x_movement()
                screen.draw()

            screen.update_partial(spotify, 20)
            screen.draw()
            time.sleep(0.1)


def init():
    """
    Entry point to main.
    """
    if __name__ == "__main__":
        main()


init()
