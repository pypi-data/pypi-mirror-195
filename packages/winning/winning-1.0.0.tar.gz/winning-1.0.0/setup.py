import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="winning",
    version="1.0.0",
    description="Fast ability inference from contest winning probabilities",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/microprediction/winning",
    author="microprediction",
    author_email="peter.cotton@microprediction.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.9",
    ],
    packages=["winning"],
    test_suite='pytest',
    tests_require=['pytest','pandas','scipy>=1.7.3'],
    include_package_data=True,
    install_requires=["numpy","pytest","pathlib","wheel"],
    entry_points={
        "console_scripts": [
            "winning=winning.__main__:main",
        ]
    },
)
