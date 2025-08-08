#!/usr/bin/env python3
"""
Setup script for Quantitative Bets
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="quantitative-bets",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A comprehensive sports betting analysis platform with advanced statistical analysis and interactive dashboards",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/Quantitative-Bets",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
            "quantitative-bets=main:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="sports betting analysis statistics dashboard nba nfl nhl wnba",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/Quantitative-Bets/issues",
        "Source": "https://github.com/yourusername/Quantitative-Bets",
        "Documentation": "https://github.com/yourusername/Quantitative-Bets#readme",
    },
)
