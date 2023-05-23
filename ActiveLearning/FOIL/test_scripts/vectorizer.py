import numpy as np
import csv
import json
import itertools

def vectorize_medical():
    with open("FOIL/data_file/medical/medical.json", "r") as f:
        data = json.load(f)
        with open("data_med.csv", "w") as f:
            writer = csv.writer(f)
            writer.writerow(['imageId']+list(data[0]['object_detect']['space'].keys())+['type'])
            for item in data:
                writer.writerow([item['imageId']]+list(item['object_detect']['space'].values())+[item['type']])
                
def vectorize_bird():
    with open("FOIL/data_file/bird/bird_171172173.json", 'r') as f:
        data = json.load(f)
        with open("data_bird171172173.csv", "w") as f:
            writer = csv.writer(f)
            writer.writerow(['imageId']+list(data[0]['object_detect'].keys())+['type'])
            for item in data:
                writer.writerow([item['imageId']]+list(item['object_detect'].values())+[item['type']])

def vectorize_adorprof():
    with open("FOIL/data_file/prof/prof_new.json", 'r') as f:
        data = json.load(f)

        obj_set = set()
        for item in data:
            for obj in item['object_detect']['object'].values():
                obj_set.add(obj['name'])
        obj_set_lst = list(obj_set)
        obj_overlaps_full = list(set(frozenset(comb) for comb in itertools.combinations_with_replacement(obj_set_lst, 2)))
        
        print(f"objects: {len(obj_set_lst)}, overlaps: {len(obj_overlaps_full)}")
        with open("data_prof_new.csv", "w") as f:
            writer = csv.writer(f)
            writer.writerow(['imageId']+obj_set_lst+[f"({'-'.join(list(e))})" for e in obj_overlaps_full]+['type'])
            for item in data:
                id = item['imageId']
                img_type = item['type']
                
                obj_vec = [0]*len(obj_set_lst)
                # object vector
                for obj in item['object_detect']['object'].values():
                    obj_vec[obj_set_lst.index(obj['name'])] += 1

                overlap_vec = [0]*len(obj_overlaps_full)
                # object overlap vector
                for ov_item in item['object_detect']['overlap'].values():
                    itemA = item['object_detect']['object'][str(ov_item['idA'])]['name']
                    itemB = item['object_detect']['object'][str(ov_item['idB'])]['name']
                    overlap_vec[obj_overlaps_full.index(frozenset([itemA, itemB]))] += 1

                result = [id]+obj_vec+overlap_vec+[img_type]
                assert len(result) == len(obj_set_lst)+len(obj_overlaps_full)+2
                writer.writerow(result)


                


if __name__ == "__main__":
    # vectorize_medical()
    # vectorize_bird()
    vectorize_adorprof()