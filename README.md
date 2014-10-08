AeroelasticSE is a wrapper for the FAST aeroelastic code that allows it to be used in OpenMDAO.

Author: [P. Graf and K. Dykes](mailto:nrel.wisdem+aeroelasticse@gmail.com) 

## Version

This software is a beta version 0.1.0.

## Detailed Documentation

For detailed documentation see <http://wisdem.github.io/AeroelasticSE/>

## Prerequisites

General: NumPy, SciPy, Swig, pyWin32, MatlPlotLib, Lxml, OpenMDAO

## Dependencies

Wind Plant Framework: [FUSED-Wind](http://fusedwind.org) (Framework for Unified Systems Engineering and Design of Wind Plants)

Sub-Models: CommonSE

Supporting python packages: Pandas, Algopy, Zope.interface, Sphinx, Xlrd, PyOpt, py2exe, Pyzmq, Sphinxcontrib-bibtex, Sphinxcontrib-zopeext, Numpydoc, Ipython

## Installation

First, clone the [repository](https://github.com/WISDEM/AeroelasticSE)
or download the releases and uncompress/unpack (AeroelasticSE.py-|release|.tar.gz or AeroelasticSE.py-|release|.zip) from the website link at the bottom the [AeroelasticSE site](http://nwtc.nrel.gov/AeroelasticSE).

Install AeroelasticSE within an activated OpenMDAO environment

	$ plugin install

It is not recommended to install the software outside of OpenMDAO.

For software issues please use <https://github.com/WISDEM/AeroelasticSE/issues>.  For functionality and theory related questions and comments please use the NWTC forum for [Systems Engineering Software Questions](https://wind.nrel.gov/forum/wind/viewtopic.php?f=34&t=1002).