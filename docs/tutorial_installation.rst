Installation
============

.. contents:: :local:

Stable (with Anaconda)
----------------------

This is our recommend installation method!
Follow the steps below to start using Spotlight!

#. You will need the Anaconda environment software. To download Anaconda follow the instructions here: https://docs.anaconda.com/anaconda/install/

#. :download:`Download the environment_rietveld.yaml file from our repository.<https://raw.githubusercontent.com/lanl/spotlight/master/tools/environment_rietveld.yaml>`

#. Create a new conda environment using the ``environment_rietveld.yaml`` file.
   There are two important things to note during this step.
   If building GSAS-II and you are behind a firewall (e.g. at LANL), then you will need to compile some fortran modules using ``scons`` as shown below.
   You will also need to set ``MAUD_PATH`` to our MAUD installation in order to do the parts of this tutorial that use MILK and MAUD.

    .. literalinclude:: ../tools/install_rietveld.sh
       :language: bash

   If you do not want to have to set ``PYTHONPATH`` and ``MAUD_PATH`` everytime you load the Anaconda env, you can create and add these commands to ``${CONDA_PREFIX}/etc/conda/activate.d/post.sh`` like is shown above in the commented out snippet.

#. Activate the environment by running the following command.

    .. code-block:: bash

        conda activate spotlight-rietveld

You should have Spotlight installed now!
Following the remainder of this tutorial to become familiar with using Spotlight.

Development (from GitHub)
-------------------------

.. warning::

    This will retrieve the latest version under development. Use at your own risk!

#. The latest development version is available directly from our `GitHub Repo<https://github.com/lanl/spotlight>`_. First, clone the repository like the following.

    .. code-block:: bash
    
        git clone https://github.com/lanl/spotlight
        cd spotlight

#. Next, we recommend that you create a Conda environment since you will still need the dependencies. You can create an empty Anaconda by running the following.

    .. code-block:: bash
    
        conda create --name spotlight-rietveld

#. And then activate the environment with the following.

    .. code-block:: bash
    
        conda activate spotlight-rietveld

#. Now install Spotlight using ``pip`` like the following.

    .. code-block:: bash
    
        pip install .

You should have Spotlight installed now!

