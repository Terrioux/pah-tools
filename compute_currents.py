#!/usr/bin/env python3

import sys
from dot_reader import *
from kekule import *
from face_graph import *
from itertools import *

def save (g, filename):
  """ saves the current graph in a dot file """
   # we open the file
  myfile = open (filename,"w")

  # we write the header
  myfile.write("digraph {\n")
  
  # we write the edges
  for edge in g.get_edges():
    val = g.get_edge_label(edge[0],edge[1]) - g.get_edge_label(edge[1],edge[0])
    options = "[label="+str(abs(val))+"]"
    if val == 0:
      myfile.write("\t" + str(edge[0]) + " -> " + str(edge[1]) + " " + options + "\n")  
    elif val > 0:
      myfile.write("\t" + str(edge[0]) + " -> " + str(edge[1]) + " " + options + "\n")  
    else:
      myfile.write("\t" + str(edge[1]) + " -> " + str(edge[0]) + " " + options + "\n")  
    
  # we write the footer
  myfile.write("}")

  # we close the file
  myfile.close ()


# we check the number of parameters in the command line
if len(sys.argv) != 2:
  print ("Usage:",sys.argv[0], "molecule.dot")
else:
  # we read the molecule
  d = Dot_Reader(sys.argv[1])
  g = d.read()

  # we compute the face graph
  fg = Face_Graph(g )

  # we set the label of each edge to 0
  for (x,y) in g.get_edges():
    g.set_edge_label(x,y,0)
    g.set_edge_label(y,x,0)
  
  # we compute the Kekulé structures
  k = Kekule(g)
    
  # we enumerate the Kekulé structures
  for s in k.get_kekule_structures():
    circuits = s.find_conjugated_circuits()
    cc_list = []
    for a in sorted(circuits.keys()):
      for cc in circuits[a]:
        a = fg.give_orientation(cc)
        a.append(a[0])
        cc_list.append(a)
        
        # we consider the conjugated circuit one per one
        for i in range(len(a)-1):
          g.set_edge_label(a[i],a[i+1],g.get_edge_label(a[i],a[i+1])+1)
    
    # we consider the independent combination of conjugated circuits
    nb = 2
    again = True
    while nb <= len(cc_list) and again:        
      for cc in combinations(cc_list,nb):
        i = 0
        independent = True
        while i < len(cc) and independent:
          j = i + 1 
          while j < len(cc) and set(cc[i]) & set(cc[j]) == set():
            j += 1
          independent = j == len(cc)
          i += 1
          
        if i == len(cc):
          # all the circuits i cc are pairwise independent
          # we take into account their contribution to currents
          for c in cc:
            for i in range(len(c)-1):
              g.set_edge_label(c[i],c[i+1],g.get_edge_label(c[i],c[i+1])+1)
          again = True
          
      nb += 1

  # we save the graph with information about currents
  save (g,sys.argv[1]+"_currents.dot")

