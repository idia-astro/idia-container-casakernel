# CasaPy-Kernel

A [Jupyter](http://jupyter.org/) kernel for [CASA](https://casa.nrao.edu/) using a Singularity container.  Based on the kernel [jupyter-casa](https://github.com/aardk/jupyter-casa).

## Updates
Changes and bug fixes:

_January 15, 2017_:
1. update to CASA from `4.7.0` to `5.1.0`
1. refactor casacode for compatibility with `python 2.7` (from `2.6`) and `ipython 6.1.0` (`0.1.0`)
1. includes `WSclean 2.5` (command line only, no notebook support)
1. introduce `casatasks` module (i.e. one can include `import casatasks` rather than starting a CASA session)
1. enable casa interactive shell from the command line 
1. enable command line script use-case (i.e. `casa -c script.py`)
1. enable python syntax highlighting

## Background

The use of iPython and Jupyter notebooks has proven to be extremely useful in data-intensive scientific research, since it allows scientists and analysts to easily create and share code and results in an intuitive, complete, and open manner.  In the field of radio astronomy, the software package CASA contains a vast array of code, and is indispensable for many projects.  However, CASA has a complexity code base with a large number of dependencies.  This creates challenges when deployed in a variety of different user environments and when used for many different purposes.  

This project attempts to bridge the gap between Jupyter and CASA by implementing a CASA kernel for Jupyter notebooks.  To make CASA compatible with Jupyter, we make a custom build of CASA, which is built in a singularity container.  The singularity container can then be used directly as a Jupyter kernel.  In this way, CASA can be run by any user, regardless of their computing environment, so long as they have a web browser capable of loading a Jupyter notebook.  

## Technical Overview 

This project is based on a prototype developed at [JIVE](http://www.jive.nl/) using a [DOCKER](https://www.docker.com/) container.  We use a [SINGULARITY](singularity.lbl.gov/) container rather than DOCKER, since the intended use is in a scientific HPC environment.  Other than that, the project is essential the same. 

### Custom CASA Build
In the image, CASA is built with a newer version of python than is available in the binary distribution.  CasaPy is refactored to work with Jupyter rather than ipython, and each CASA task is wrapped.  In cases where a task is interactive (i.e. it spawns a QT or interactive window), we attempt to parametrize the graphical input, and capture the relevant output as an image.  Eventually, we would want to either embed interactive tasks within a notebook cell, or allow for an X11 window to interact with the notebook.  

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

You will need to install Singularity to build the container:

* [Singularity](singularity.lbl.gov/)


### Building the Container

The following is a step by step example for creating the container from scratch.   We first create a singularity container and then build all software inside that container. If you already have access to a built container then you can skip to the next section.

First create a container, it will need about 8GB of storage: 

`singularity create --size 8192 jupyter-casa.img`

All the procedures for buildng the software, configuring the environment, and defining the behaviour of the container are defined in the `.def` file.  Since this is a lot of stuff, it will take several hours to complete:

`singularity bootstrap jupyter-casa.img jupyter-casa-5.1.1-cli.def`

If you see any errors, you can rerun the bootstrap step incrementally in order to isolate the point of failure.

### Using the Container

Now that we have build our container, we can set it up as a [jupyter kernel](http://jupyter-client.readthedocs.io/en/latest/kernels.html) by adding a kernel.json file to your existing jupyter or jupyterhub system.  You can also use the container in several different other ways.  To summarize, the container can be used:

1. **As a Jupyter kernel for CASA**

    Copy the `kernel.json` file to your home directory:
    `mkdir -p $HOME/.local/share/jupyter/kernels/jupyter-casa-kernel/`
    `cp idia-container-casakernel/jupyter/kernels/casapy/kernel.json ~/.local/share/jupyter/kernels/jupyter-casa-kernel/`
    Then start a jupyter notebook session and choose the new kernel, 'jupyter-casa-kernel'.

2. **Using the embedded CASA terminal** -- 

    Run CASA using the conventional interactive CASA session.  First invoke a singularity shell session, then start the casa interactive terminal in the normal way:
    `sudo singularity shell --writable jupyter-casa.img`
    `casa --nogui`

3. **To execute a non-interactive script** 

    Run a non-interactive script (i.e. `casa -c myscript.py`) - e.g., to execute cluster / HPC jobs
    `sudo singularity exec --writable jupyter-casa.img casa -c myscript.py`



### Tests



## Acknowledgments

This version created by @sonasi ([Joseph Bochenek](joe.bochenek@uct.ac.za)) and [IDIA](http://idia.ac.za/).  It's based on a proof of concept Jupyter-CASA kernel created by @aardk ([Aard Keimpema](https://github.com/aardk)) and [JIVE](http://www.jive.nl/).


[1] [Jupyter](http://jupyter.org/install)

[2] [CASA](https://casa.nrao.edu/casa_obtaining.shtml)

[3] [WSClean](https://sourceforge.net/projects/wsclean/)
