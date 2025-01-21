from setuptools import setup, find_packages

setup(
    name="daraza-sdk",
    version="0.1.0",
    author="AJr.Allan, Daraza",
    author_email="info@daraza.net",
    description="A Python SDK for interacting with the Daraza API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/arcticline-platform/daraza-sdk.git",
    packages=find_packages(),
    install_requires=["requests"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
