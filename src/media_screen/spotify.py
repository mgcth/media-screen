import time
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from PIL import Image
from io import BytesIO
import pathlib
import os
from misc import config, KILO, MEGA


config = config["spotify"]
cache_file = os.path.join(
    pathlib.Path(__file__).parent.resolve(), ".cache-" + config["user"]
)
KILO = 1000
MEGA = 1000000


class Spotify:
    """
    Spotify class of media_screen
    """

    def __init__(self, delay=30):
        """
        Initialise the Spotify class and set authorisation. First run saves to cache and requires user input.

        Input:
            delay: api call delay in s converted to ms in function
        """

        self._item_ok = False
        self._delay = delay * KILO  # s to ms
        self._country = config["country"]

        self._item = None
        self._isrc = None
        self._artists = None
        self._album = None
        self._track = None
        self._time_delay = None
        self._track_end_time = None

        try:
            credentials = SpotifyOAuth(
                client_id=config["clientid"],
                client_secret=config["clientsecret"],
                redirect_uri=config["redirecturi"],
                scope=config["scope"],
                open_browser=False,
                username=config["user"],
                cache_path=cache_file,
            )

            self._client = spotipy.client.Spotify(
                client_credentials_manager=credentials
            )

            self._update()

        except spotipy.oauth2.SpotifyOauthError as e:
            print("Error during Spotify authentication.")
            print(e)
            self._client = None

    def _get_current_item(self):
        """
        Get current track information.
        """

        self._item = self._client.currently_playing(self._country)
        if self._item != None:
            self._item_ok = True
            self._isrc = self._item["item"]["external_ids"]["isrc"]
            self._artists = self._item["item"]["artists"][0][
                "name"
            ]  # first artist for now
            self._album = self._item["item"]["album"]["name"]
            self._track = self._item["item"]["name"]
        else:
            print("Recieved current item is empty")
            self._item_ok = False

    def _get_track_time(self):
        """
        Get the current track's progress and duration and set track end time.
        """

        if self._item_ok:
            self.duration = self._item["item"]["duration_ms"]
            self.progress = self._item["progress_ms"]

            current_time = self._get_time()
            self._track_end_time = current_time + self.duration
            self._time_delay = current_time + self._delay

    def _get_track_image(self):
        """
        Download the track album cover image and hold in memory.
        """

        if self._item_ok:
            image_details = self._item["item"]["album"]["images"][
                0
            ]  # get first and largest image size
            url = image_details["url"]
            self.image_size = image_details["width"], image_details["height"]
            response = requests.get(url)
            self.image = Image.open(BytesIO(response.content))

    def _get_time(self):
        """
        Get current time in ms
        """

        return time.time_ns() / MEGA  # ns to ms

    def _update(self):
        """
        Update object state with one api call.
        """

        if self._client != None:
            self._get_current_item()
            self._get_track_image()
            self._get_track_time()

    @property
    def item_ok(self):
        """
        Get item_ok property.

        Output:
            item_ok: item recieved is OK
        """

        return self._item_ok

    @property
    def artists(self):
        """
        Get artists property.

        Output:
            artists: artists
        """

        return self._artists

    @property
    def album(self):
        """
        Get album property.

        Output:
            album: album
        """

        return self._album

    @property
    def track(self):
        """
        Get track property.

        Output:
            track: track
        """

        return self._track

    def check_if_new_track(self):
        """
        Check if we have passed the track end time and update the object.
        Don't use progress so we don't have to call the api too often.
        However, we need to call the api if user changes track, do that with a delay.

        Output:
            new_track: boolean stating if new track started or not
        """

        new_track = False

        if self._item_ok:

            current_time = self._get_time()
            if current_time > self._time_delay:

                self._time_delay = current_time + self._delay
                previous_track_external_id = self._isrc
                self._update()

                current_item_external_id = self._isrc
                if previous_track_external_id != current_item_external_id:
                    new_track = True

            elif current_time > self._track_end_time:
                self._update()
                new_track = True

        return new_track
