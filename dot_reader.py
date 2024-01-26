from graph import *

class Dot_Reader:
  """ this class allows for reading graphs from dot files """
  
  def __init__ (self, filename) -> None:
    """ initializes the reader """
    self.__filename = filename
    
  def read (self) -> Graph:
    # we create an empty graph
    g = Graph()
  
    # we open the file
    myfile = open (self.__filename,"r")

    # we skip the header
    c = myfile.read(1)
    while c != "{":
      c = myfile.read(1)
    
    line = myfile.readline()
    while line :
      if len(line) > 3:
        edge = line.replace("\n","").split(" ")[0::2]
        
        for v in edge:
          if not g.is_vertex(v):
            g.add_vertex(v)
        
        g.add_edge (edge[0], edge[1])
        
      line = myfile.readline()

    # we close the file
    myfile.close ()

    return g
