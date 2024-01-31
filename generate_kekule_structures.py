#!/usr/bin/env python3

import sys
from dot_reader import *
from kekule import *


# we check the number of parameters in the command line
if len(sys.argv) != 2:
  print ("Usage:",sys.argv[0], "molecule.dot")
else:
  # we read the molecule
  d = Dot_Reader(sys.argv[1])
  g = d.read()

  # we compute the Kekulé structures
  k = Kekule(g)

  # we print their number
  print ("# Kekulé structures:",k.get_kekule_structures_number())

  # we save the Kekulé structures
  i = 0
  for s in k.get_kekule_structures():
    output_filename = sys.argv[1]+"_kekule"+str(i)+".dot"
    s.save(output_filename)
    i += 1
