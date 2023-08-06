import codecs
import os
from setuptools import setup, find_packages

# these things are needed for the README.md show on pypi
here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()


VERSION = '1.0.1'
DESCRIPTION = 'An industrial data augmentation library '
LONG_DESCRIPTION = 'You can use any methods of industrial data augmentation in your python file by installing our library,' \
                   'you can also download the platform(Idap, an executable file) to finish augmentation task conveniently.'

# Setting up
setup(
    name="idaly",
    version=VERSION,
    author="chenking",
    author_email="",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'data augmentation', 'industrial big data'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)