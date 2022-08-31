import pathlib

from setuptools import find_packages, setup

import versioneer

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

# using climate-assessment as a template here
REQUIREMENTS_INSTALL = ["netCDF4", "numpy", "pandas", "scipy", "tqdm", "xarray"]
REQUIREMENTS_NOTEBOOKS = ["notebook", "ipywidgets"]
REQUIREMENTS_TESTS = [
    "codecov",
    "pytest-cov",
    "pytest-console-scripts",
    "pytest>=4.0",
    "matplotlib",
]
REQUIREMENTS_DOCS = ["sphinx>=1.4", "sphinx_rtd_theme"]
REQUIREMENTS_DEPLOY = [
    "twine>=1.11.0",
    "setuptools>=41.0",
    "wheel>=0.31.0",
]  # plus conda

requirements_dev = [
    *["bandit", "black", "flake8", "isort", "pydocstyle"],
    *REQUIREMENTS_NOTEBOOKS,
    *REQUIREMENTS_TESTS,
    *REQUIREMENTS_DOCS,
    *REQUIREMENTS_DEPLOY,
]

requirements_extras = {
    "docs": REQUIREMENTS_DOCS,
    "tests": REQUIREMENTS_TESTS,
    "deploy": REQUIREMENTS_DEPLOY,
    "dev": requirements_dev,
}

setup(
    name="fair",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="Finite-amplitude Impulse Response (FaIR) simple climate model",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/OMS-NetZero/FAIR",
    author="Chris Smith",  # TODO: add in all contributors
    author_email="c.j.smith1@leeds.ac.uk",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords="simple, climate, model, temperature, CO2, forcing, emissions",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.6, <4",
    install_requires=REQUIREMENTS_INSTALL,
    extras_require=requirements_extras,
)
