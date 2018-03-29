Install osvcad
************

The simplest way to install **osvcad** is by creating a Docker image that sets up the required environment.

Note that the *./install_osvcad.sh* script maps the $HOME directory of the host machine to the $HOME folder of the Docker container. This means that the $HOME folder of the
host machine and the $HOME of the osvcad Docker container share the same files and folders.

Installation steps
------------------

- Install `Docker <https://docs.docker.com/install/>`_ for your platform

- *git clone https://github.com/osv-team/osvcad* somewhere under $HOME

- *cd osvcad*

- *./install_osvcad.sh*

- *./start_osvcad.sh*

Now you can execute examples from osvcad or write your own examples.


Development environment
-----------------------

After launching the osvcad Docker container (*./start_osvcad.sh* command) you can type the following command at the container prompt:

*export PYTHONPATH="${PYTHONPATH}:/home/<user>/path/to/osvcad/"*

This will allow you to have changes to the osvcad package code taken into account for tests and examples.