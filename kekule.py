from pycsp3 import *
from kekule_structure import *

class Kekule:
  """ this class allows for dealing with Kekule structure computations """

  def __init__ (self, g:Graph) -> None:
    self.__g = g
    self.__edges = g.get_edges()
    self.compute()


  def compute (self):
    """ define the PyCSP3 model """
    self.__model_defined = True
    # we define the variables
    
    # each variable correspond to a bound of the molecule
    bounds = VarArray (size=self.__g.get_edge_number(), dom=range(2))
    self.bounds=bounds
    
    # constraints
    for x in self.__g.get_vertices():
      scope = []
      for y in self.__g.get_neighbors(x):
        if x < y:
          scope.append(bounds[self.__edges.index((x,y))])
        else:
          scope.append(bounds[self.__edges.index((y,x))])
      
      satisfy (sum (scope) == 1)
  
    self.__result = solve (sols = ALL)
    if self.__result is SAT:
      self.__solutions = [zip(self.__edges, values (bounds, sol=i)) for i in range (n_solutions())]
    else:
      self.__solutions = []

  
  def get_kekule_structures_number (self) -> int:
    """ returns the number of Kekulé structures """
    return len(self.__solutions)
    
  
  def get_kekule_structures (self) -> list:
    """ returns the list of all the Kekulé structures """
    return [Kekule_Structure(self.__g,s) for s in self.__solutions]
