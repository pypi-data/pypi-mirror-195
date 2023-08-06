from setuptools import setup, find_packages
import os

VERSION = '0.1.1'
DESCRIPTION = 'A bare-bones Python library for converting currencies using the conversion rates of NBR (National Bank of Romania)'

# Setting up
setup(
    name="cursbnr",
    version=VERSION,
    author="Katistix Studios (Paul Tal)",
    author_email="<katistix.studios@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'currency', 'exchange', 'romania'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
