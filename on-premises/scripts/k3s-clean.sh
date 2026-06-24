#!/usr/bin/env zsh

sudo k3s crictl rmi --prune

sudo k3s crictl  images ls
