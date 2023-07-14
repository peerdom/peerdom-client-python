from setuptools import setup, find_packages

setup(
    name="peerdomclient",
    version="0.1.0",
    author="Peerdom",
    author_email="info@peerdom.org",  # change to peerdom email
    maintainer="Robin Szymczak",
    maintainer_email="robin@peerdom.org",
    description="Peerdom's Python api wrapper developed by Peerdom",
    long_description=open('README.md').read(),
    url="https://companyname.com/products/company-package",  # change to github page
    #    packages=find_packages(where='peerdomclient'),
    #    package_dir={'': 'peerdomclient'},
    install_requires=[
        "Requests==2.31.0",
        "setuptools==66.1.1"
    ],
)
