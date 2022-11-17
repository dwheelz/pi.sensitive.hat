import os
from pathlib import Path
from setuptools import setup, find_packages
import subprocess



def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

# Config RTIMULib (its a right pain)
def _setup_rtimulib():
    rtimlib_cwd = Path("src", "RTIMULib", "Linux", "python").absolute()
    subprocess.check_call(["python", "setup.py", "build"], cwd=rtimlib_cwd)
    subprocess.check_call(["python", "setup.py", "install"], cwd=rtimlib_cwd)

_setup_rtimulib()

setup(
    name="pi.sensitive.hat",
    author="Jumbo Bumbo",
    long_description=read('README.md'),
    license="BSD",
    python_requires='>=3.9',
    packages=find_packages(),
    install_requires=read("requirements.txt"),
    entry_points=dict(console_scripts=['temps = src.sense_app.main:temps'])
)
