from setuptools import find_packages, setup

from tasks import __version__ as version

INSTALL_REQUIRES = [
]

DEV_TEST = [
    "pytest>=3.9.0",
]

setup(
    name='tasks',
    version=version,
    packages=find_packages(exclude=["*test*"]),
    install_requires=INSTALL_REQUIRES,
    extras_require={
        "dev-test": (DEV_TEST,),
    },
)
