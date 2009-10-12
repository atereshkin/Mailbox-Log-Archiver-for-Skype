#!/usr/bin/env python
# Builds a distribution using bbfreeze (works on Windows and Linux)
# It may be necessary for some python versions on windows to copy python2(4,5,6).dll
# in the distribution directory.
# Also for some versions of python Microsovt Visual C++ redistributable package required.
import shutil

from os import chdir
from bbfreeze import Freezer

f = Freezer("mlas", includes=("sip", ))
f.addScript("src/plugin.py", gui_only=True)
f()    # starts the freezing process
