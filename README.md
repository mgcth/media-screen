# media screen
Python code to fetch Spotify data of currently playing track and update a Raspberry Pi e-ink display based on that data.

The `config.json` file should look like:
```
{
    "screen": {
        "libdir": "path/to/lib",
        "font": "path/to/font.ttf/ttc"
    },
    "spotify": {
        "user": "user",
        "clientid": "client_id",
        "clientsecret": ""client_secret",
        "redirecturi": "redirect_uri",
        "scope": "comma-separated-scope",
        "country": "ISO country code"
    }
    "last.fm": {
        "username": "last.fm user name",
        "api_key": "api_key",
        "api_secret": "api_secret"
    }
}
```

## Requirements
This package works with a Waveshare e-ink display (HAT). For install instructions go to: https://www.waveshare.com/wiki/3.7inch_e-Paper_HAT. These packages are not included in the requirements.txt file.