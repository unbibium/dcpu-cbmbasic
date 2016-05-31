#!/usr/bin/python
#
# Dependency checker for dasm16 files

import sys
import re
from collections import defaultdict

if len(sys.argv) < 2:
    print("Lists symbol-based dependencies of each file")
    print("Usage: %s <filenames>" % sys.argv[0])
    sys.exit(1)

files = []

if len(sys.argv) == 2:
	print("need more than one file to cross-ref")
	sys.exit(1)
	# future versions might branch into includes
	# so that we can test different build variants
    #files = parseIncludes(sys.argv[1])

if len(sys.argv) > 2:
    files = sys.argv[1:]

if not files:
    print("no files!")
    sys.exit(1)

# collect all labels
labelDict = defaultdict(set)
labelRe = re.compile(r'^:([A-Za-z0-9]{4,})')

for filename in files:
	for line in open(filename).readlines():
		m = labelRe.match(line)
		if m:
			labelDict[filename].add(m.group(1))

# collect all references to labels from other files
refDict = defaultdict(set) 
symbolRe = re.compile(r'(?<=[\[\s\.])([A-Za-z][A-Za-z0-9]{3,})')

xrefDict = defaultdict(set)

for filename in files:
	print(filename)
	externalSymbols = set()
	foundSymbols = set()
	for otherFilename in files:
		if otherFilename == filename: continue
		externalSymbols |= labelDict[otherFilename]
	for line in open(filename).readlines():
		if line[0] == ';': continue
		line = line.split(";")[0]
		ms = set(symbolRe.findall(line))
		foundSymbols |= ms & externalSymbols
	refDict[filename] = foundSymbols

for filename in files:
	refSet = refDict[filename]
	print(filename)
	for otherFilename in files:
		if otherFilename == filename: continue
		refsForThisFile = refSet & labelDict[otherFilename]
		if refsForThisFile:
			print("    %s: %s" % (otherFilename, ", ".join(refsForThisFile)))
