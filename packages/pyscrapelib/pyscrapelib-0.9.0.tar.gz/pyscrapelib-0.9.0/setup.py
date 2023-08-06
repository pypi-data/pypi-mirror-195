from setuptools import setup, find_packages

VERSION = '0.9.0'
DESCRIPTION = 'PyScrapeLib is a Python library designed to make it easy to gather information and data from other Python libraries.'
LONG_DESCRIPTION = 'With PyScrapeLib, you can easily extract relevant information from a wide range of libraries and use it for your own purposes. Whether you need to gather data for research, build a new application, or simply explore the capabilities of other libraries, PyScrapeLib can help you get the information you need.'

# Setting up
setup(
    name="pyscrapelib",
    version=VERSION,
    author="Nick",
    author_email="nick.faltermeier@gmx.de",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python'],
    classifiers=[
        "Operating System :: Microsoft :: Windows",
    ]
)