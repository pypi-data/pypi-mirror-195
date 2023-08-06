import sys
from setuptools import setup

if 'sdist' not in sys.argv:
    sys.exit(
        "\n*** Please install the `btrack` package "
        "instead of `napari-btrack-reader`) ***\n"
    )

setup(
    name="napari-btrack-reader",
    version="1.0.2",
    long_description=(
        "The functionality of this package has been integrated into "
        "[BayesianTracker](https://github.com/quantumjot/BayesianTracker)."
    )
)
