import os
from binsync import __version__ as _VERSION

VERSION = _VERSION
PLUGIN_DIR = os.path.dirname(os.path.realpath(__file__))
IDA_DIR = os.path.abspath(os.path.join(PLUGIN_DIR, "..", ".."))
UI_DIR = os.path.join(PLUGIN_DIR, "ui")
# THEMES_DIR = os.path.join(PLUGIN_DIR, 'themes')
