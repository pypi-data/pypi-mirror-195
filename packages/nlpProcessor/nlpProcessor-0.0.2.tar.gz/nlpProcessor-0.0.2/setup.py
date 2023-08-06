from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.2'
DESCRIPTION = 'Natural language processing package'
LONG_DESCRIPTION = 'This package deals with emojis, abbreviations, contraction words etc. by removing or replacing them.'

# Setting up
setup(
    name="nlpProcessor",
    version=VERSION,
    author="Afnanurrahim Ansari",
    author_email="afnanurrahim150102@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    include_package_data=True,
    package_data={'': ['data/*.json', 'data/*.csv']},
    install_requires=['pandas','emoji'],
    keywords=['nlp','natural language processing','processor'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)