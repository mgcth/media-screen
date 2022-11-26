from unittest.mock import patch
from media_screen.main import init


@patch("media_screen.main.__name__", "__main__")
@patch("media_screen.main.main")
def test_init(mock_main):
    """Dummy test."""
    pass
