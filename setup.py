#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This module contains the build information for this project."""

import setuptools  # type: ignore[import-untyped]

# open readme
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    author="Joris Schellekens",
    author_email="joris.schellekens.1989@gmail.com",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Text Processing :: Markup :: PDF",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    description="borb is a library for reading, creating and manipulating PDF files in python.",
    extras_require={
        "dev": [
            "black",
            "mypy",
            "pydocstyle",
        ],
        "docs": [
            "sphinx",
            "sphinx-rtd-theme",
        ],
        "full": [
            "cryptography",
            "ffmpeg-python",
            "fonttools",
            "matplotlib",
            "Pillow",
            "python-barcode",
            "py_avataaars",
            "requests",
            "segno",
        ],
    },
    include_package_data=True,
    install_requires=[],
    keywords=["pdf", "pdf-generation", "pdf-processing", "borb"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    name="borb",
    packages=setuptools.find_packages(include=["borb", "borb.*"]),
    project_urls={
        "Source": "https://github.com/borb-pdf/borb",
        "Tracker": "https://github.com/borb-pdf/borb/issues",
    },
    python_requires=">=3.6",
    url="https://github.com/borb-pdf/borb",
    version="3.0.6",
)
