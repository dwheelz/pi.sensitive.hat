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
    name="sense_app",
    version="0.0.1",
    author="Jumbo Bumbo",
    long_description=read('README.md'),
    license="BSD",
    python_requires='>=3.9',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=read("requirements.txt"),
    entry_points={
        "console_scripts": [
            'temps = sense_app.main:temps',
            'creeper = sense_app.main:creeper_face',
            'cleardisplay = sense_app.main:clear_display',
            'randompattern = sense_app.main:gen_random_pattern',
            'lowlight = sense_app.main:enable_low_light',
            'normallight = sense_app.main:disable_low_light',
        ]
    },
    include_package_data=True
)
