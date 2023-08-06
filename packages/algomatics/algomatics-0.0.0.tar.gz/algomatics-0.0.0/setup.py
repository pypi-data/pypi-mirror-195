import io
from setuptools import setup, find_packages

def long_description():
    with io.open('README.md', 'r', encoding='utf-8') as f:
        readme = f.read()
    return readme

setup(
    name="algomatics",
    version="0.0.0",
    description="This is one place tool for automating task",
    author="vikash tripathi",
    py_modules="algomatics",
    packages=find_packages(exclude=('tests', 'tests.*')),
    long_description=long_description(),
    install_requires = []
)