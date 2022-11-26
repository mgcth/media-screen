"""Scheduler module."""
import time
import datetime
from typing import Callable
from media_screen.lastfm import LastFM, Song

from media_screen.screen import Screen
from media_screen.misc import KILO, MEGA

DELAY = 60
NIGHT_START = datetime.time(0, 0, 0)
NIGHT_END = datetime.time(8, 0, 0)
DAY_START = datetime.time(8, 0, 0)
DAY_END = datetime.time(23, 59, 59)


def get_delay():
    """Get delay based on play stats and time of day."""
    time_now = datetime.datetime.now().time()

    if NIGHT_START <= time_now <= NIGHT_END:
        delay = DELAY * 10

    if DAY_START <= time_now <= DAY_END:
        delay = DELAY * 1

    delay = int(delay * KILO)  # s to ms

    return delay


class Item:
    """Item class."""

    def __init__(
        self,
        song: Song,
        duration: int = 0,
        progress: int = 0,
        set_delay: Callable = get_delay,
    ) -> None:
        """Item initialisation.

        Args:
            song: song
            duration: duration of previous track
            progress: last.fm API does not provide this, set to 0
            set_delay: delay function
        """
        delay = set_delay()
        self._song = song
        self._duration = song.duration if song.duration > delay else delay
        self._progress = progress
        self._delay = delay
        self._creation_time = self._get_time()

        duration = self._duration if duration == 0 else duration

        self._track_end_time = self._creation_time + duration
        self._time_delay = self._creation_time + self._delay

    @property
    def song(self):
        """Get song."""
        return self._song

    @property
    def timer(self):
        """Count down."""
        return self._track_end_time - self._get_time()

    @property
    def delay_timer(self):
        """Delay timer."""
        return self._time_delay - self._get_time()

    def reset_delay(self):
        """Reset delay timer."""
        current_time = self._get_time()
        if self._track_end_time == self._time_delay:
            self._track_end_time = current_time + self._delay

        self._time_delay = current_time + self._delay

    def _get_time(self):
        """Get current time in ms"""
        return time.time_ns() / MEGA  # ns to ms


class Scheduler:
    """Scheduler class."""

    def __init__(self, delay: float, velocity: float) -> None:
        """Initialise scheduler.

        Args:
            delay: delay in api call
            velocity: screen text movement if out of bounds
        """
        self.delay = delay
        self.velocity = velocity
        self.lastfm = LastFM()
        self.item = Item(self.lastfm.song)

    def run(self) -> None:
        """Scheduler run method."""
        new_track = self._set_track()

        with Screen() as screen:
            while True:
                if self.item.timer < 0 or self.item.delay_timer < 0:
                    new_track = self._set_track()

                if new_track is True:
                    screen.draw(0, self.item.song, 0, self.item._delay)
                    new_track = False

                time.sleep(2)

    def _set_track(self) -> bool:
        """Get the current track's progress and duration and set track end time.

        Returns:
            new track (True), same track (False)
        """
        new_track = self.lastfm.currently_playing
        duration = 0 if new_track else self.item.timer
        self.item = Item(self.lastfm.song, duration)

        return new_track
