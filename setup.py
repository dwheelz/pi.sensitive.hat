"""Sets up RTIMULib and sense hat, invoke when in a venv to save yourself sadness"""

import os
from pathlib import Path
import subprocess

from setuptools import setup, find_packages


def read(fname: str):
    """Reads a file"""
    return open(os.path.join(os.path.dirname(__file__), fname), encoding="UTF-8").read()

def _setup_rtimulib():
    """Config RTIMULib (its a right pain)"""
    rtimlib_cwd = Path("src", "RTIMULib", "Linux", "python").absolute()
    subprocess.check_call(["python", "setup.py", "build"], cwd=rtimlib_cwd)
    subprocess.check_call(["python", "setup.py", "install"], cwd=rtimlib_cwd)

_setup_rtimulib()

setup(
    name="pisensitivehat",
    version="0.0.1",
    author="Jumbo Bumbo",
    long_description=read('README.md'),
    license="BSD",
    python_requires='>=3.9',
    packages=find_packages(),
    install_requires=read("requirements.txt"),
    entry_points={
        "console_scripts": [
            'temps = src.sense_app.main:temps',
            'creeper = src.sense_app.main:creeper_face'
            'cleardisplay = src.sense_app.main:clear_display'
        ]
    },
    include_package_data=True
)
