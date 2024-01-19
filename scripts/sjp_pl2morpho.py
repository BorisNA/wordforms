# Convert dumps from sjp.pl
import re
import icu


FILEIN = "odm.txt"
FILEOUT = "forms-PL_new.txt"

forms = {}

with open(FILEIN,mode='r',encoding="utf8") as fin:

	for line in fin:
		words = re.split(r',\x20*', line)
		words = [w.strip() for w in words]
		words = [w for w in words if w != ""]

		if len( words ) <= 1:
			continue

		base, *flex = words
		flex = [f for f in flex if f != base]
		if len(flex) == 0:
			continue

		if not forms.get( base ):
			forms[base] = set()

		forms[base].update( flex )


collator = icu.Collator.createInstance(icu.Locale('pl_PL.UTF-8'))
bases = sorted( forms, key=collator.getSortKey )
# TODO case-insensitive?

with open( FILEOUT, mode='w', encoding='utf8') as fout:
	for base in bases:
		print( base + ": ", end = "", file=fout )
		print( ", ".join( list( forms[ base ] ) ), file=fout )