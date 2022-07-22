import pathlib
from setuptools import setup, find_packages
import pyNut

# The text of the README file
ME_PATH = pathlib.Path(__file__).parent
README = (ME_PATH / "README.md").read_text()
NAME = "pynut"
VERSION = pyNut.__version__

# This call to setup() does all the work
setup(
    name = NAME,
    version = VERSION,
    description = "Function easing life :)",
    long_description = README,
    long_description_content_type = "text/markdown",
    url = "https://github.com/Laurent-Tupin/pynut",
    author = "Laurent Tupin",
    author_email = "laurent.tupinn@gmail.com",
    license = "Copyright 2022-2035",
    classifiers=[
        "License :: Free For Home Use",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    packages = find_packages(exclude = ("test",)),
    include_package_data = True,
    install_requires = ["pynut-API==2.1.4", "pynut-DB==2.1.1", "pynut-Email==2.1.2", "pynut-ftp==2.1.3"]
    #entry_points={"console_scripts": ["EXEnameFile=FolderName.__main__:main"]},
)
