#!/bin/bash
#
# run from current directory
#
# todo: make file list dynamic

./tokenize.py ../demos/startrek.lst startrek.dprg
./tokenize.py ../demos/eliza.lst eliza.dprg
./tokenize.py ../demos/tenprint.lst tenprint.dprg
./tokenize.py ../demos/dirlist.lst dirlist.dprg

echo '; DEMO PROGRAMS' | cat - directory.dasm16 *.dprg >|../demo.dasm16

rm *.dprg
