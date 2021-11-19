#!/usr/bin/env bash

set -e

docker build -t local/thingity-test -f Dockerfile .
docker run --rm -it local/thingity-test /bin/bash
