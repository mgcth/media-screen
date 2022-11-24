"""Define constants."""
import json


KILO = 1000
MEGA = 1000000

FILE = "config.json"

with open(FILE, "r") as f:
    CONFIG = json.load(f)
