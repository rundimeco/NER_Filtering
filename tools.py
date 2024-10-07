import json
def get_entity_json_file(path, filter_misc):
  """
  From json_path outputs only entity occurrences
  """
  with open(path) as f:
    liste = json.load(f)
  if type(liste[0]) is str:
    return liste
  elif type(liste[0]) is not list:
    print("Expected list of lists or list of strings, got this:")
    print(type(liste[0]), liste[0])
    exit() 
  if len(liste[0])==1:
    return liste
  elif len(liste[0])==2:
    if filter_misc==True:
      liste= [x for x in liste if x[1]!="MISC"]
    return [x[0] for x in liste]
  else:
    print(path)
    print(f"Got {len(liste[0])} elements, expected 1 (entity) or 2 (entity + class)")
    print(liste[0])
    exit()
