###  Start of fixing import paths
import os, sys, inspect
import sublime
BASE_PATH = os.path.abspath(os.path.dirname(__file__))
PACKAGES_PATH = sublime.packages_path() or os.path.dirname(BASE_PATH)
sys.path += [BASE_PATH]
### End of fixing import paths

import base


class Grep (base.Base):
    pass

engine_class = Grep
