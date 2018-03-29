#!/usr/bin/env bash

xhost +local:osvcad
docker start osvcad
docker exec -it osvcad /bin/bash