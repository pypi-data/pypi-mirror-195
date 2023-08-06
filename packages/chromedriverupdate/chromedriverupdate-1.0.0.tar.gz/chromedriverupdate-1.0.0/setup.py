import os

import pkg_resources
from setuptools import setup, find_packages

setup(
    name="chromedriverupdate",
    version='1.0.0',
    description="Update chrome driver",
    long_description=open(os.path.join(os.path.dirname(__file__), "README.md"), encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    python_requires=">=3.7",
    author="cghn",
    url="https://github.com/kirikumo/chromedriverupdate",
    license="GPLv3",
    packages=find_packages(),
    install_requires=[
        str(r)
        for r in pkg_resources.parse_requirements(
            open(os.path.join(os.path.dirname(__file__), "requirements.txt"))
        )
    ],
    include_package_data=True,
)