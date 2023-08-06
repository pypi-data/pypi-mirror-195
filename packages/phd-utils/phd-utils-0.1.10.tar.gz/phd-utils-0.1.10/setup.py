import subprocess
import sys
from setuptools import setup, find_packages

# Define the required system package
required_packages = ['openexr']

# Use subprocess to check if the required package is installed
try:
    subprocess.check_call(['dpkg', '-s'] + required_packages,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
except subprocess.CalledProcessError:
    print('Error: the required system package ({}) is not installed. '
          'Please install it manually.'.format(required_packages),
          file=sys.stderr)
    sys.exit(1)

setup(
    name='phd-utils',
    version='0.1.10',
    description='A collection of utilities for PhD students',
    author='Henrique Weber',
    packages=find_packages(),
    install_requires=[
        'skylibs',
        'openexr',
        'opencv-python',
        'numpy',
    ],
)
