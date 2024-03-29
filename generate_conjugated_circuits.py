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
  
  cycles = g.find_cycles()
  for a in sorted(cycles.keys()):
    for p in cycles[a]:
      print (p)
  # faire un test d'inclusion, si max > 2 suppr


  # we compute the Kekulé structures
  k = Kekule(g)

  # we print their number
  print ("# Kekulé structures:",k.get_kekule_structures_number())

  # we same the Kekulé structures
  i = 0
  for s in k.get_kekule_structures():
    output_filename = sys.argv[1]+"_kekule"+str(i)+".dot"
    s.save(output_filename)
    
    circuits = s.find_conjugated_circuits()
    
    print (f"Conjugated circuits for Kekule structure #{i}:")
    for a in sorted(circuits.keys()):
      for p in circuits[a]:
        print (p)

    print()
    i += 1
