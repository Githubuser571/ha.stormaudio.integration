import os
from setuptools import setup

setup(
    name='stormaudio',
    version='0.1',
    packages=['stormaudio'],
    install_requires=['pyserial>=3.4'],
    url='https://github.com/username/stormaudio',
    author='Your Name',
    author_email='your.email@example.com',
    description='Integration for StormAudio processors',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
