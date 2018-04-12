# FROM continuumio/miniconda3:4.4.10
FROM guillaumeflorent/miniconda-pythonocc:3-0.18.3

MAINTAINER Guillaume Florent <florentsailing@gmail.com>

# For wx : libgtk2.0-0 libxxf86vm1
# Funily, installing libgtk2.0-0 seems to solve the XCB plugin not found issue for Qt !!
# For pyqt : libgl1-mesa-dev libx11-xcb1
RUN apt-get update && apt-get install -y libgtk2.0-0 libxxf86vm1 libgl1-mesa-dev libx11-xcb1 && rm -rf /var/lib/apt/lists/*

# Other conda packages
RUN conda install -y numpy matplotlib wxpython pyqt networkx jinja2 pytest
RUN conda install -y -c gflorent corelib aocxchange aocutils ccad party

## ccad
#WORKDIR /opt
## ADD https://api.github.com/repos/osv-team/ccad/git/refs/heads/master version.json
#RUN git clone --depth=1 https://github.com/osv-team/ccad
#WORKDIR /opt/ccad
#RUN python setup.py install
## RUN cp -r /opt/ccad/ccad /opt/conda/lib/python3.6/site-packages

## party
#WORKDIR /opt
## ADD https://api.github.com/repos/osv-team/party/git/refs/heads/master version.json
#RUN git clone --depth=1 https://github.com/osv-team/party
#WORKDIR /opt/party
#RUN python setup.py install

# osvcad
WORKDIR /opt
# ADD https://api.github.com/repos/osv-team/osvcad/git/refs/heads/master version.json
RUN git clone --depth=1 https://github.com/osv-team/osvcad
WORKDIR /opt/osvcad
RUN python setup.py install
