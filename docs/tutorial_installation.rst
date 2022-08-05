Installation
============

.. contents:: :local:

Stable (with Anaconda)
----------------------

This is our recommend installation method!
Follow the steps below to start using Spotlight!

#. You will need the Anaconda environment software. To download Anaconda follow the instructions here: https://docs.anaconda.com/anaconda/install/

#. :download:`Download the environment_rietveld.yaml file from our repository.<https://raw.githubusercontent.com/lanl/spotlight/master/tools/environment_rietveld.yaml>`

#. Create a new conda environment using the following file.

    .. literalinclude:: ../tools/install_rietveld.sh
       :language: bash

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

