#!/usr/bin/env bash

buildtag="slack-bot-builder"

docker build  -t $buildtag $(dirname $0)/..