#from distutils.core import setup
from setuptools import setup

setup(
    name='SimpleHist',
    version='0.1dev',
    description="Simple histograms, designed for data manipulation",
    author='Nicholas Devenish',
    author_email='n.e.devenish@sussex.ac.uk',
    packages=['simplehist', 'simplehist.test'],
    license=open('LICENSE.txt').read(),
    long_description=open('README.txt').read(),
    url='https://github.com/ndevenish/simplehistogram',
    keywords = ['histogram'],
    classifiers = [
      "Programming Language :: Python",
      "Programming Language :: Python :: 2.6",
      "License :: OSI Approved :: MIT License",
      "Operating System :: OS Independent",
      "Intended Audience :: Developers",
      "Intended Audience :: Science/Research",
      "Topic :: Scientific/Engineering :: Mathematics",
      "Topic :: Scientific/Engineering :: Physics",
      "Development Status :: 2 - Pre-Alpha",
      "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=['numpy'],
    test_suite='simplehist.test',
    zip_safe=False,
)