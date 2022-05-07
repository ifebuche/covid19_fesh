<<<<<<< HEAD
# -*- coding: utf-8 -*-
=======
>>>>>>> 27dd9875f98c51b82553091a9dbcf027191524ef
"""Activate virtualenv for current interpreter:

Use exec(open(this_file).read(), {'__file__': this_file}).

This can be used when you must use an existing Python interpreter, not the virtualenv bin/python.
"""
import os
import site
import sys

try:
<<<<<<< HEAD
    abs_file = os.path.abspath(__file__)
except NameError:
    raise AssertionError("You must use exec(open(this_file).read(), {'__file__': this_file}))")

bin_dir = os.path.dirname(abs_file)
base = bin_dir[: -len("Scripts") - 1]  # strip away the bin part from the __file__, plus the path separator

# prepend bin to PATH (this file is inside the bin directory)
os.environ["PATH"] = os.pathsep.join([bin_dir] + os.environ.get("PATH", "").split(os.pathsep))
os.environ["VIRTUAL_ENV"] = base  # virtual env is right above bin directory

# add the virtual environments libraries to the host python import mechanism
prev_length = len(sys.path)
for lib in "..\Lib\site-packages".split(os.pathsep):
    path = os.path.realpath(os.path.join(bin_dir, lib))
    site.addsitedir(path.decode("utf-8") if "" else path)
sys.path[:] = sys.path[prev_length:] + sys.path[0:prev_length]

sys.real_prefix = sys.prefix
sys.prefix = base
=======
    __file__
except NameError:
    raise AssertionError("You must use exec(open(this_file).read(), {'__file__': this_file}))")

# prepend bin to PATH (this file is inside the bin directory)
bin_dir = os.path.dirname(os.path.abspath(__file__))
os.environ["PATH"] = os.pathsep.join([bin_dir] + os.environ.get("PATH", "").split(os.pathsep))

base = os.path.dirname(bin_dir)

# virtual env is right above bin directory
os.environ["VIRTUAL_ENV"] = base

# add the virtual environments site-package to the host python import mechanism
IS_PYPY = hasattr(sys, "pypy_version_info")
IS_JYTHON = sys.platform.startswith("java")
if IS_JYTHON:
    site_packages = os.path.join(base, "Lib", "site-packages")
elif IS_PYPY:
    site_packages = os.path.join(base, "site-packages")
else:
    IS_WIN = sys.platform == "win32"
    if IS_WIN:
        site_packages = os.path.join(base, "Lib", "site-packages")
    else:
        site_packages = os.path.join(base, "lib", "python{}.{}".format(*sys.version_info), "site-packages")

prev = set(sys.path)
site.addsitedir(site_packages)
sys.real_prefix = sys.prefix
sys.prefix = base

# Move the added items to the front of the path, in place
new = list(sys.path)
sys.path[:] = [i for i in new if i not in prev] + [i for i in new if i in prev]
>>>>>>> 27dd9875f98c51b82553091a9dbcf027191524ef
