.. ananke documentation master file, created by
  sphinx-quickstart on Fri Jul 19 15:03:41 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Ananke: A module for causal inference
*************************************

How to install
==============
Install `graphviz <https://www.graphviz.org/download/>`_ using the appropriate method for your OS
    
.. code:: shell

    # Ubuntu

    sudo apt install graphviz libgraphviz-dev pkg-config

    # Mac

    brew install graphviz

    # Mac (M1)
    ## see https://github.com/pygraphviz/pygraphviz/issues/398
    
    brew install graphviz
    python -m pip install \
        --global-option=build_ext \
        --global-option="-I$(brew --prefix graphviz)/include/" \
        --global-option="-L$(brew --prefix graphviz)/lib/" \
        pygraphviz

    # Fedora

    sudo yum install graphviz

Install the latest `release <https://pypi.org/project/ananke-causal/>`__ using pip.

.. code:: shell

    pip3 install ananke-causal

For more details please see the `gitlab <https://gitlab.com/causal/ananke>`_, or the `documentation <https://ananke.readthedocs.io>`_ for details on how to use Ananke.


Documentation
*************

.. toctree::
   :maxdepth: 2
   :caption: Contents:
   
   notebooks/quickstart.ipynb
   notebooks/causal_graphs.ipynb
   notebooks/estimation.ipynb
   notebooks/identification_surrogates.ipynb
   notebooks/linear_gaussian_sems.ipynb
   notebooks/maximum_likelihood_discrete_data_admgs.ipynb


Citation
========
If you enjoyed this package, we would appreciate the following citations:

.. bibliography:: references.bib
   :all: 

   
Contributors
============
* Rohit Bhattacharya
* Jaron Lee
* Razieh Nabi
* Preethi Prakash
* Ranjani Srinivasan


Ananke Graphs
=============
:doc:`ananke.graphs`

Ananke Identification
=====================
:doc:`ananke.identification`

Ananke Estimation
=====================
:doc:`ananke.estimation`

Ananke Models
=====================
:doc:`ananke.models`

Indices and Tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
