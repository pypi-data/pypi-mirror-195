from setuptools import setup, find_packages
import codecs
import os

VERSION = '1.0'
DESCRIPTION = 'package for file storage'
with open("README.md",'r') as fh:
    LONG_DESCRIPTION = fh.read()
# Setting up
setup(
    name="sskp",
    version=VERSION,
    author="Sahil",
    author_email="sahilapte14@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['ngitkmit','store files', 'database', 'store', 'file', 'ngit','mongo','kmit'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)