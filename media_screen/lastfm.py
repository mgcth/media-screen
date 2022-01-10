import time
import pylast
from config import config


config = config["last.fm"]


class LastFM:
    """
    LastFM class.
    """

    def __init__(self):
        """
        Initialise the class.
        """

        username = config["username"]

        try:
            self.network = pylast.LastFMNetwork(
                api_key=config["api_key"],
                api_secret=config["api_secret"],
                username=username,
            )
            self.user = pylast.User(username, self.network)

        except pylast.PyLastError as e:
            print("Problems connecting to last.fm")
            print(e)
            self.network = None
            self.user = None

    def get_currently_playing(self):
        """
        Get the currently playing track
        """

        time.sleep(5)

        try:
            self.track = self.user.get_now_playing()
            if self.track != None:
                self.count = self.track.get_userplaycount()
        except pylast.MalformedResponseError as e:
            print("Last.fm get track error")
            print(e)
            self.track = None
