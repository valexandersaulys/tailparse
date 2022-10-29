#!/bin/bash

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
    exit exit 1;
fi
   
# check for coverage -- warn user if we don't have it installed
python -m coverage --version
if [ $? != 0 ]
then
    coverage run -m unittest
    coverage report --omit=*tests*
else
    python -m unittest
fi

