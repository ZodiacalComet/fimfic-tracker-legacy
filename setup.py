# This setup.py file is a combination of:
#
# + "setup.py (for humans)", as the whole base.
#       https://github.com/navdeep-G/setup.py/blob/master/setup.py
#
# + "discord.py", git metadata on pre-release versions.
#       https://github.com/Rapptz/discord.py/blob/master/setup.py
import os

from setuptools import find_packages, setup

# Package meta-data.
NAME = "fimfic-tracker"
DESCRIPTION = "An unnecessary CLI application for tracking stories on Fimfiction."
URL = "https://github.com/ZodiacalComet/fimfic-tracker"
AUTHOR = "ZodiacalComet"
EMAIL = "ZodiacalComet@gmail.com"
REQUIRES_PYTHON = ">=3.7.0"

# Root directory and module directory
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_SLUG = NAME.lower().replace("-", "_").replace(" ", "_")

with open(os.path.join(ROOT_DIR, "README.md")) as fd:
    LONG_DESCRIPTION = fd.read()

with open(os.path.join(ROOT_DIR, "requirements.txt")) as fd:
    REQUIRED = fd.read().splitlines()

# Acquiring version from __version__.py file.
VERSION_FILE = os.path.join(ROOT_DIR, PROJECT_SLUG, "__version__.py")

with open(VERSION_FILE) as fd:
    exec(compile(fd.read(), VERSION_FILE, "exec"))

# Appending git metadata to pre-release versions
if __version__.endswith(("a", "b", "rc")):  # noqa: F821
    try:
        from subprocess import run

        out = run(["git", "rev-list", "--count", "HEAD"], capture_output=True).stdout
        if out:
            __version__ += out.decode("utf-8").strip()  # noqa: F821

        out = run(["git", "rev-parse", "--short", "HEAD"], capture_output=True).stdout
        if out:
            __version__ += "+g" + out.decode("utf-8").strip()  # noqa: F821
    except Exception:
        pass


setup(
    name=NAME,
    version=__version__,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    entry_points={"console_scripts": ["fimfic-tracker=fimfic_tracker.__main__:main"]},
    install_requires=REQUIRED,
    include_package_data=True,
    license="Unlicense",
)
