import os
from setuptools import setup, find_packages

setup(
    name="flutterator",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    author="Lorenzo Busi",
    author_email="info@lorenzobusi.it",
    description="CLI per creare progetti Flutter con struttura personalizzata - by GetAutomation",
    long_description=open("README.md").read() if os.path.exists("README.md") else "",
    long_description_content_type="text/markdown",
    py_modules=["flutter_cli"],
    install_requires=[
        "click>=8.0.0",
    ],
    entry_points={
        "console_scripts": [
            "flutterator=flutter_cli:create",
        ],
    },
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)