#!/usr/bin/env bash

SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"

cp -r $SCRIPTPATH/bin/* /usr/sbin/
