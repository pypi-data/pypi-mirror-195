from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="haso_api_client",
    version="1.0.0",
    author="Haseeb Ali",
    author_email="haseb.chaudhry@gmail.com",
    description="A simple API client package.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Haseb-ali/api_client",
    packages=find_packages(),
    install_requires=[
        "requests",
        "pyyaml",
        "jwt",
        "requests_oauthlib"
        # Add any other required packages here
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
