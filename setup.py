import setuptools
import gazi

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='gazi',
    version=gazi.__version__,
    author="Andreas Arnesson",
    author_email="aar@bth.se",
    description="Running Jplag on scale",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/andreasarne/gazi",
    packages=setuptools.find_packages(exclude=[
        "tests.*",
        "tests"
    ]),
    python_requires='>=3.6',
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
 )