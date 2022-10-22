import time
import pylast
from media_screen.misc import config, KILO, MEGA


config = config["last.fm"]


class LastFM:
    """
    LastFM class.
    """

    def __init__(self):
        """
        Initialise the class.
        """

        self._count = None

        try:
            username = config["username"]
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

    def get_currently_playing(self):
        """
        Get the currently playing track
        """

        time.sleep(5)  # for now, should try to id last.fm and spotify

        try:
            track = self.user.get_now_playing()
            if track != None:
                self._count = track.get_userplaycount()
        except pylast.MalformedResponseError as e:
            print("Last.fm get track error")
            print(e)

    @property
    def count(self):
        """
        Get item_ok property.

        Output:
            count: times track has been played
        """

        return self._count
