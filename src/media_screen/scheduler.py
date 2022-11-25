"""Scheduler module."""
import time
from media_screen.lastfm import LastFM, Song

from media_screen.screen import Screen
from media_screen.misc import KILO, MEGA


class Item:
    """Item class."""

    def __init__(self, song: Song, progress: int = 0, delay: int = 30) -> None:
        """Item initialisation.

        Args:
            song: song
            duration: duration of track
            progress: last.fm API does not provide this, set to 0
            delay: delay in API call
        """
        delay = delay * KILO  # s to ms
        self._song = song
        self._duration = song.duration if song.duration > delay else delay
        self._progress = progress
        self._delay = delay
        self._creation_time = self._get_time()

        self._track_end_time = self._creation_time + self._duration
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
        delay = self._time_delay - self._get_time()
        return delay

    def reset_delay(self):
        """Reset delay timer."""
        if self._track_end_time == self._time_delay:
            self._track_end_time = self._get_time() + self._delay

        self._time_delay = self._get_time() + self._delay

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
        self.item = None

    def run(self) -> None:
        """Scheduler run method."""
        with Screen() as screen:
            while True:
                if self.item is None:
                    new_track = self._set_track()
                    continue

                if self.item.timer < 0 or self.item.delay_timer < 0:
                    new_track = self._set_track()

                if new_track is True:
                    screen.draw(0, self.item.song, 0, self.item._delay)
                    new_track = False

                time.sleep(5)

    def _set_track(self) -> bool:
        """Get the current track's progress and duration and set track end time.

        Returns:
            new track (True), same track (False)
        """
        new_track = self.lastfm.currently_playing

        if new_track is False:
            if self.item:
                self.item.reset_delay()
            return new_track

        if self.lastfm.item_ok:
            self.item = Item(self.lastfm.song)
            return new_track
