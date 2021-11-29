import os

import pkg_resources
from setuptools import find_packages, setup

about = {}
here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "empresas_brasil", "__version__.py")) as f:
    exec(f.read(), about)

with open(os.path.join(here, "requirements.txt")) as f:
    install_requires = [str(req) for req in pkg_resources.parse_requirements(f)]

with open("README.md", "r") as f:
    readme = f.read()


setup(
    packages=find_packages(exclude=("docs", "tests")),
    name=about["__title__"],
    description=about["__description__"],
    version=about["__version__"],
    author=about["__author__"],
    author_email=["__author_email__"],
    long_description=readme,
    long_description_content_type="text/markdown",
    url=about["__url__"],
    license=about["__license__"],
    python_requires=">=3.8",
    install_requires=install_requires,
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    entry_points={
        'console_scripts': [
            '{name}={name}.client:run'.format(name=about["__title__"])
        ],
    },
)
