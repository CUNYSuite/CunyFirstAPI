import setuptools

requires = [
    'requests>=2.21.0',
    'lxml>=4.2.1',
    'beautifulsoup4>=4.6.0'
]


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cunyfirstapi",
    version="0.0.8",
    author="Ehud Adler",
    author_email="ehud.adler62@qmail.cuny.edu",
    description="A simple CUNYFIRST python API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CUNYSuite/CunyFirstAPI",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)