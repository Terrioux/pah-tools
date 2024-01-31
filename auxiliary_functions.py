def arc_direction (circuit, x, y) -> bool:
  """ returns True if the arc linking vertices x and y goes from x to y in the circuit defined by the list vertices, False if it goes from y to x """
  index0 = circuit.index(x)
  index1 = circuit.index(y)
  if  (index0 == 0 and index1 == len(circuit)-1):   
    # x is the first vertex and y the last one, so we have the arc (y,x)
    return False
  elif (index0 == len(circuit)-1) and index1 == 0:
    # x is the last vertex and y the first one, so we have the arc (x,y)
    return True
  else: 
    # general case
    return index0 < index1
