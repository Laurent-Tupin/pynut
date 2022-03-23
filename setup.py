import pathlib
from setuptools import setup, find_packages
import pyNut

# The text of the README file
ME_PATH = pathlib.Path(__file__).parent
README = (ME_PATH / "README.md").read_text()

# This call to setup() does all the work
setup(
    name    = "pynut",
    version = pyNut.__version__,
    description = "Function easing life :)",
    long_description = README,
    long_description_content_type = "text/markdown",
    url = "https://github.com/LaurentTupin/pynut",
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
    install_requires = ["pandas", "paramiko", "beautifulsoup4", "exchangelib", "openpyxl","psutil",
                        "pyodbc", "PyQt5", "pywin32", "selenium", "xlrd==1.2.0", "XlsxWriter", "xlwings"]
    #entry_points={"console_scripts": ["EXEnameFile=FolderName.__main__:main"]},
)
