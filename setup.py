""" Setup.py """
import codecs
import os

from setuptools import find_packages, setup

#INSTALL_REQUIRES = ["attrs>=20.3.0", "jsonpath-rw>=1.4.0"]
#EXTRAS_REQUIRE = {"docs": ["sphinx"], "tests": ["coverage[toml]", "pytest"]}
INSTALL_REQUIRES = []
HERE = os.path.abspath(os.path.dirname(__file__))

def read(*parts):
    """ Read the contents of a text file """
    with codecs.open(os.path.join(HERE, *parts), "rb", "utf-8") as file:
        return file.read()


setup(
    name="lambda_rest_router",
    version="0.0.2",
    url="https://github.com/stojce/lambda-rest-router",
    description="AWS Lambda REST Router for AWS API Gateway",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="Stojce Slavkovski",
    author_email="stojce@me.com",
    packages=find_packages(where="lambda_rest_router"),
    package_dir={"": "lambda_rest_router"},
    include_package_data=True,
    install_requires=INSTALL_REQUIRES,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
