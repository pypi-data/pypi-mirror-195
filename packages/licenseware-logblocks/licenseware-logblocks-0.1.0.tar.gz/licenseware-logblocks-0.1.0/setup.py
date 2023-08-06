from setuptools import find_packages, setup

# python3 setup.py bdist_wheel sdist

setup(
    name="licenseware-logblocks",
    version="0.1.0",
    url="https://github.com/licenseware/licenseware-logblocks",
    author="Licenseware",
    author_email="contact@licenseware.com",
    description="Post formatted log messages to slack, mentioning users when error ocurrs",
    entry_points={"console_scripts": ["logblocks = logblocks.logblocks:main"]},
    packages=find_packages(include=["logblocks", "logblocks.*"]),
)
