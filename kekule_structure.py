from graph import *

class Kekule_Structure():
  """ this class allows for representing a Kekulé structure of a molecule """
  
  def __init__ (self, g: Graph, labelling: list) -> None:
    """ creates a Kekulé from a graph and a valid edge labelling """
    super().__init__()
    self.__g = g.copy()
    
    for edge,label in labelling:
      self.__g.set_edge_label (edge[0],edge[1],label)
      self.__g.set_edge_label (edge[1],edge[0],label)
      
    self.__conjugated_circuits = {}

  
  def save (self, filename):
    """ saves the Kekule structure in a dot file """
     # we open the file
    myfile = open (filename,"w")

    # we write the header
    myfile.write("strict graph {\n")
    
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


  def find_conjugated_circuits (self) -> list:
    """ returns the list of conjugated circuits of the Kekulé structure """
    self.__conjugated_circuits = {}
    x = self.__g.get_vertices()[0]    # we start with the first vertex (this choice is arbitrary)
    for v in self.__g.get_neighbors(x):
      if self.__g.get_edge_label(x,v) == 1:  # we consider the double bound involving x
        self.find_conjugated_circuits_rec ([x,v])
        
    return self.__conjugated_circuits
  
  
  def find_conjugated_circuits_rec (self, path):
    """ extends the current path with the aim of finding new conjugated circuits """
    for v in self.__g.get_neighbors(path[-1]):
      if self.__g.get_edge_label(path[-1],path[-2]) != self.__g.get_edge_label(path[-1],v):
        if v in path:
          pos = path.index(v)
          circuit = path[pos:]  # we define the found conjugated circuit
          
          if len(circuit) % 2 == 0:
            # only even circuits are considered
            if len(circuit) in self.__conjugated_circuits:  # we check whether this circuit is new
              i = 0
              while i < len(self.__conjugated_circuits[len(circuit)]) and set(circuit) != set(self.__conjugated_circuits[len(circuit)][i]):
                i += 1
              if i == len(self.__conjugated_circuits[len(circuit)]):
                # we have a new circuit
                self.__conjugated_circuits[len(circuit)].append(circuit[circuit.index(min(circuit)):]+circuit[:circuit.index(min(circuit)):])
            else:
              # we have a new circuit (with a new size)
              self.__conjugated_circuits[len(circuit)] = [circuit[circuit.index(min(circuit)):]+circuit[:circuit.index(min(circuit)):]]
        else:
          self.find_conjugated_circuits_rec (path+[v])

