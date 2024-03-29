[![build](https://github.com/mgcth/media_screen/actions/workflows/github-actions-build.yml/badge.svg?branch=master)](https://github.com/mgcth/media_screen/actions/workflows/github-actions-build.yml)
[![coverage](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/mgcth/cec46aedd403b589ddf14c657ef187fd/raw/media-screen-coverage-badge.json)](https://github.com/mgcth/media_screen/actions/workflows/github-actions-build.yml)
[![lint](https://github.com/mgcth/media_screen/actions/workflows/github-actions-lint.yml/badge.svg?branch=master)](https://github.com/mgcth/media_screen/actions/workflows/github-actions-lint.yml)
![code style](https://img.shields.io/badge/code%20style-black-black)

# media-screen

Package to show some last.fm statistics on a Raspberry Pi e-ink screen.

The `config.json` file should look like:

```json
{
    "screen": {
        "libdir": "path/to/lib",
        "font": "path/to/font.ttf/ttc",
        "icon_liked": "https://icon.png"
    },
    "last.fm": {
        "username": "last.fm user name",
        "api_key": "api_key",
        "api_secret": "api_secret"
    },
}
```

## Requirements

This package works with a Waveshare e-ink display (HAT). For install instructions go to: <https://www.waveshare.com/wiki/3.7inch_e-Paper_HAT>. These packages are not included in the requirements.txt file.

## Example

![Example image of the screen](https://mladen.gibanica.net/posts/media_screen/20220130_111004.jpg)
