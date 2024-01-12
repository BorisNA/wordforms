import sys
import logging
from pathlib import Path
from typing import TextIO, Dict, Set

FILE_LOGGING_LEVEL = logging.DEBUG
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


def read_wordforms_as_list( infile: TextIO ) -> Dict[ str, Set ]|None:
    is_error = False
    infl_dict = {}
    for line in infile:
        line = line.rstrip()
        spl = line.split(":")
        if len(spl) != 2:
            err = f'Wordform error at: "{line}"'
            if 'logging' in sys.modules:
                logging.error( err )
            else:
                print( err, file=sys.stderr )
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

    if is_error:
        infl_dict = None

    return infl_dict


# Still essential (for Windows?)
sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')

inflDict = read_wordforms_as_list( sys.stdin )

if inflDict:
    for stem in inflDict:
        forms = ", ".join(sorted(list(inflDict[stem])))
        assert forms != ""
        print( f'{stem}: {forms}' )
else:
    print( "Empty list is generated or there are errors - see the log-file", file = sys.stdout )