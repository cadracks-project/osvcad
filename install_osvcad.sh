#!/usr/bin/env bash

home="${1:-$HOME}"
username="$USER"
user="$(id -u)"

imageName="guillaume-florent/osvcad:latest"
containerName="osvcad"
displayVar="$DISPLAY"

# docker build --file Dockerfile.py3 --no-cache --tag ${imageName} .
docker build --file Dockerfile.py3 --tag ${imageName} .

docker run  -it -d --name ${containerName} --user=${user}   \
    -e USER=${username}                                     \
    -e QT_X11_NO_MITSHM=1                                   \
    -e DISPLAY=${displayVar}                                \
    -e QT_XKB_CONFIG_ROOT=/usr/share/X11/xkb                \
    --workdir="${home}"                                     \
    --volume="${home}:${home}"                              \
    --volume="/etc/group:/etc/group:ro"                     \
    --volume="/etc/passwd:/etc/passwd:ro"                   \
    --volume="/etc/shadow:/etc/shadow:ro"                   \
    --volume="/etc/sudoers.d:/etc/sudoers.d:ro"             \
     -v=/tmp/.X11-unix:/tmp/.X11-unix ${imageName}          \
     /bin/bash
