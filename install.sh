#!/usr/bin/env bash

SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"
# echo export PATH="$SCRIPTPATH/bin:\$PATH" >> ~/.profile

pwd=$(pwd)
cd /usr/sbin
for script in $(ls $SCRIPTPATH/bin | grep -v utils)
do
  ln -s $SCRIPTPATH/bin/$script $script
done
cd $pwd
