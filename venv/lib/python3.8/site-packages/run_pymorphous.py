"""Run a pymorphous program

"""

import ast
import sys
import os
from os.path import splitext

PROFILE = len(sys.argv) > 2

def run():
    if len(sys.argv) < 2:
        print "run_pymorphous: no input file specified!"
        sys.exit(1)
    
    infile = sys.argv[1]
    if not os.path.exists(infile):
        print "File to compile not found: %s" % infile
        sys.exit(1)
    
    ifile = open(infile, 'r')
    source = ifile.read()
    
    #a = ast.parse(source)
    
    #code = compile(a, "<string>", "exec")
    #exec(code, globals(), globals())
    exec(source, globals(), globals())

if PROFILE:
    import cProfile
    command = "run()"
    cProfile.runctx( command, globals(), globals(), filename="PyMorphous.profile" )
else:
    run()
