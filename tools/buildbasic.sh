#!/bin/bash
../qplop.py startrek.lst startrek.dprg
../qplop.py eliza.lst eliza.dprg
../qplop.py tenprint.lst tenprint.dprg
../qplop.py dirlist.lst dirlist.dprg

echo '; DEMO PROGRAMS' | cat - directory.dasm16 *.dprg >|demo.dasm16
