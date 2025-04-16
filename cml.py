import xml.etree.ElementTree as ET
from graph import *
import sys

class CML_Collection:
  """ This class allows for representing the graph related to each molecule of a collection of """
  
  def __init__ (self) -> None:
    """ creates an empty collection  """
    self.__collection = []
    
    
  def read (self, filename: str) -> None:
    """ reads the collection from the given CML file """    
    tree = ET.parse(filename)
    root = tree.getroot()
    for child in root:    
      if "molecule" in child.tag:
        # we consider each molecule
        mol = Graph()
        
        for data_type in child:
          if "atomArray" in data_type.tag:
            # we get the list of carbons atoms
            for atom in data_type:
              if atom.attrib["elementType"] == "C":
                mol.add_vertex(atom.attrib["id"]) 
          elif "bondArray" in data_type.tag:
            # we get the list of bonds between carbon atoms
            for bond in data_type:
              a,b = bond.attrib["atomRefs2"].split(" ")
              if mol.is_vertex(a) and mol.is_vertex(b): 
                mol.add_edge(a,b)

        self.__collection.append(mol)
  

  def get_size(self):
    """ returns the size of the collection """
    return len(self.__collection)


  def get_benzenoid_number(self) -> dict:
    """ returns the numbers of benzenoids in the collection depending on the number of hexagons """
    nb = {}
    k = 0
    
    for mol in self.__collection:
      if mol.is_benzenoid():
        n = mol.get_hexagon_number()
        if n not in nb:
          nb[n] = 0
        nb[n] += 1
        
    return nb


if __name__ == "__main__":
  if len(sys.argv) != 2:
    print ("Usage:",sys.argv[0],"cml-file")
    exit(0)
  filename = sys.argv[1]
  CML_collection = CML_Collection()
  CML_collection.read(filename)
  print ("Collection", filename)
  print ("\t# molecules:",CML_collection.get_size())
  print ("\t# benzenoids:",CML_collection.get_benzenoid_number())
