from setuptools import setup # type: ignore

install_requires = [
    "numpy",
]

packages = [
    "pyTOMS",
]

console_scripts = [] # type: ignore

setup(
    name = "pyTOMS",
    version = "0.0.0",
    packages = packages,
    install_requires = install_requires,
    entry_points = {"console_scripts": console_scripts},
)
