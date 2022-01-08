import sys
import os
import time
from lastfm import LastFM
from config import config


config = config["screen"]

if os.path.exists(config["libdir"]):
    sys.path.append(config["libdir"])

import logging
from waveshare_epd import epd3in7
import time
from PIL import Image, ImageDraw, ImageFont, ImageOps
import traceback


logging.basicConfig(level=logging.INFO)


KILO = 1000
MEGA = 1000000


lastfm = LastFM()


class Screen:
    """
    Screen class of media_screen.
    """

    def __init__(self, mode=0):
        """
        Initialise screen class.

        Input:
            mode: 0 - full or 1 - partial, controls the display mode
        """

        self.font60 = ImageFont.truetype(config["font"], 60)
        self.mode = mode
        self.reset_x_movement()
        self.reset_time()

    def __enter__(self):
        """
        Create screen and its image.
        """

        try:
            logging.info("Initialise")
            self.epd = epd3in7.EPD()

            self.clear()

            self.image = Image.new("1", (self.epd.height, self.epd.width), 255)

        except IOError as e:
            logging.info(e)

        except KeyboardInterrupt:
            self.shutdown("ctrl + c")

        return self

    def __exit__(self, type, value, traceback):
        """
        Shutdown screen.
        """

        self.clear()
        self.sleep()

    def draw_cover_art(self, spotify):
        """
        Draw cover art.

        Input:
            -spotify: spotify object
        """

        logging.info("Draw track art")

        image = ImageOps.grayscale(spotify.image)
        image.thumbnail((200, 200), Image.ANTIALIAS)
        self.image.paste(image, (0, 0))

    def draw_text(self, spotify, velocity=0):
        """
        Draw music text

        Input:
            -spotify: spotify object
            -velocity: velocity of moving text if needed, pixels/refresh
        """

        time_image = Image.new("1", (160, 70), 255)
        time_draw = ImageDraw.Draw(time_image)
        time_draw.rectangle((0, 8, 160, 70), fill=255)
        time_draw.text((0, 8), time.strftime("%H:%M"), font=self.font60, fill=0)

        lastfm.get_currently_playing()
        play_count_image = Image.new("1", (200, 70), 255)
        play_count_draw = ImageDraw.Draw(play_count_image)
        play_count_draw.rectangle((0, 8, 200, 70), fill=255)
        play_count_draw.text((0, 8), str(lastfm.count), font=self.font60, fill=0)

        music_image = Image.new("1", (480, 210), 255)

        music_image, self.artists_x = self.slide_music_text(
            music_image, self.artists_x, spotify.artists, 0, velocity
        )
        music_image, self.album_x = self.slide_music_text(
            music_image, self.album_x, spotify.album, 70, velocity
        )
        music_image, self.track_x = self.slide_music_text(
            music_image, self.track_x, spotify.track, 140, velocity
        )

        self.image.paste(play_count_image, (0, 210))
        self.image.paste(time_image, (320, 210))
        self.image.paste(music_image, (0, 0))

    def slide_music_text(self, music_image, obj, text, y_position, velocity):
        """
        Draw the music information and slide it if too long.

        Input:
            -music_image: music image object
            -obj: objects x position
            -text: text to draw
            -y_position: text's y-position
            -velocity: velocity of moving text if needed, pixels/refresh
        """

        music_draw = ImageDraw.Draw(music_image)
        music_draw.rectangle((0, y_position, 480, y_position + 70), fill=255)

        music_x, _ = music_draw.textsize(text, font=self.font60)
        if music_x > 480:
            obj += velocity

            if obj > music_x - 480:
                obj = 0

        music_draw.text((-obj, y_position), text, font=self.font60, fill=0)

        return music_image, obj

    def draw(self, mode, delay=5):
        """
        Draw to screen based on current display mode.

        Input:
            -mode: mode of drawing, 0 full, 1 partial
            -delay: time to wait for new draw
        """

        # want to update time_delay below because draw can take some time
        if self.get_time() > self.time_delay:
            self.epd.init(mode)  # activate screen for drawing

            self.draw_kernel(mode)

            self.sleep()  # put screen to sleep

            self.time_delay = self.get_time() + delay * KILO

    def draw_kernel(self, mode):
        """
        Drawing kernel.

        Input:
            -mode: mode of drawing
        """

        self.image = self.image.rotate(180)

        if mode == 1:
            logging.info("Partial update")
            self.clear(1)
            self.epd.display_1Gray(self.epd.getbuffer(self.image))
        else:
            logging.info("Full update")
            self.clear(0)
            self.epd.display_4Gray(self.epd.getbuffer_4Gray(self.image))

        self.image = self.image.rotate(
            180
        )  # rotate back (not efficient, find better way later)

    def clear(self, mode=0):
        """
        Clear the screen and set mode.
        """

        logging.info("Clear")
        self.mode = mode
        self.epd.init(mode)
        self.epd.Clear(0xFF, mode)

    def sleep(self):
        """
        Put screen to sleep.
        """

        logging.info("Goto Sleep...")
        self.epd.sleep()

    def shutdown(self, text="Shutdown screen"):
        """
        Shutdown screen.

        Input:
            -text: text to log
        """

        logging.info(text)
        epd3in7.epdconfig.module_exit()

    def reset_x_movement(self):
        """
        Reset the x_movement of text.
        """

        self.artists_x = 0
        self.album_x = 0
        self.track_x = 0

    def get_time(self):
        """
        Get current time in ms
        """

        return time.time_ns() / MEGA  # ns to ms

    def reset_time(self):
        """
        Reset time variable
        """

        self.time_delay = 0
