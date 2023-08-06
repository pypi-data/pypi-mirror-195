from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.2'
DESCRIPTION = 'This will automate the job application process to seek.com'
LONG_DESCRIPTION = """
      Automation software like this can be a valuable tool for job seekers
      looking to streamline their job application process on Seek.com.
      These tools can save job seekers time, reduce errors in their applications,
      and increase their chances of landing an interview.
"""

# Setting up
setup(
    name="JobHunter",
    version=VERSION,
    author="Reamon Sumapig (DSoftwareArtist)",
    author_email="<29reamonsumapig@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[
      'python-dotenv',
      'black',
      'requests',
      'selenium',
      'chromedriver-autoinstaller',
      'pydantic[email]',
      'beautifulsoup4',
      'lxml',
      'gspread',
      'oauth2client'
    ],
    keywords=['python', 'jobhunter'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Customer Service",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix ",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)