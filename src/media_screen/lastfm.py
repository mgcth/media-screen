"""Last.fm module."""
import time
import requests
from PIL import Image
from io import BytesIO
from media_screen.misc import CONFIG
from pylast import LastFMNetwork, User, Track, PyLastError, MalformedResponseError


config = CONFIG["last.fm"]


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

        if self._track != None:
            self._set_track_details()
        else:
            self._clear()

        return True

    @property
    def count(self) -> int:
        """Get track count.

        Returns:
            times track has been played
        """
        return self._count

    @property
    def item_ok(self) -> bool:
        """Check if item is ok to draw."""
        return self._item_ok

    @property
    def track(self) -> str:
        """Get track title."""
        return self._track_title

    @property
    def album(self) -> str:
        """Get album title."""
        return self._album_title

    @property
    def artists(self) -> str:
        """Get artists name."""
        return self._artists_name

    def _get_track_image(self) -> None:
        """Download the track album cover image and hold it in memory."""
        if self._item_ok:
            response = requests.get(self._image_url)
            self.image = Image.open(BytesIO(response.content))

    def _set_track_details(self) -> None:
        """Store track details in object."""
        self._item_ok = True
        self._count = self._track.get_userplaycount()
        self._track_title = self._track.title
        self._album_title = self._track.get_album().title
        self._artists_name = self._track.get_artist().name
        self._image_url = self._track.get_cover_image()

        self._get_track_image()

    def _clear(self) -> None:
        """Clear object details."""
        self._item_ok = False
        self._count = None
        self._track_title = None
        self._album_title = None
        self._artists_name = None
        self._image_url = None
        self._track = None
