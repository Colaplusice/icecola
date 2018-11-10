
import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="python-utils",
    version="0.0.1",
    author="Colaplusice",
    author_email="fjl2401@163.com",
    description="A  util package for python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Colaplusice/python-utils",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)