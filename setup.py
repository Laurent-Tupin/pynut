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
    install_requires = ["pandas==1.1.3", "paramiko==2.6.0", "beautifulsoup4==4.7.1", "exchangelib==4.7.2",
                        "openpyxl==3.0.5","psutil==5.9.0", "pyodbc==4.0.32", "pywin32==303", "selenium==3.141.0",
                        "xlrd==1.2.0", "XlsxWriter==1.3.5", "xlwings==0.20.8", "pyarrow", "fastparquet"]
    #entry_points={"console_scripts": ["EXEnameFile=FolderName.__main__:main"]},
)
