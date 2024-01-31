from graph import *
from auxiliary_functions import *


class Face_Graph (Graph):
  """ this class allows for expressing faces graphs with labeled edges """
  
  def __init__ (self, g) -> None:
    """ creates the face graph of the graph g (excluding the external face) """
    super().__init__()
    self.__g = g
    self.__faces = []

    # we compute all the possible cycles
    cycles = self.__g.find_cycles()
    
    # we deduce the faces of the graph
    sizes = sorted(cycles.keys())
    
    self.__faces = cycles[sizes[0]]
    
    for size in sizes[1:]:
      for c in cycles[size]:
        inter = [len(set(c) & set(f)) for f in self.__faces]
        if max(inter) <= 2:
          self.__faces.append(c)
    
    # we build the face graph
    for i in range(len(self.__faces)):
      self.add_vertex(i)
    
    for i in range(len(self.__faces)-1):
      for j in range(i+1,len(self.__faces)):
        if len(set(self.__faces[i]) & set (self.__faces[j])) == 2:
          self.add_edge(i,j)
          
    
    # we build clockwise circuits (the term clockwise is arbitrary, since it depends on the way the molecule is drawn)
    self.__clockwise_circuits = [self.__faces[0]]  # the first face defines an arbitrary orientation

    stack = [0]
    done = []
    
    # we orientate each face in the same way as the first one
    while len(stack) > 0 and len(self.__clockwise_circuits) < len (self.__faces):
      f = stack.pop()
      done.append(f)

      for n in self.get_neighbors(f):
        if n not in done and n not in stack:
          common_edge = list(set(self.__faces[f]) & set (self.__faces[n]))    # we identify the two common vertices          
          if arc_direction(self.__faces[f],common_edge[0],common_edge[1]) == arc_direction(self.__faces[n],common_edge[0],common_edge[1]):
            # the arc is in the same direction in the two circuits, so we reverse the second circuit
            self.__clockwise_circuits.append(self.__faces[n][::-1])
            self.__faces[n] = self.__faces[n][::-1]
          else:
            # the arc has a different direction depending on the considered circuit, so we keep the second circuit as it is
            self.__clockwise_circuits.append(self.__faces[n])

          stack.append(n)

    
  def get_face (self, i: int) -> list:
    """ returns the ith face of g """
    if 0 <= i < len(self.__faces):
      return self.__faces[i].copy()
    else:
      return []


  def get_faces (self) -> list:
    """ returns the ith face of g """
    return self.__faces.deepcopy()
    
    
  def give_orientation (self, conjugated_circuit):
    """ defines the orientation of a conjugated circuit and returns it """
    # we look for a face that shares the largest number of arcs with the conjugated circuit
    inter_max = set()
    for c in self.__clockwise_circuits:
      inter = set(conjugated_circuit) & set(c)
      if len(inter) > len(inter_max):
        inter_max = inter
        c_max = c

    i = 0
    while not set(conjugated_circuit[i:i+2]) <= inter_max:
      i += 1

    if len(conjugated_circuit) % 4 == 2:
      # the circuit is aromatic
      if arc_direction(c_max,conjugated_circuit[i],conjugated_circuit[i+1]) == arc_direction(conjugated_circuit,conjugated_circuit[i],conjugated_circuit[i+1]):
        return conjugated_circuit
      else:
        return conjugated_circuit[::-1]
    elif len(conjugated_circuit) % 4 == 0:
      # the circuit is anti-aromatic
        if arc_direction(c_max,conjugated_circuit[i],conjugated_circuit[i+1]) == arc_direction(conjugated_circuit,conjugated_circuit[i],conjugated_circuit[i+1]):
          return conjugated_circuit[::-1]
        else:
          return conjugated_circuit
    else:
      raise ValueError ("invalid conjugated circuit ("+str(conjugated_circuit)+")")
