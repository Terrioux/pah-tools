class Graph:
  """ this class allows for expressing undirected graphs with labeled edges """
  
  def __init__ (self) -> None:
    """ creates an empty graph """
    self.__n = 0
    self.__m = 0
    self.__adjacency_list = {}


  def get_vertex_number (self) -> int:
    """ returns the number of vertices """
    return self.__n

  
  def get_edge_number (self) -> int:
    """ returns the number of edges """
    return self.__m


  def is_vertex (self,x) -> bool:
    """ returns True if x is a vertex of the graph, False otherwise """
    return x in self.__adjacency_list
    
  
  def add_vertex (self,x) -> None:
    """ adds the vertex x to the graph """
    if x not in self.__adjacency_list:
      self.__n = self.__n + 1
      self.__adjacency_list[x] = {}


  def get_vertices (self) -> list:
    """ returns the list of vertices """
    return list(self.__adjacency_list)


  def is_edge (self,x,y) -> bool:
    """ returns True if the edge {x,y} exists, False otherwise """
    if x in self.__adjacency_list :
      if y in self.__adjacency_list:
        return y in self.get_neighbors(x)
      else:
        raise ValueError("Unknown vertex "+str(y))
    else:
      raise ValueError("Unknown vertex "+str(x))


  def add_edge (self,x,y) -> None:
    """ adds the edge {x,y} to the graph with a None label """
    if not self.is_edge(x,y):
       self.__adjacency_list[x][y] = None
       self.__adjacency_list[y][x] = None
       self.__m = self.__m + 1


  def get_neighbors (self,x) -> list:
    """ returns the list of neighbors of x """
    if x in self.__adjacency_list.keys():
      return list(self.__adjacency_list[x])
    else:
      return []


  def get_edge_label (self,x,y):
    """ returns the label related to the edge {x,y} if it exists, None otherwise """
    if x in self.__adjacency_list :
      if y in self.__adjacency_list:
        if y in self.__adjacency_list[x]:
          return self.__adjacency_list[x][y]
        else:
          return None
      else:
        raise ValueError("Unknown vertex "+str(y))
    else:
      raise ValueError("Unknown vertex "+str(x))

  
  def set_edge_label (self,x,y,l):
    """ sets the label l to the edge {x,y} """
    if x in self.__adjacency_list :
      if y in self.__adjacency_list:
        if y in self.__adjacency_list[x]:
          self.__adjacency_list[x][y] = l
          self.__adjacency_list[y][x] = l
        else:
          raise ValueError("Unknown edge {"+str(x)+","+str(y)+"}")
      else:
        raise ValueError("Unknown vertex "+str(y))
    else:
      raise ValueError("Unknown vertex "+str(x))

  
  
  def get_edges (self) -> list:
    """ returns the list of edges of the graph """
    return [(x,y) for x in self.__adjacency_list for y in self.get_neighbors(x) if x < y]
  
  
  def __str__ (self) -> str:
    """ returns a string describing the graph """
    s = ""
    for x in self.__adjacency_list.keys():
      s = s + "Neighbors of " + str(x) + ": " + str(self.get_neighbors(x)) + "\n"
    return s


  def copy (self):
    """ returns a copy of the current graph """
    g = Graph()
    for v in self.get_vertices():
      g.add_vertex(v)
    for edge in self.get_edges():
      g.add_edge(edge[0],edge[1])
      g.set_edge_label(edge[0],edge[1],self.get_edge_label(edge[0],edge[1]))
    return g
