import sys
import os
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

        self.font64 = ImageFont.truetype(
            os.path.join(config["fontdir"], config["font"]), 64
        )
        self.font60 = ImageFont.truetype(
            os.path.join(config["fontdir"], config["font"]), 60
        )
        self.mode = mode

        self.artists_x = 0
        self.album_x = 0
        self.track_x = 0

        try:
            self.epd = epd3in7.EPD()
            logging.info("Initialise")
            self.clear()

            self.image = Image.new("1", (self.epd.height, self.epd.width), 255)

        except IOError as e:
            logging.info(e)

        except KeyboardInterrupt:
            logging.info("ctrl + c")
            epd3in7.epdconfig.module_exit()

    def __enter__(self):
        """ """

        return self

    def __exit__(self, type, value, traceback):
        """
        Soft destruction of object.
        """

        self.clear()

        logging.info("Goto Sleep...")
        self.epd.sleep()

        logging.info("Shutdown screen")
        epd3in7.epdconfig.module_exit()

    def update_full(self, spotify):
        """
        Update screen - full refresh.

        Input:
            -spotify: spotify object
        """

        logging.info("Draw track art")
        self.clear()

        image = ImageOps.grayscale(spotify.image)
        image.thumbnail((200, 200), Image.ANTIALIAS)
        self.image.paste(image, (0, 0))

    def update_partial(self, spotify, velocity=0):
        """
        Update screen - partial refresh

        Input:
            -spotify: spotify object
            -velocity: velocity of moving text if needed, pixels/refresh
        """

        logging.info("Partial update")
        if self.mode == 0:
            self.clear(1)  # 1 Gray mode

        time_image = Image.new("1", (200, 80), 255)
        time_draw = ImageDraw.Draw(time_image)
        time_draw.rectangle((20, 8, 200, 272), fill=255)
        time_draw.text((20, 8), time.strftime("%H:%M"), font=self.font64, fill=0)

        music_image = Image.new("1", (280, 200), 255)
        # self.draw()  # draw blank first, make nicer

        music_image, self.artists_x = self.draw_music_text(
            music_image, self.artists_x, spotify.artists, 0, velocity
        )
        music_image, self.album_x = self.draw_music_text(
            music_image, self.album_x, spotify.album, 70, velocity
        )
        music_image, self.track_x = self.draw_music_text(
            music_image, self.track_x, spotify.track, 140, velocity
        )

        self.image.paste(time_image, (0, 200))
        self.image.paste(music_image, (210, 0))

    def draw_music_text(self, music_image, obj, text, y_position, velocity):
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
        music_draw.rectangle((0, y_position, 280, y_position + 60), fill=255)

        music_x, _ = music_draw.textsize(text, font=self.font60)
        if music_x > 280:
            obj += velocity

            if obj > music_x - 280:
                obj = 0

        music_draw.text((-obj, y_position), text, font=self.font60, fill=0)

        return music_image, obj

    def draw(self):
        """
        Draw to screen based on current display mode.
        """

        self.image = self.image.rotate(180)
        if self.mode == 1:
            self.epd.display_1Gray(self.epd.getbuffer(self.image))
        else:
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

    def reset_x_movement(self):
        """
        Reset the x_movement of text.
        """

        self.artists_x = 0
        self.album_x = 0
        self.track_x = 0
