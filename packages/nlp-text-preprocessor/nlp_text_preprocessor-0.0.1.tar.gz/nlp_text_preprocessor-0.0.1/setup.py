from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'Natural language processing package'
LONG_DESCRIPTION = 'This package deals with emojis, abbreviations, contraction words etc. by removing or replacing them.'

# Setting up
#data_files=[('data', ['nlp_lib/data/abbreviations.json']),]
setup(
    name="nlp_text_preprocessor",
    version=VERSION,
    author="Afnanurrahim Ansari",
    author_email="afnanurrahim150102@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    include_package_data=True,
    package_data={'nlp_preprocessor': ['nlp_lib/data/abbreviations.json', 'nlp_lib/data/contractions.json','nlp_lib/data/emoji_emotion.csv']},
    install_requires=['pandas','emoji','wordfreq'],
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