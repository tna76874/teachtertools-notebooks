#!/bin/bash
set -e

WORKDIR="/home/jovyan/work"

mkdir -p "$WORKDIR"
cd "$WORKDIR"
wget -O - https://github.com/tna76874/teachtertools-notebooks/archive/master.tar.gz | tar xz --strip=2 "teachtertools-notebooks-master/notebooks"

chown -R 1000 "$WORKDIR"

exec "$@"