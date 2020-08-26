import pathlib

from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name="dash-transcrypt",
    version="0.0.1",
    author="Emil Haldrup Eriksen",
    packages=["dash_transcrypt"],
    url="https://github.com/thedirtyfew/dash-transcrypt/",
    include_package_data=True,
    license="MIT",
    long_description=README,
    long_description_content_type="text/markdown",
    description="Transcrypt bindings for Plotly Dash.",
    install_requires=["transcrypt"],
    classifiers=[
        "Programming Language :: Python :: 3",
        'Framework :: Dash',
    ],
)
