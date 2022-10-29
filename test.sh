#!/bin/bash

html_flag="false";

# test for commandline args
while getopts 'h' flag; do
  case "${flag}" in
    h) html_flag='true' ;;
  esac
done

# check that we have mypy installed for testing
python -m mypy --version
if [ $? != 0 ]
then
    echo "You don't have mypy installed for type checking in testing";
    exit 1;
fi

# run mypy
mypy tailparse
if [ $? != 0 ]
then
    echo "Did not pass type checking";
    exit 1;
fi
   
# check for coverage -- warn user if we don't have it installed
python -m coverage --version
if [ $? != 0 ]
then
    python -m unittest
else
    coverage run -m unittest
    if [ $? != 0 ]
    then
        exit $?
    else
        if [[ $html_flag -eq "true" ]]
        then
            coverage html --omit=*tests*
        else
            coverage report --omit=*tests*
        fi
    fi    
fi

