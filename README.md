[![build](https://github.com/mgcth/media_screen/actions/workflows/github-actions-build.yml/badge.svg?branch=master)](https://github.com/mgcth/media_screen/actions/workflows/github-actions-build.yml)
![coverage](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/mgcth/a732c5d7edae26bdcc6aafdc74560037/raw/badge.json)
[![lint](https://github.com/mgcth/media_screen/actions/workflows/github-actions-lint.yml/badge.svg?branch=master)](https://github.com/mgcth/media_screen/actions/workflows/github-actions-lint.yml)
![code style](https://img.shields.io/badge/code%20style-black-black)

# media screen

Python code to fetch Spotify data of currently playing track and update a Raspberry Pi e-ink display based on that data.

The `config.json` file should look like:
```json
{
    "screen": {
        "libdir": "path/to/lib",
        "font": "path/to/font.ttf/ttc",
        "icon_liked": "https://icon.png"
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
    },
}
```

## Requirements

This package works with a Waveshare e-ink display (HAT). For install instructions go to: https://www.waveshare.com/wiki/3.7inch_e-Paper_HAT. These packages are not included in the requirements.txt file.

## Example

![Example image of the screen](https://mladen.gibanica.net/posts/media_screen/20220130_111004.jpg)
