from setuptools import setup
import os

this_dir = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_dir, 'requirements.txt'), 'r') as fp:
    install_reqs = [r.rstrip() for r in fp.readlines()]

setup(
    name="dynasty",
    packages=['dynasty'],
    install_requires=install_reqs,
    description="A Python class hierarchy analyzer",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Michal Golan",
    author_email="migolan@gmail.com",
    url="https://github.com/migolan/dynasty"
)
