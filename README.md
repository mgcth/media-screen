# media screen
Python code to fetch Spotify data of currently playing track and update a Raspberry Pi e-ink display based on that data.

The `config.json` file should look like:
```
{
    "screen": {
        "fontdir": "path/to/font",
        "libdir": "path/to/lib",
        "font": "path/to/font.ttc"
    },
    "spotify": {
        "user": "user",
        "clientid": "client_id",
        "clientsecret": ""client_secret",
        "redirecturi": "redirect_uri",
        "scope": "comma-separated-scope",
        "country": "ISO country code"
    }
}
```
## Requirements
This package works with a Waveshare e-ink display (HAT). For install instructions go to: https://www.waveshare.com/wiki/3.7inch_e-Paper_HAT. These packages are not included in the requirements.txt file.