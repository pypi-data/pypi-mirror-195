from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="ra_engine",
    version="0.0.1-rev5",
    license="MIT",
    author="Navindu Dananaga",
    author_email="navindudananga123@gmail.com",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SLTDigitalLab/RAE-sdk-python.git",
    keywords="ra_engine",
    install_requires=["requests", "pandas"],
)
