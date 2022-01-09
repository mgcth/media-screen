import json
import pathlib
import os


file = os.path.join(pathlib.Path(__file__).parent.resolve(), "config.json")

with open(file, "r") as f:
    config = json.load(f)
