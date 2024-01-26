from graph import *

class Kekule_Structure():
  """ this class allows for representing a Kekulé structure of a molecule """
  
  def __init__ (self, g: Graph, labelling: list) -> None:
    """ creates a Kekulé from a graph and a valid edge labelling """
    super().__init__()
    self.__g = g.copy()
    
    for edge,label in labelling:
      self.__g.set_edge_label (edge[0],edge[1],label)

  
  def save (self, filename):
    """ saves the Kekule structure in a dot file """
     # we open the file
    myfile = open (filename,"w")

    # we write the header
    myfile.write("strict graph {")
    
    # we write the edges
    for edge in self.__g.get_edges():
      if self.__g.get_edge_label(edge[0],edge[1]) == 1:
        options = '[color=blue, style="bold"]'
      else:
        options = ""
      
      myfile.write("\t" + str(edge[0]) + " -- " + str(edge[1]) + " " + options + "\n")  
    
    # we write the footer
    myfile.write("}")

    # we close the file
    myfile.close ()
