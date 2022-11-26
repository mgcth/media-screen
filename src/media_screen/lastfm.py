"""Last.fm module."""
import requests
from PIL import Image
from io import BytesIO
from typing import Any
from media_screen.misc import CONFIG
from pylast import LastFMNetwork, User, PyLastError, MalformedResponseError


config = CONFIG["last.fm"]


class Song:
    """Song class"""

    def __init__(
        self,
        title: str = "",
        album: str = "",
        artist: str = "",
        image: Any = None,
        duration: int = 0,
        playcount: int = 0,
    ) -> None:
        """Initialise song.

        Args:
            title: song title
            album: song album
            artist: song artist
            image: song cover image
            duration: song duration
            playcount: number of times song played
        """
        self.title = title
        self.album = album
        self.artist = artist
        self.image = image
        self.duration = duration
        self.playcount = playcount


class LastFM:
    """LastFM class."""

    def __init__(self):
        """Initialise the Last.fm class."""
        self._clear()

        try:
            username = config["username"]
            network = LastFMNetwork(
                api_key=config["api_key"],
                api_secret=config["api_secret"],
                username=username,
            )
            network.enable_rate_limit()
            self.user = User(username, network)
        except PyLastError:
            raise PyLastError("Failed to connect to last.fm")

    @property
    def currently_playing(self) -> bool:
        """Get the currently playing track

        Returns:
            new track (True), same track (False)
        """
        try:
            track = self.user.get_now_playing()
        except MalformedResponseError:
            raise MalformedResponseError("Last.fm get track error.")

        if self._track == track:
            return False
        else:
            self._track = track

        if self._track != None:
            self._set_track_details()
        else:
            self._clear()

        return True

    @property
    def item_ok(self) -> bool:
        """Check if item is ok to draw."""
        return self._item_ok

    @property
    def song(self) -> Song:
        """Get track image url."""
        return self._song

    def _get_track_image(self, image_url) -> None:
        """Download the track album cover image and hold it in memory.

        Args:
            image_url: image url
        """
        response = requests.get(image_url)
        return Image.open(BytesIO(response.content))

    def _set_track_details(self) -> None:
        """Store track details in object."""
        self._item_ok = True

        track_title = self._track.title
        track_album = self._track.get_album().title
        track_artist = self._track.get_artist().name
        track_image_url = self._track.get_cover_image()
        track_image = self._get_track_image(track_image_url)
        track_duration = self._track.get_duration()
        track_playcount = self._track.get_userplaycount()

        self._song = Song(
            track_title,
            track_album,
            track_artist,
            track_image,
            track_duration,
            track_playcount,
        )

    def _clear(self) -> None:
        """Clear object details."""
        self._item_ok = False
        self._track = None
        self._song = Song()
