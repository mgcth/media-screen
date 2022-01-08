from spotify import Spotify
from screen import Screen
import time


def main():
    """
    Main function.
    """

    spotify = Spotify()
    spotify.update()

    eink_screen = Screen()
    with eink_screen as screen:
        screen.update_full(spotify)
        screen.draw(0)
        screen.update_partial(spotify)
        screen.draw(2)

        while True:
            if spotify.check_if_new_track():
                screen.update_full(spotify)
                screen.reset_x_movement()
                screen.draw(0)

            screen.update_partial(spotify, 20)
            screen.draw(2)


def init():
    """
    Entry point to main.
    """
    if __name__ == "__main__":
        main()


init()
