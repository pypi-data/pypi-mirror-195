import io
import os

from setuptools import find_packages, setup


def read(*paths, **kwargs):
    """Read the contents of a text file safely.
    >>> read("README.md")
    ...
    """

    content = ""
    with io.open(
        os.path.join(os.path.dirname(__file__), *paths),
        encoding=kwargs.get("encoding", "utf8"),
    ) as open_file:
        content = open_file.read().strip()

    return content


def read_requirements(path):
    return [
        line.strip()
        for line in read(path).split("\n")
        if not line.startswith(('"', "#", "-", "git+"))
    ]


setup(
    name="Flare_Utilities",
    version="0.0.3",
    description="""
        Flare Utilities having support libraries for Flare-BDD framework for reporting purposes.
    """,
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="Aravinth Alliraj",
    packages=find_packages("Reporting"),
    package_dir={"": "Reporting"},
    install_requires=["pyarmor"],
    classifiers=[
        "Intended Audience :: Developers",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
    ],
)
