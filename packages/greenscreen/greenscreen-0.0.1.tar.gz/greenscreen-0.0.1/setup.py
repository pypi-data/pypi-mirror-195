from gettext import install
from setuptools import setup

setup(
    name='greenscreen',
    version='0.0.1',
    author='avocardio',
    author_email='mkalcher@uos.de',
    description='A package for checking the energy efficiency of large models while training',
    packages=['greenscreen'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.6',
    install_requires=[
        'tensorflow',
        'keras',
        'numpy',
    ],
)