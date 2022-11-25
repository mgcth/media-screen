"""Scheduler module."""
import time
from media_screen.lastfm import LastFM
from media_screen.screen import Screen
from media_screen.misc import KILO, MEGA


class Item:
    """Item class."""

    def __init__(self, duration: int, progress: int = 0, delay: int = 30) -> None:
        """Item initialisation.

        Args:
            duration: duration of track
            progress: last.fm API does not provide this, set to 0
            delay: delay in API call
        """
        self.duration = duration
        self.progress = progress
        self.delay = delay * KILO  # s to ms
        self.creation_time = self._get_time()

        self._track_end_time = self.creation_time + self.duration
        self._time_delay = self._set_delay()

    @property
    def timer(self):
        """Count down."""
        return self._track_end_time - self._get_time()

    @property
    def delay_timer(self):
        """Delay timer."""
        delay = self._time_delay - self._get_time()
        self._time_delay = self._set_delay()
        return delay

    def _get_time(self):
        """Get current time in ms"""
        return time.time_ns() / MEGA  # ns to ms

    def _set_delay(self):
        """Set time delay."""
        return self.creation_time + self._delay


class Scheduler:
    """Scheduler class."""

    def __init__(self, delay: float, velocity: float) -> None:
        """Initialise scheduler.

        Args:
            delay: delay in api call
            velocity: screen text movement if out of bounds
        """
        self._delay = delay
        self._velocity = velocity
        self.lastfm = LastFM()
        self.item = None
        self.track = None

    def run(self) -> None:
        """Scheduler run method."""
        with Screen() as screen:
            while True:
                if self.item is None:
                    new_track = self._set_track()
                    continue

                if self.item.timer < 0:
                    new_track = self._set_track()

                if self.item.delay_timer < 0:
                    new_track = self._set_track()

                if new_track is True:
                    screen.draw(0, self.lastfm, 0, self._delay)

                time.sleep(1)

    def _set_track(self) -> bool:
        """Get the current track's progress and duration and set track end time.

        Returns:
            new track (True), same track (False)
        """
        new_track = self.lastfm.currently_playing
        print(self.lastfm._track)

        if new_track is False:
            return new_track

        if self.lastfm.item_ok:
            duration = self.track.get_duration()
            self.item = Item(duration)
            return new_track
