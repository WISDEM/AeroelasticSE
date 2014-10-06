Installation
------------

.. admonition:: Prerequisites
   :class: warning

   NumPy, SciPy, the FAST executable.  For some wrappers, the fusedwind framework.

Clone the repository at `<https://github.com/WISDEM/AeroelasticSE>`_ or download the releases and uncompress/unpack.

Install the AeroelasticSE plugin with the following command.

.. code-block:: bash

   $ python setup.py install

To check if installation was successful try to import the module

.. code-block:: bash

    $ python -c "import AeroelasticSE"

Then run the unit tests for the various FAST wrappers.
NOTE: these will require the user to correctly set the location of FAST and its input files.
Currently this is done by editing the source files themselves.  (The tests are in the
source modules).  

.. code-block:: bash

  $ python runFAST.py --help
  $ python runFAST.py
  $ python runFAST.py -t
  $ python FAST_component.py
  $ python FusedFAST.py 
  $ python iecApp.py -i some_cases.txt -f runbatch-control.txt
  
Please see :ref:`aeroelasticse`.
