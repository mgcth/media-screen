import pylast
from config import config


config = ["last.fm"]


class LastFM:
    """
    LastFM class.
    """

    def __init__(self):
        """
        Initialise the class.
        """

        username = config["username"]
        self.network = pylast.LastFMNetwork(
            api_key=config["api_key"],
            api_secret=config["api_secret"],
            username=username,
        )
        self.user = pylast.User(username, self.network)

    def get_currently_playing(self):
        """
        Get the currently playing track
        """

        self.track = self.user.user.get_now_playing()
        self.count = self.track.get_userplaycount()
