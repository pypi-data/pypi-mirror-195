from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'NLP Preprocessing By XComsians'
LONG_DESCRIPTION = 'i have created this library that you just have to set your data with the parameters that which type of preprocessing you need on your data. if you pass empty data then preprocessing will apply which is set by default you need to install library emoji , pandas , numpy , nltk , and all other basics to run this.'

# Setting up
setup(
    name="XComsians",
    version=VERSION,
    author="Engr. Bilal Ahmad",
    author_email="bilalahmad176176@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'XComsians', 'NLP Preprocessing', 'preprocessing by XComsians', 'Engr. Bilal Ahmad'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)