#!/usr/bin/env bash

SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"
echo export PATH="$SCRIPTPATH/bin:\$PATH" >> ~/.profile
