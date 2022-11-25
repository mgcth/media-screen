"""Main module."""
from media_screen.scheduler import Scheduler


def main():
    """
    Main function defining the run loop.
    """
    delay = 2
    velocity = 0

    scheduler = Scheduler(delay, velocity)
    scheduler.run()


def init():
    """
    Entry point to main.
    """
    if __name__ == "__main__":
        main()


init()
