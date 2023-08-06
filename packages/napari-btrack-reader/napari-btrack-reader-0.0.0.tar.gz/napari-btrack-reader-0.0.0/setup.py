import sys
from setuptools import setup

if 'sdist' not in sys.argv:
    sys.exit(
        "\n*** Please install the `btrack` package "
        "instead of `napari-btrack-reader`) ***\n"
    )

setup(
    name="napari-btrack-reader"
)
