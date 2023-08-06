import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

VERSION = '0.1.0'
PACKAGE_NAME = 'vennoverlap'
AUTHOR = 'Alva Rani James'
AUTHOR_EMAIL = 'alvarani@gmail.com'
URL = 'https://github.com/ranijames/Data_overlap'

LICENSE = 'MIT License'
DESCRIPTION = 'vennoverlap is a package which would help to generate lists of overlaps between columns of given dataframe. eg. If you plot a venn diagram between 2 or more list, it will not provide you the values. But this library will gives you the value'
LONG_DESCRIPTION = (HERE / "README.md").read_text()
LONG_DESC_TYPE = "text/markdown"

INSTALL_REQUIRES = [
         'pandas',
        'itertools'
]


PYTHON_REQUIRES = ">=3.8"
setup(name=PACKAGE_NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      long_description_content_type=LONG_DESC_TYPE,
      author=AUTHOR,
      license=LICENSE,
      author_email=AUTHOR_EMAIL,
      url=URL,
      install_requires=INSTALL_REQUIRES,
      packages=find_packages()
      )