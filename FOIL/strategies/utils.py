import numpy as np

import sys
import os
import pickle

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))

from FOIL.FoilModel import FoilImageClassifier, FoilBase
from FOIL.data import ClassificationDataManager

def similarity_sample(*args):
    return similarity_sample_default(*args)
    #return similarity_sample_bird(*args)
    #return similarity_sample_med(*args)
    raise NotImplementedError

####################### Default ########################
def similarity_sample_default(s1, s2, test, *args):
    """
    """
    ob_lst_1 = get_object_lst(s1)
    ob_lst_2 = get_object_lst(s2)
    # print(ob_lst_1)
    # print(ob_lst_2)

    ob_dict_1 = get_object_dict(s1)
    ob_dict_2 = get_object_dict(s2)
    # print(ob_dict_1)
    # print(ob_dict_2)
    overlap_lst_1 = get_overlap_lst(s1)
    overlap_lst_2 = get_overlap_lst(s2)
    overlap_sim = common_elements_metric(overlap_lst_1, overlap_lst_2, 2)
    if test == 1:  # Mode 1
        object_sim = common_elements_metric(ob_lst_1, ob_lst_2, 1)
    elif test == 2:  # Mode 2
        object_sim = common_elements_metric2(ob_dict_1, ob_dict_2)
    elif test == 3:  # Mode 3
        object_sim = max(common_elements_metric2(ob_dict_1, ob_dict_2), common_elements_metric(ob_lst_1, ob_lst_2, 1))
    else:  # Mode Jaccard
        object_sim = common_elements_metric_jac(ob_lst_1, ob_lst_2, 1)
        overlap_sim = common_elements_metric_jac(overlap_lst_1, overlap_lst_2, 2)
    # print(object_sim)

    return object_sim + overlap_sim

#################### Medical ########################
def get_med_obj(sample):
    return sample['object_detect']['space']

def to_vector(item):
    """
    Convert an item to a vector
    """
    return np.array(list(item.values()))

def weighted_cosine_distance(vec1, vec2, weights=None):
    if weights is None:
        weights = np.ones(vec1.shape[0])
    return np.dot((vec1 * weights), (vec2 * weights)) / (np.linalg.norm(vec1 * weights) * np.linalg.norm(vec2 * weights))

# Consine distance
def similarity_sample_med(s1, s2, *args):
    """ Similarity func for medical dataset
    """
    # extract object vector
    obj1, obj2 = get_med_obj(s1), get_med_obj(s2)
    vec1, vec2 = to_vector(obj1), to_vector(obj2)

    # compute cosine similarity
    return weighted_cosine_distance(vec1, vec2)

#################### Bird ########################
def similarity_sample_bird(s1, s2, test, *args):
    # For bird dataset
    dict1 = s1['object_detect']
    dict2 = s2['object_detect']
    return common_elements_metric_bird(dict1, dict2)


# def get_object_lst(sample):
#     result = []
#     for key in sample['object_detect']['object']:
#         obj = sample['object_detect']['object'][key]['name']
#         if obj not in result:
#             result.append(obj)
#     return result

def get_object_lst(sample):
    result = []
    for key in sample['object_detect']['object']:
        obj = sample['object_detect']['object'][key]['name']
        if obj not in result:
            result.append(obj)
    for key in sample['panoptic_segmentation']:
        obj = sample['panoptic_segmentation'][key]['name']
        if obj not in result:
            result.append(obj)
    return result

def Union(lst1, lst2):
    final_list = list(set(lst1) | set(lst2))
    return final_list


# def get_object_dict(sample):
#     dict = {}
#     sum_obj = 0
#     for key in sample['object_detect']['object']:
#         obj = sample['object_detect']['object'][key]['name']
#         if obj not in dict:
#             dict[obj] = 0
#         dict[obj] += 1
#         sum_obj += 1
#     dict['sum_obj'] = sum_obj
#     return dict

def get_object_dict(sample):
    dict = {}
    sum_obj = 0
    for key in sample['object_detect']['object']:
        obj = sample['object_detect']['object'][key]['name']
        if obj not in dict:
            dict[obj] = 0
        dict[obj] += 1
        sum_obj += 1
    for key in sample['panoptic_segmentation']:
        obj = sample['panoptic_segmentation'][key]['name']
        if obj not in dict:
            dict[obj] = 0
        dict[obj] += 1
        sum_obj += 1
    dict['sum_obj'] = sum_obj
    return dict


