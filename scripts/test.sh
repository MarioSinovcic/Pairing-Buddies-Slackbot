#!/usr/bin/env bash
source "$(dirname "$0")/dockerbuild.sh"

docker run --rm -it -v $HOME/.aws:/root/.aws $buildtag python3 bot_tests.py