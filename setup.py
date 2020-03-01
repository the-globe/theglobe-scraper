# This is for a feature package!
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="scraper",
    version="0.0.1",
    author="Santiago Martinez-Avial, Marvin Willms",
    author_email="santiago.martinez@code.berlin, marvin.willms@code.berlin",
    description="A package for scraping and inserting News to a MongoDB",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Mavial/theglobescraper",
    packages=setuptools.find_packages(),
    install_requires=[
        'pymongo >= 3.10.1',
        'colorlog >= 4.1.0',
        'scrapy >= 1.8.0',
        'redis >= 3.4.1'

    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        # "License :: OSI Approved :: MIT License",
        # "Operating System :: OS Independent",
    ],
    python_requires='>=3.7.4',
)