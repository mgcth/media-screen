import time
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from PIL import Image
from io import BytesIO
import pathlib
import os
from config import config

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

    def __init__(self, delay=10):
        """
        Initialise the Spotify class and set authorisation. First run saves to cache and requires user input.

        Input:
            -delay: api call delay in seconds converted to ms in function
        """

        credentials = SpotifyOAuth(
            client_id=config["clientid"],
            client_secret=config["clientsecret"],
            redirect_uri=config["redirecturi"],
            scope=config["scope"],
            open_browser=False,
            username=config["user"],
            cache_path=cache_file,
        )
        self.country = config["country"]
        self.client = spotipy.client.Spotify(client_credentials_manager=credentials)
        self.delay = delay * KILO  # s to ms

    def get_current_item(self):
        """
        Get current track information.
        """

        self.current_item = self.client.currently_playing(self.country)
        self.isrc = self.current_item["item"]["external_ids"]["isrc"]
        self.artists = self.current_item["item"]["artists"][0][
            "name"
        ]  # first artist for now
        self.album = self.current_item["item"]["album"]["name"]
        self.track = self.current_item["item"]["name"]

    def get_track_time(self):
        """
        Get the current track's progress and duration and set track end time.
        """

        self.duration = self.current_item["item"]["duration_ms"]
        self.progress = self.current_item["progress_ms"]

        current_time = self.get_time()
        self.track_end_time = current_time + self.duration
        self.time_delay = current_time + self.delay

    def get_track_image(self):
        """
        Download the track album cover image and hold in memory.
        """

        image_details = self.current_item["item"]["album"]["images"][
            0
        ]  # get first and largest image size
        url = image_details["url"]
        self.image_size = image_details["width"], image_details["height"]
        response = requests.get(url)
        self.image = Image.open(BytesIO(response.content))

    def check_if_new_track(self):
        """
        Check if we have passed the track end time and update the object.
        Don't use progress so we don't have to call the api too often.
        However, we need to call the api if user changes track, do that with a delay.

        Output:
            -new: boolean stating if new track started or not
        """

        new = False
        current_time = self.get_time()

        if current_time > self.time_delay:
            self.time_delay = current_time + self.delay

            previous_track_external_id = self.isrc
            self.get_current_item()
            current_item_external_id = self.isrc

            if previous_track_external_id != current_item_external_id:
                self.update()
                new = True

        if current_time > self.track_end_time:
            self.update()
            new = True

        return new

    def update(self):
        """
        Update the object with an api call.
        """

        self.get_current_item()
        self.get_track_image()
        self.get_track_time()

    def get_time(self):
        """
        Get current time in ms
        """

        return time.time_ns() / MEGA  # ns to ms
