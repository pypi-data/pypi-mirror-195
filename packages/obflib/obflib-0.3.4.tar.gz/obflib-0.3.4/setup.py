# SPDX-FileCopyrightText: 2022 Freemelt AB <opensource@freemelt.com>
#
# SPDX-License-Identifier: Apache-2.0
# -*- coding: utf-8 -*-

import re
from setuptools import setup, find_packages
from _version import __version__


with open("README.md") as readme_file:
    long_description = readme_file.read()


def convert_debian_version_to_python(match):
    print(match)
    if match.group(3):
        return f"{match.group(1)}+{match.group(3)}"
    else:
        return match.group(1)


__version__ = re.sub(
    r"(.*)(\+deb\d+)~?(git\.[^.]*\.[^.]*)?(\.1)",
    convert_debian_version_to_python,
    __version__,
)

setup(
    name="obflib",
    version=__version__,
    license="apache-2.0",
    author="Freemelt AB",
    author_email="opensource@freemelt.com",
    maintainer="Freemelt AB",
    maintainer_email="opensource@freemelt.com",
    description="Python library for verifying, reading and manipulating OBF files"
    " for use in metal 3D printers from Freemelt AB",
    keywords="obf openbuildfile freemelt",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/freemelt/openmelt/obflib-python",
    packages=find_packages(exclude=["tests"]),
    package_data={
        "obflib": ["py.typed"],
        "openbuildfile": [
            "schemas/v*/*.json",
            "examples/*.obf",
            "examples/standard/buildProcessors/bob/*",
        ],
    },
    install_requires=[
        "click>=7.0",
        "jsonschema>=3.2.0",
        "semantic-version>=2.8.5",
        "PyYAML>=3.13",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "obftool = obflib.cli:main",
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
