from setuptools import setup
import platform

base = (["requests==2.27.1", "spotipy==2.19.0", "Pillow==9.0.1", "pylast==4.5.0"],)

setup(name="media_screen", install_requires=base)
