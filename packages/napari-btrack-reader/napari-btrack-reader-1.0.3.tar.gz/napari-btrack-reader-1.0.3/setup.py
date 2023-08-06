import sys
from setuptools import setup

if 'sdist' not in sys.argv:
    sys.exit(
        "\n*** Please install the `btrack` package "
        "instead of `napari-btrack-reader`) ***\n"
    )

description = (
    "The functionality of this package has been integrated into "
    "https://github.com/quantumjot/BayesianTracker."
)

setup(
    name="napari-btrack-reader",
    version="1.0.3",
    description=description,
    long_description=description,
)
