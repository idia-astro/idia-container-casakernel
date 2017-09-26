# CasaPy-Kernel

A [Jupyter](http://jupyter.org/) kernel for [CASA](https://casa.nrao.edu/) based on [jupyter-casa](https://github.com/aardk/jupyter-casa)

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

What things you need to install the software and how to install them:

* [SINGULARITY](singularity.lbl.gov/)

### Creating the Container

A step by step series of examples that tell you have to get a development env running

Create a singularity container and bootstrap it: 

singularity create --size 8192 jupyter-casa.img
singularity bootstrap jupyter-casa.img jupyter-casa-build.def

You can execute a command in the shell or open an interactive session:

```
sudo singularity exec --writable jupyter-casa.img chmod 755 /singularity
sudo singularity run jupyter-casa.img
sudo singularity shell --writable jupyter-casa.img
```


Now that we have build our container, we can set it up as a [jupyter kernel](http://jupyter-client.readthedocs.io/en/latest/kernels.html) by adding a kernel.json file to your existing jupyter or jupyterhub system.

```
mkdir /usr/share/local/jupyter/kernels/jupyter-casa-kernel
cp kernel.json /usr/share/local/jupyter/kernels/jupyter-casa-kernel
```

or 

```
cp kernel.json $HOME/.local/jupyter/kernels/jupyter-casa-kernel/
```



### Tests



### Deployment


## Acknowledgments

This project is based on a proof of concept by [Aard Keimpema](https://github.com/aardk) at [JIVE](http://www.jive.nl/)
