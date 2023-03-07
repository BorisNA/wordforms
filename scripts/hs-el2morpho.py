# Convert andreyefgs's files


import fileinput
import sys
import re




sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')

debug = False

forms = {}

for line in fileinput.input():
	if line.startswith("#"):
		continue

	number, flex, base = line.split("_")

	flex = flex.strip()
	base = base.strip()

	if flex == base or flex == "-":
		continue

#	if re.match( r'^\d', flex ):
#		continue
#	if ( base[0].isupper() ^ flex[0].isupper() ): # and tags.startswith( "VER" ):
#		continue

#	if  base[0].isupper() ^ flex[0].isupper():
#		print( base + ": " + flex, file = sys.stderr )
#		continue # ???

	if base not in forms:
		forms[ base ] = set()
	forms[ base ].add( flex )

bases = sorted( forms ) # , key=din5007

for base in bases:
	print( base + ": ", end = "" )
	print( ",".join( list( forms[ base ] ) ) )