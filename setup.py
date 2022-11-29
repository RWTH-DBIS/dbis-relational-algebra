import pathlib

from setuptools import setup


class Version(object):
    name = "relational_algebra"
    description = "RWTH Aachen Computer Science i5/dbis assets for Lecture Datenbanken und Informationssysteme"
    version = "1.0.1"


# The directory containing this file
HERE = pathlib.Path(__file__).parent.resolve()

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="dbis-relational-algebra",
    version=Version.version,
    description=Version.description,
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://git.rwth-aachen.de/i5/teaching/dbis-relational-algebra",
    author="Til Mohr",
    author_email="til.mohr@rwth-aachen.de",
    license="Apache",
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    packages=["relational_algebra"],
    include_package_data=True,
    install_requires=["docstring_inheritance", "typeguard", "pandas"],
)
