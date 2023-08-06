from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "Readme.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

with open("version.txt", "r") as file:
    VERSION = file.readlines()[0]

DESCRIPTION = 'cli for ram monitoring'

# Setting up
setup(
    name="memota",
    version=VERSION,
    author="Bovur",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['psutil==5.9.4', 'python-daemon==2.3.2', 'click==8.1.3', 'lockfile==0.12.2', 'ram'],
    keywords=['python', 'ram', 'monitoring'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    entry_points={
        'console_scripts': [
            'memota = memota.memota:cli',
        ]
    }
)