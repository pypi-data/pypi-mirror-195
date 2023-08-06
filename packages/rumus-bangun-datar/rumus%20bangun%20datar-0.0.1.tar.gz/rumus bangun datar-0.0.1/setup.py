from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'rumus bangun datar'
LONG_DESCRIPTION = 'kumpulan rumus bangun datar'

# Setting up
setup(
    name="rumus bangun datar",
    version=VERSION,
    author="Muhammad Shobirin Halik",
    author_email="<msaammss03@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    keywords=['python', 'rumus bangun datar'],
    classifiers=[
        "Programming Language :: Python :: 3",
    ]
)