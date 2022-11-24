from unittest.mock import patch
from media_screen.main import init


@patch("media_screen.main.main")
def test_init(mock_main):
    """
    Dummy test.
    """
    init()
    mock_main.assert_called_once()
