"""Screen module."""
import os
import sys
import time
import requests
import logging
from io import BytesIO
from waveshare_epd import epd3in7
from media_screen.misc import CONFIG, KILO, MEGA
from PIL import Image, ImageDraw, ImageFont, ImageOps


config = CONFIG["screen"]

if os.path.exists(config["libdir"]):
    sys.path.append(config["libdir"])

logging.basicConfig(level=logging.INFO)


class Screen:
    """Screen class of media_screen."""

    def __init__(self, mode=0):
        """Initialise screen class.

        Input:
            mode: 0 - full or 1 - partial, controls the display mode
        """
        self._font60 = ImageFont.truetype(config["font"], 60)
        self._mode = mode
        self._artists_x = 0
        self._album_x = 0
        self._track_x = 0
        self._time_delay = 0

    def __enter__(self):
        """Create screen and its image."""
        try:
            logging.info("Initialise")
            self._epd = epd3in7.EPD()

            self._clear()

            self._image = Image.new("1", (self._epd.height, self._epd.width), 255)

            response = requests.get(config["icon_liked"])
            self.liked_icon = Image.open(BytesIO(response.content)).convert("RGBA")
            background = Image.new("RGBA", self.liked_icon.size, (255, 255, 255))
            self.liked_icon = Image.alpha_composite(background, self.liked_icon)
            self.liked_icon = ImageOps.grayscale(self.liked_icon)
            self.liked_icon.thumbnail((65, 65), Image.ANTIALIAS)

        except IOError as e:
            logging.info(e)

        except KeyboardInterrupt:
            self._shutdown("ctrl + c")

        return self

    def __exit__(self, type, value, traceback):
        """Shutdown screen."""
        self._clear()
        self._sleep()

    def _draw_cover_art(self, lastfm):
        """Draw cover art.

        Input:
            lastfm: lastfm object
        """
        logging.info("Draw track art")

        if lastfm.item_ok:
            image = ImageOps.grayscale(lastfm.image)
            image.thumbnail((65, 65), Image.ANTIALIAS)
            self._image.paste(image, (235, 210))

    def _draw_text(self, lastfm, velocity=0):
        """Draw music text.

        Input:
            lastfm: lastfm object
            velocity: velocity of moving text if needed, pixels/refresh
        """
        time_image = Image.new("1", (160, 70), 255)
        time_draw = ImageDraw.Draw(time_image)
        time_draw.rectangle((0, 8, 160, 70), fill=255)
        time_draw.text((0, 8), time.strftime("%H:%M"), font=self._font60, fill=0)

        play_count_image = Image.new("1", (150, 70), 255)
        play_count_draw = ImageDraw.Draw(play_count_image)
        play_count_draw.rectangle((0, 8, 150, 70), fill=255)

        liked_image = Image.new("1", (65, 65), 255)
        if lastfm.count != None:
            play_count_draw.text((0, 8), str(lastfm.count), font=self._font60, fill=0)

            if lastfm.count > 200:
                liked_image.paste(self.liked_icon, (0, 0))

        music_image = Image.new("1", (480, 210), 255)
        if lastfm.item_ok:
            music_image, self._artists_x = self._slide_music_text(
                music_image, self._artists_x, lastfm.artists, 0, velocity
            )
            music_image, self._album_x = self._slide_music_text(
                music_image, self._album_x, lastfm.album, 70, velocity
            )
            music_image, self._track_x = self._slide_music_text(
                music_image, self._track_x, lastfm.track, 140, velocity
            )

        self._image.paste(liked_image, (0, 210))
        self._image.paste(play_count_image, (70, 210))
        self._image.paste(time_image, (320, 210))
        self._image.paste(music_image, (0, 0))

    def _slide_music_text(self, music_image, obj, text, y_position, velocity):
        """Draw the music information and slide it if too long.

        Input:
            music_image: music image object
            obj: objects x position
            text: text to draw
            y_position: text's y-position
            velocity: velocity of moving text if needed, pixels/refresh
        """
        music_draw = ImageDraw.Draw(music_image)
        music_draw.rectangle((0, y_position, 480, y_position + 70), fill=255)

        music_x, _ = music_draw.textsize(text, font=self._font60)
        if music_x > 480:
            obj += velocity

            if obj > music_x - 480:
                obj = 0

        music_draw.text((-obj, y_position), text, font=self._font60, fill=0)

        return music_image, obj

    def _draw_kernel(self, mode):
        """Drawing kernel.

        Input:
            mode: mode of drawing
        """
        self._image = self._image.rotate(180)

        if mode == 1:
            logging.info("Partial update")
            self._clear(1)
            self._epd.display_1Gray(self._epd.getbuffer(self._image))
        else:
            logging.info("Full update")
            self._clear(0)
            self._epd.display_4Gray(self._epd.getbuffer_4Gray(self._image))

        self._image = self._image.rotate(
            180
        )  # rotate back (not efficient, find better way later)

    def _clear(self, mode=0):
        """Clear the screen and set mode."""
        logging.info("Clear")
        self._mode = mode
        self._epd.init(mode)
        self._epd.Clear(0xFF, mode)

    def _sleep(self):
        """Put screen to sleep."""
        logging.info("Goto Sleep...")
        self._epd.sleep()

    def _shutdown(self, text="Shutdown screen"):
        """Shutdown screen.

        Input:
            text: text to log
        """
        logging.info(text)
        epd3in7.epdconfig.module_exit()

    def _get_time(self):
        """Get current time in ms."""
        return time.time_ns() / MEGA  # ns to ms

    def _reset_x_movement(self):
        """Reset the x_movement of text."""
        self._artists_x = 0
        self._album_x = 0
        self._track_x = 0

    def _reset_time(self):
        """Reset time variable."""
        self._time_delay = 0

    def draw(self, mode, lastfm, velocity=0, delay=5):
        """Draw to screen based on current display mode.

        Input:
            mode: mode of drawing, 0 full, 1 partial
            lastfm: lastfm object
            velocity: velocity of moving text if needed, pixels/refresh
            delay: time to wait for new draw
        """
        self._draw_text(lastfm, velocity)
        self._draw_cover_art(lastfm)
        self._reset_x_movement()
        self._reset_time()

        # want to update time_delay below because draw can take some time
        if self._get_time() > self._time_delay:
            self._epd.init(mode)  # activate screen for drawing

            self._draw_kernel(mode)

            self._sleep()  # put screen to sleep

            self._time_delay = self._get_time() + delay * KILO
