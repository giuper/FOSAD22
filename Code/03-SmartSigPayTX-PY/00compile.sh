#!/usr/bin/bash

##change this to the folder that contains goal
DIRECTORY=~/node
GOAL=${DIRECTORY}/goal

FILE=fourtytwo.teal

##uncomment next line if you want to use passphrase.teal
##FILE=passphrase.teal

${GOAL} clerk compile ${FILE}




