#coding:utf8
__author__ = 'dk'
import setuptools
long_desp = \
'''
A python lib for encrypted traffic classification.\n
Homepage : https://github.com/jmhIcoding/traffic_classification_utils \n
'''
with open("README-en.md", "r",encoding="utf8") as fh:
    long_desp = fh.read()

setuptools.setup(
    name="flowspot",
    version="1.2",
    author="Minghao Jiang",
    author_email="jiangminghao@iie.ac.cn",
    description="A python lib to parse traffic flow information from pcaps",
    url="https://github.com/jmhIcoding/traffic_classification_utils",
    long_description=long_desp,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
