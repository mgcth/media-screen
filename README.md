# media screen
Python code to fetch Spotify data of currently playing track and update a Raspberry Pi E ink display based on that data.

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