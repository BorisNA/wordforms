import fileinput
import sys
import re

def din5007(input):
	""" This function implements sort keys for the german language according to 
	DIN 5007."""
	
	# key1: compare words lowercase and replace umlauts according to DIN 5007
	key1=input.lower()
	key1=key1.replace(u"ä", u"a")
	key1=key1.replace(u"ö", u"o")
	key1=key1.replace(u"ü", u"u")
	key1=key1.replace(u"ß", u"ss")
	
	# key2: sort the lowercase word before the uppercase word and sort
	# the word with umlaut after the word without umlaut
	key2=input.swapcase()
	
	# in case two words are the same according to key1, sort the words
	# according to key2. 
	return (key1, key2)
	
sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')

debug = False

forms = {}

for line in fileinput.input():
	if line.startswith("#"):
		continue

	flex, base, tags = line.split("\t")

	if flex == base or flex == "-":
		continue
	if re.match( r'^\d', flex ):
		continue
	if ( base[0].isupper() ^ flex[0].isupper() ): # and tags.startswith( "VER" ):
		continue

	if  base[0].isupper() ^ flex[0].isupper():
		print( base + ": " + flex, file = sys.stderr )

	if base not in forms:
		forms[ base ] = set()
	forms[ base ].add( flex )

bases = sorted( forms, key=din5007 )

for base in bases:
	print( base + ": ", end = "" )
	print( ",".join( list( forms[ base ] ) ) )