import setuptools

# with open("README.md", "r", encoding = "utf-8") as fh:
#     long_description = fh.read()

dependencies = ["selenium", "selenium_stealth", "webdriver-manager"]

setuptools.setup(
    name = "driver_h",
    version = "0.1.2",
    author = "Yaroslav O.",
    author_email = "publicyaro1@gmail.com",
    # description = "This package return driver that prevents detection chrome driver while using selenium",
    # long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/Yaroslav1233/driver-h",
    # project_urls = {
    #     "Bug Tracker": "package issues URL",
    # },
    install_requires = dependencies,
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir = {"": "src"},
    packages = setuptools.find_packages(where="src"),
    python_requires = ">=3.6"
)

