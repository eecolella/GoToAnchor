###  Start of fixing import paths
import os, sys, inspect
import sublime
BASE_PATH = os.path.abspath(os.path.dirname(__file__))
PACKAGES_PATH = sublime.packages_path() or os.path.dirname(BASE_PATH)
sys.path += [BASE_PATH]
### End of fixing import paths

import base


class FindStr (base.Base):
    """Uses Windows built-in findstr command."""

    def _command_line(self, query, folders):
        return " ".join([
            self.path_to_executable,
            self.mandatory_options,
            self.common_options,
            '"/d:%s"' % ":".join(folders),
            query,
            "*.*"
            ])


engine_class = FindStr
