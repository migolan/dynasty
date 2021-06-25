from setuptools import setup

setup(
    name="dynasty",
    packages=['dynasty'],
    install_requires=open('requirements.txt').read(),
    description="A Python class hierarchy analyzer",
    long_description=open('README.md').read(),
    author="Michal Golan",
    author_email="migolan@gmail.com",
    url="https://github.com/migolan/dynasty"
)
