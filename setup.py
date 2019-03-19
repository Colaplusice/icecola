import io
import re

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with io.open('__init__.py', 'rt', encoding='utf8') as f:
    version = re.search(r'__version__ = \'(.*?)\'', f.read()).group(1)

setuptools.setup(
    name="icecola",
    version=version,
    author="Colaplusice",
    author_email="fjl2401@163.com",
    description="A  util package for python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Colaplusice/icecola",
    packages=setuptools.find_packages(),
    package_dir={'crawler_utils': 'crawler_utils'},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'pymongo>=3.7',
        'pendulum>=2.0',
        'peewee>=3.9',
        'Flask>=1.0',
    ],
    python_requires='>=3.5',
)
