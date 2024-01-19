import sys
import logging
from pathlib import Path
from typing import TextIO, Dict, Set
import re
import glob

FILE_LOGGING_LEVEL = logging.INFO
CONSOLE_LOGGING_LEVEL = logging.ERROR

logFormatter = logging.Formatter("[%(levelname)-5.5s]  %(message)s")
rootLogger = logging.getLogger()

logFileName = Path(__file__).stem + ".log"

fileHandler = logging.FileHandler(logFileName, encoding="utf8", mode="w")
fileHandler.setFormatter(logFormatter)
fileHandler.setLevel(FILE_LOGGING_LEVEL)
rootLogger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
consoleHandler.setLevel(CONSOLE_LOGGING_LEVEL)
rootLogger.addHandler(consoleHandler)

rootLogger.setLevel(logging.DEBUG)

# Main code


def check_wordforms( infile: TextIO ) -> (bool, bool):
    is_error = False
    infl_dict = {}
    for line in infile:
        line = line.rstrip()
        spl = line.split(":")
        if len(spl) != 2:
            logging.error( f'"{infile.name}": Too many ":" at "{line}"' )
            is_error = True
            continue

        stem, flex = spl
        stem = stem.strip()
        flex_line = flex.split(",")
        flex_line = (f.strip() for f in flex_line)
        flex_line = [f for f in flex_line if f != stem and f != '']
        if len(flex_line) > 0:
            # do not add empty sets
            if not infl_dict.get(stem):
                infl_dict[stem] = set()
            infl_dict[stem].update(flex_line)

    w_empty = False
    w_badword = False

    for s in infl_dict:
        if len(infl_dict[s]) == 0 or ( len(infl_dict[s]) == 1 and infl_dict[s]=="" ):
            w_empty = True
            logging.info( f'Empty infections for "{s}"')

        for w in infl_dict[s]:
            if re.match( r'[^\w\x20]', w ):
                w_badword = True
                logging.info( f'Bad inflection: "{s}" -> "{w}"')

    if w_empty:
        logging.warning(f'"{infile.name}": Empty inflection lines')
    if w_badword:
        logging.warning(f'"{infile.name}": Bad inflections')

    return is_error, w_empty | w_badword


if len( sys.argv ) <= 1:
    print( "Parameters: filename(s)" )
    exit(-1)

for p in sys.argv[1:]:
    for fn in glob.iglob(p):
        with open( fn, mode='r', encoding="utf8") as fin:
            print( f'Checking {fn}:...', end='')
            sys.stdout.flush()
            err, warn = check_wordforms( fin )
            if warn:
                print(f'WARN ', end='')
            if err:
                print(f'ERR ', end='')
            if not (err or warn):
                print(f'OK', end='')
            print()

