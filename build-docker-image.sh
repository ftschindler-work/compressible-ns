#!/bin/bash

sudo docker build --rm=true --force-rm=true -t ftschindlerwork/compressible-ns -f Dockerfiles/Dockerfile Dockerfiles/
