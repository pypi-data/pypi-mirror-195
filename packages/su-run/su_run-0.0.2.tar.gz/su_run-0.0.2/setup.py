from setuptools import setup, find_packages

VERSION = '0.0.2'

setup(
    name='su_run',
    version=VERSION,
    description='Run a subprocess as different user',
    author='Clayton Voges',
    author_email='vogesclayton@gmail.com',
    packages=find_packages(),
    install_requires=[]
)
