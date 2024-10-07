import json
import glob
from tools import *
#TODO: parser d'arguments
#argv 1 : liste de versions
#argv 2 (optionnel): GT
#argv 3 : utiliser clustering  et similarité
#argv 4 : utiliser base de connaissance
#Pour chaque entité calculer ses TF (vecteur) et son IDF
#séparer entités et étiquettes
#Exploiter la longueur

def count_entities(lists_entities):
  """
  Outputs a vector for each entity with its tf in each list
  """
  entity_stats = {}
  for cpt, l in enumerate(lists_entities):
    for ent in l:
      entity_stats.setdefault(ent, [0]*len(lists_entities))
      entity_stats[ent][cpt]+=1
  print(ent, entity_stats[ent])
  return entity_stats

def filter_entities(entity_stats, min_df =2, min_tf=1, min_len=2):
  filtered = {}
  print(f"Before filtering : {len(entity_stats)}")
  for entity, stats in entity_stats.items():
    #Add clean entity (spaces ??)
    if len(entity)<min_len:
      continue
    if len([x for x in stats if x>=min_tf])<min_df:
      continue
    filtered[entity] = stats
  print(f"After  filtering : {len(filtered)}")
  return filtered
    
def evaluate(entity_ref, ent_before, ent_after):
  positives = set(entity_ref.keys())
  for situation, data in [["before", ent_before], ["after", ent_after]]:
    print(f"Evaluation {situation} filtering")
    VP = set(data.keys()).intersection(positives)
    FP = set(data.keys()).difference(positives)
    FN = positives.difference(set(data.keys()))
    if len(VP) == 0:
      R, P, F = 0, 0, 0
    else:
      R = round(len(VP)/(len(VP)+len(FN)), 4)
      P = round(len(VP)/(len(VP)+len(FP)), 4)
      F = (2*P*R)/(P+R)
    res= {"Recall": R, "Precision": P, "F-score":F}
    print(json.dumps(res, indent =2))


def get_entities(path_versions, path_ref, filter_misc):
  all_entities = [get_entity_json_file(path, filter_misc) for path in path_versions]
  entity_stats = count_entities(all_entities)
  filtered_entities = filter_entities(entity_stats, min_df =2, min_tf=1, min_len=2)
  if path_ref is not None:
    entity_ref =count_entities([get_entity_json_file(path_ref, filter_misc)])
    evaluate(entity_ref, entity_stats, filtered_entities)
  return filtered_entities

def main_func(path_versions, path_ref= None, filter_misc=False):
  """
  Path with json files in appropriate format
  path_ref used for evaluation (not mandatory)
  """
  filtered_entities = get_entities(path_versions, path_ref, filter_misc)
  return filtered_entities

if __name__=="__main__":
  path_noisy = "DATA/Example/Versions/"
  path_silver= "DATA/Example/Silver/"
  
  path_silver_file = glob.glob(f"{path_silver}/*.json")[0]
  path_noisy_files = glob.glob(f"{path_noisy}/*.json")
  
  for filter_misc in [False, True]:
    print(f"Filter_misc : {filter_misc}")  
    res = main_func(path_noisy_files, path_silver_file, filter_misc)

    path_out = f"tmp_filter_misc={filter_misc}.json"
    with open(path_out, "w") as w:
      w.write(json.dumps(res,indent=2, ensure_ascii=False))
    print(f"Output written in {path_out}")
