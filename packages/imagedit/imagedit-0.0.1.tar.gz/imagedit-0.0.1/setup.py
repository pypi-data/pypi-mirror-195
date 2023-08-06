from setuptools import setup, find_packages

with open('readme.md', 'r') as rd:
    page_description = rd.read()

with open('requirements.txt') as re:
    requirements = re.read().splitlines()


setup(
    name="imagedit",
    version="0.0.1",
    author="Alexandre Silva",
    author_email="henrique.map@outlook.com",
    description="This project belongs to Alexandre Silva. This package is a demo for uploading simulation on the Test Pypi website. Email: alexandresilva18a@gmail.com",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Alexandre-S-bits/imagedit",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)