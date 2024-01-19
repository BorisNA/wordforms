# Convert dumps from http://www.danielnaber.de/morphologie/ and/or https://morphy.wolfganglezius.de/
# 1. Get stable languagetools build and needed *pos* repositories from languagetools
# 2. Get an "export.sh" script from german_pos
# *. Commandtool is like:
# java -cp $LT_PATH/languagetool.jar org.languagetool.tools.DictionaryExporter -i ${1%.*}.dict -info ${1%.*}.info
#      -o ${1%.*}.dump
import argparse
import fileinput
import logging
import sys
import re
from pathlib import Path

import icu

FILE_LOGGING_LEVEL = logging.DEBUG
CONSOLE_LOGGING_LEVEL = logging.ERROR

logFormatter = logging.Formatter("[%(levelname)-5.5s]  %(message)s")
rootLogger = logging.getLogger()

logFileName = Path(__file__).stem + ".log"

if FILE_LOGGING_LEVEL:
	fileHandler = logging.FileHandler(logFileName, encoding="utf8", mode="w")
	fileHandler.setFormatter(logFormatter)
	fileHandler.setLevel(FILE_LOGGING_LEVEL)
	rootLogger.addHandler(fileHandler)

if CONSOLE_LOGGING_LEVEL:
	consoleHandler = logging.StreamHandler()
	consoleHandler.setFormatter(logFormatter)
	consoleHandler.setLevel(CONSOLE_LOGGING_LEVEL)
	rootLogger.addHandler(consoleHandler)

rootLogger.setLevel(logging.DEBUG)

parser = argparse.ArgumentParser(
	description='Convert lingtools dump to inflections (wordforms) table',
	formatter_class=argparse.RawTextHelpFormatter,
	epilog='''example:
 %(prog)s -i german.dump -o forms_DE.txt --lang de_DE
 '''
)
parser.add_argument('-i', '--input', dest='FNAME_DUMP', metavar='FILENAME', required=True,
					action='store',
					help='input lingtools dump')
parser.add_argument('-o', '--output', dest='FNAME_WORDFORMS', metavar='FILENAME', required=False,
					action='store',
					help='output wordforms file name (will be infile with txt extension if omitted)')
parser.add_argument('--locale', dest='LOCALE', metavar='LOCALE', required=False,
					action='store',
					help='locale to sort entries (example: de_DE), no sorting if omitted')

args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])

if not args.FNAME_WORDFORMS:
	args.FNAME_WORDFORMS = args.FNAME_DUMP + "_wf.txt"

with open(args.FNAME_DUMP, mode='r', encoding='utf8') as fin:
	print(f'Parsing file {args.FNAME_DUMP}')
	forms = {}

	for line in fin:
		if line.startswith("#"):
			continue

		flex, base, tags = line.split("\t")

		if base == "атами":
			pass

		flex = flex.strip()
		base = base.strip()
		tags = tags.strip()

		if flex == base or flex == "-":
			continue
		if re.match(r'^\d', flex):
			logging.debug( f'{base}: digit {flex}')
			continue
		if base[0] == "-" or base[0] == "­":   # Both are dashes
			# some ошмётки
			logging.debug( f'{base}: ignoring dash {flex}')
			continue

		if base.lower() == flex.lower():
			logging.debug( f'{base}: mixed case {flex}')
			continue

		if base not in forms:
			forms[base] = set()

		forms[base].add(flex)

print(f'Normalizing...')
for stem in list(forms.keys()):
	words = forms[stem]
	words = [w.strip() for w in words]
	words = [w for w in words if w != ""]
	if len(words) == 0:
		del forms[stem]
	else:
		forms[stem] = words


if args.LOCALE:
	print(f'Sorting...')
	collator = icu.Collator.createInstance(icu.Locale(f'{args.LOCALE}.UTF-8'))
	stems = sorted(forms.keys(), key=collator.getSortKey)
else:
	stems = list(forms.keys())

with open(args.FNAME_WORDFORMS, mode='w', encoding='utf8') as fout:
	print(f'Generating {args.FNAME_WORDFORMS}')

	for stem in stems:
		print(stem + ": ", end="", file=fout)
		print(", ".join(list(forms[stem])), file=fout)
