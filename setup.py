#!/usr/bin/env python3
"""
SynapseStats - Communication Analytics for THE_SYNAPSE

Setup script for pip installation.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_path = Path(__file__).parent / "README.md"
if readme_path.exists():
    long_description = readme_path.read_text(encoding='utf-8')
else:
    long_description = "Communication analytics for THE_SYNAPSE"

setup(
    name="synapsestats",
    version="1.0.0",
    author="Atlas (Team Brain)",
    author_email="metaphyllc@example.com",
    description="Communication analytics for THE_SYNAPSE - Track message volume, response times, agent activity, and more",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DonkRonk17/SynapseStats",
    
    py_modules=["synapsestats"],
    
    python_requires=">=3.7",
    
    # Zero dependencies - pure Python standard library!
    install_requires=[],
    
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Communications",
        "Topic :: System :: Monitoring",
        "Topic :: Utilities",
    ],
    
    keywords="synapse analytics communication monitoring team-brain",
    
    entry_points={
        "console_scripts": [
            "synapsestats=synapsestats:main",
        ],
    },
    
    project_urls={
        "Bug Reports": "https://github.com/DonkRonk17/SynapseStats/issues",
        "Source": "https://github.com/DonkRonk17/SynapseStats",
        "Documentation": "https://github.com/DonkRonk17/SynapseStats#readme",
    },
)