def common_elements_metric(list1, list2, mode):
    if not list1 or not list2:
        return 0
    if mode == 1:
        return len([element for element in list1 if element in list2])/max(len(list1), len(list2))
        # Jaccard
        # return len([element for element in list1 if element in list2])/len(Union(list1, list2))

    if mode == 2:
        acc = 0
        for ele1 in list1:
            for ele2 in list2:
                acc += compare_tuple(ele1[ele1.index('(') + 1:ele1.index(')')], ele2[ele2.index('(') + 1:ele2.index(')')], 2)
        return acc/max(len(list1), len(list2))
        # Jaccard
        # return acc / len(Union(list1, list2))

def common_elements_metric_jac(list1, list2, mode):
    if not list1 or not list2:
        return 0
    if mode == 1:
        # Jaccard
        return len([element for element in list1 if element in list2])/len(Union(list1, list2))

    if mode == 2:
        acc = 0
        for ele1 in list1:
            for ele2 in list2:
                acc += compare_tuple(ele1[ele1.index('(') + 1:ele1.index(')')], ele2[ele2.index('(') + 1:ele2.index(')')], 2)
        # Jaccard
        return acc / len(Union(list1, list2))

def common_elements_metric2(dict1, dict2):
    acc = 0
    for key, value in dict1.items():
        if key in dict2 and key != 'sum_obj':
            if abs(dict1[key] - dict2[key]) <= 2:
                acc += max(dict1[key], dict2[key])
    return acc/min(dict1['sum_obj'], dict2['sum_obj'])


def common_elements_metric_bird(dict1, dict2):
    # Accumulate the same key-value pair in two dict and divide by max dict length
    acc = 0
    for key, value in dict1.items():
        if key in dict2 and dict1[key] == dict2[key]:
            acc += 1
    return acc/max(len(dict1), len(dict2))


def get_overlap_lst(sample):
    result = []
    for key in sample['object_detect']['overlap']:
        overlap_item = 'overlap({},{})'.format(find_object(sample, sample['object_detect']['overlap'][key]['idA']),
                                                find_object(sample, sample['object_detect']['overlap'][key]['idB']))
        is_in = 0
        for item in result:
            if compare_tuple(overlap_item[overlap_item.index('(') + 1:overlap_item.index(')')], item[item.index('(') + 1:item.index(')')], 1):
                is_in = 1
                break
        if not is_in:
            result.append(overlap_item)
    return result

def find_object(sample, index):
    for key in sample['object_detect']['object']:
        if int(key) == index:
            return sample['object_detect']['object'][key]['name']


def compare_tuple(str1, str2, mode):
    # Compare (A,B) with (C,D)
    if mode == 1:
        if str1[:str1.index(',')] == str2[:str2.index(',')] and str1[str1.index(',') + 1:] == str2[str2.index(',') + 1:]:
            return True
        elif str1[:str1.index(',')] == str2[str2.index(',') + 1:] and str1[str1.index(',') + 1:] == str2[:str2.index(',')]:
            return True
        else:
            return False
    if mode == 2:
        # A,B A,B; A,B B,A; A,C A,B B,A; A,C C,B B,C; A,C B,D
        result = 0
        if str1[:str1.index(',')] == str2[:str2.index(',')]:
            result += 0.5
            if str1[str1.index(',') + 1:] == str2[str2.index(',') + 1:]:
                result += 0.5
        elif str1[:str1.index(',')] == str2[str2.index(',') + 1:]:
            result += 0.5
            if str1[str1.index(',') + 1:] == str2[:str2.index(',')]:
                result += 0.5
        elif str1[str1.index(',') + 1:] == str2[:str2.index(',')]:
            result += 0.5
            if str1[:str1.index(',')] == str2[str2.index(',') + 1:]:
                result += 0.5
        elif str1[str1.index(',') + 1:] == str2[str2.index(',') + 1:]:
            result += 0.5
            if str1[:str1.index(',')] == str2[:str2.index(',')]:
                result += 0.5
        return  result



if __name__ == '__main__':
    data_parser = ClassificationDataManager()
    X, X_unlabeled, y = data_parser.get_data_from_file(filename='data_med')
    # data1 = X[1]
    # data2 = X[1]
    # for key in data1['object_detect']['space']:
    #     print(f"{data1['object_detect']['space'][key]}              {data2['object_detect']['space'][key]}\n")
    # print(f"Similarity: {similarity_sample_med(data1, data2)}")
    result = []
    for i in range(len(X)):
        for j in range(i + 1, len(X)):
            result.append(similarity_sample(X[i], X[j]))
    # find least 10 similar
    pivot_index = np.argpartition(result, 10)[10]
    pivot = result[pivot_index]
    
    # Extract the 10 least numbers from the list
    least_numbers = [num for num in result if num < pivot][:10]
    print(least_numbers)
    