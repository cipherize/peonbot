from munch import munchify
import yaml

ifh = open("config.yaml", "r")

config = munchify(yaml.safe_load(ifh))
