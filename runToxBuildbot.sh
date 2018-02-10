#!/bin/bash
tox -e freeze 

# the buildbot only tests the successful conf (wiht sympy fixed). As soon as the new sympy works with Comportmental systems
# we activate the followwing line again
# tox -e bleadingEdge 

