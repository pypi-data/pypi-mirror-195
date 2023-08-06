import setuptools

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "aiopagination",
    version = "1.0.2",
    author = "Rakhmatullo Shermatov",
    author_email = "milodcomposer@gmail.com",
    description = "A library designed to build pagination using the aiogram library",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/Raxmatillo/aiopagination",
    project_urls = {
        "Bug Tracker": "https://github.com/Raxmatillo/aiopagination/issues",
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir = {"": "src"},
    packages = setuptools.find_packages(where="src"),
    python_requires = ">=3.6"
)
