import numpy as np
from modAL.models import ActiveLearner
from foil.foil_model import FoilBase
from foil.foil_types import FoilX

""" Similarity """
def similarity_sample(al_type, *args):
    if isinstance(al_type, str):
        if al_type == 'Bird':
            # print("Using bird similarity")
            return similarity_sample_bird(*args)
        elif al_type == 'Default':
            # print("Using default similarity")
            return similarity_sample_default(*args)
        elif al_type == 'Medical':
            # print("Using med similarity")
            return similarity_sample_med(*args)
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
""" End of similarity"""

""" Informativeness """
def informativeness_query_strategy_2(mode, classifier: ActiveLearner, X: FoilX, n_instances: int = 1) -> np.ndarray:
    X_satis_list = []
    # Calculate informativeness score for each sublist
    # info_result = [measure_individual_informativeness_score(mode, sample, classifier.estimator) for sample in X]
    rule_result, x_satis_list = classifier.estimator.predict(X, rt_satis_list=True)
    info_result = [measure_individual_informativeness_score2(mode, rule_result[i], x_satis_list[i]) for i in range(len(X))]
    # Normalize
    if max(info_result) - min(info_result) != 0:
        X_satis_list = [x - min(info_result) / max(info_result) - min(info_result) for x in info_result]
    else:
        X_satis_list = info_result
    # Sort index
    X__sorted_index = np.argsort(X_satis_list)[:n_instances]
    # print("Sorted index by informativeness: ", np.argsort(X_satis_list))
    
    return X__sorted_index, np.array(X)[X__sorted_index]

def measure_individual_informativeness_score2(mode, rule_result, x_satis_list, verbose=False) -> float:
    if mode == 0:  # Conflict
        if len(rule_result) > 1:
            return len(rule_result)
        return 0
    # This block is for different lambda values
    elif mode == 1:  # lambda = 1
        res_score = satis_score_avg(x_satis_list, 1)
        return res_score
    elif mode == 2:  # lambda = 0.2
        res_score = satis_score_avg(x_satis_list, 0.2)
        return res_score
    elif mode == 6:  # lambda = 0.6
        res_score = satis_score_avg(x_satis_list, 0.6)
        return res_score
    else:  # entropy
        res_score = satis_score_entropy(x_satis_list)
        return res_score

# Helpers
def satis_score(x_satis_list: list[float]) -> float:
    return satis_score_avg(x_satis_list)

def satis_score_avg(x_satis_list: list[float], lam) -> float:
    if x_satis_list.count(1.0) == 1:
        return 0
    conflict_count = x_satis_list.count(1.0)
    nonsatis_index = np.where(np.array(x_satis_list) != 1.0)[0]
    nonsatis_avg = np.mean(np.array(x_satis_list)[nonsatis_index]) if len(nonsatis_index) > 0 else 1
    return lam * conflict_count + 1 - nonsatis_avg

def satis_score_entropy(x_satis_list: list[float]) -> float:
    if x_satis_list.count(1.0) == 1:
        return 0
    # conflict_count = x_satis_list.count(1.0)
    nonsatis_index = np.where(np.array(x_satis_list) != 1.0)[0]
    nonsatis_list = np.array(x_satis_list)[nonsatis_index]
    nonsatis_entropy = np.sum(-nonsatis_list @ np.log2(nonsatis_list, where=nonsatis_list>0).T) if len(nonsatis_index) > 0 else 0
    return nonsatis_entropy

def get_objects(X):
    X_objs = []
    for x in X:
        objs = []
        objs_raw: dict[str, object] = x['object_detect']['object']
        for idx, value in objs_raw.items():
            objs.append(value['name'])
        X_objs.append(objs)
    return X_objs


def get_panel_obj(X_objs):
    common_objs = [el for sublist in X_objs for el in sublist]
    return max(common_objs, key=common_objs.count)


def get_panel(X_objs, y):
    results = {}
    for i in range(0,len(X_objs)):
        if y[i] not in results:
            results[y[i]] = []
        results[y[i]].append(i)
    output = {}
    for key, value in results.items():
        temp = []
        for item in value:
            temp.append(X_objs[item])
        output[key] = get_panel_obj(temp)
    return output


def min_max_norm(results):
    norm_list = []
    min_value = min(results)
    max_value = max(results)
    for value in results:
        tmp = (value - min_value) / (max_value - min_value)
        norm_list.append(tmp)
    return norm_list


def measure_informativeness_all(X):
    results = np.zeros(len(X), int)
    X_objs = get_objects(X)
    panel = get_panel_obj(X_objs)
    for i in range(0, len(X)):
        objs = X_objs[i]
        unique_objts = np.unique(objs)
        results[i] += len(objs)
        if panel in unique_objts:
            results[i] -= objs.count(panel)
    return min_max_norm(results)


def measure_informativeness_certain(X, sample):
    results = np.zeros(len(X), int)
    X_objs = get_objects(X)
    panel = get_panel_obj(X_objs)
    sample_objs = get_object_lst(sample)
    for i in range(0, len(X)):
        objs = X_objs[i]
        results[i] += len(objs)
        results[i] -= objs.count(panel)
    np.append(results, len(sample_objs) - sample_objs.count(panel))
    return min_max_norm(results)[-1]

""" End of informativeness """

""" Diversity """
def diversity_sampling_strategy_global(classifier, X, test, al_type, n_instances=1):

    # Global Consideration
    centroids = np.random.choice(range(len(X)), size=n_instances, replace=False)
    changed, newCentroids = Update_cen(X, centroids, n_instances, test, classifier, al_type)
    while changed > 0:
        changed, newCentroids = Update_cen(X, newCentroids, n_instances, test, classifier, al_type)
    centroids = newCentroids
    cluster = []
    dis = Distance(X, centroids, n_instances, test, classifier, al_type)
    maxIndex = np.argmax(dis, axis=1)
    for i in range(n_instances):
        cluster.append([])
    for i, j in enumerate(maxIndex):
        cluster[j].append(i)

    return centroids, np.array(X)[centroids]


# Helper
def Distance(dataSet, centroids, k, test, estimator: FoilBase, al_type) -> np.array:
    dis = []
    for idex, sample in enumerate(dataSet):
        cent_sim = []
        for cent in centroids:
            if idex != cent:
                cent_sim.append(similarity_sample(al_type, sample, dataSet[cent], test, estimator))
            else:
                cent_sim.append(9999)
        dis.append(np.array(cent_sim))
    dis = np.array(dis)
    return dis


def Update_cen(dataSet, centroids, k, test, estimator: FoilBase, al_type):
    distance = Distance(dataSet, centroids, k, test, estimator, al_type=al_type)
    maxIndex = np.argmax(distance, axis=1)
    cluster = []
    for i in range(k):
        cluster.append([])
    for i, j in enumerate(maxIndex):
        cluster[j].append(i)
    newCentroids = []
    for i in range(k):
        sam_sum_lst = []
        for sample in cluster[i]:
            sam_sum = 0
            for other_sam in cluster[i]:
                sam_sum += similarity_sample(al_type, dataSet[sample], dataSet[other_sam], test, estimator)
            sam_sum_lst.append(sam_sum)
        index_lst = [cluster[i][j] for j, value in enumerate(sam_sum_lst) if value == max(sam_sum_lst)]
        # print("index_lst", index_lst)
        if index_lst:
            max_index = index_lst[0]
        else:
            max_index = []
        newCentroids.append(max_index)
    # print("newCentroids: ", newCentroids)
    # print("oldCentroids: ", centroids)

    # changed = newCentroids - centroids
    changed = 0
    # print(al_type(centroids))
    for cen in newCentroids:
        if cen not in centroids:
            changed += 1
    # print(changed)

    return changed, newCentroids
""" End of diversity """

""" Factory method for creating strategies."""
def strategy_factory(sim_mode, lambda_mode, m, al_type="Default"):
    def strat(classifier, X, n_instances):
        # intermediate set m
        interm_idx, interm_set = informativeness_query_strategy_2(lambda_mode, classifier, X, n_instances=m)
        n = n_instances
        cent = []
        centx = None
        while n != 0:
            a, b = diversity_sampling_strategy_global(classifier.estimator, interm_set, sim_mode, al_type, n)
            interm_set = np.delete(interm_set, a, axis=0)
            cent.extend(a)
            if not centx:
                centx = b
            else:
                centx.extend(b)
            n -= len(a)
        idx = []
        for selected in centx:
            idx.append(next((index for (index, d) in enumerate(X) if d["imageId"] == selected["imageId"]), None))
        return idx, centx
    return strat


def diversity_factory(sim_mode, al_type='Default'):
    def diversity(classifier, X, n_instances):
        X_use = np.copy(X)
        n = n_instances
        cent = []
        centx = None
        while n != 0:
            a, b = diversity_sampling_strategy_global(classifier.estimator, X_use, sim_mode, n, al_type=al_type)
            X_use = np.delete(X_use, a, axis=0)
            cent.extend(a)
            if not centx:
                centx = b
            else:
                centx.extend(b)
            n -= len(a)
        idx = []
        for selected in centx:
            idx.append(next((index for (index, d) in enumerate(X) if d["imageId"] == selected["imageId"]), None))
        return idx, centx
    return diversity


def informative_factory(lambda_mode):
    # If lambda_mode is 1, 2, 6, we have a lambda = 1, 0.2, 0.6
    # If lambda_mode is 0 and 10, we have conflict and entropy
    def lonely_info(classifier, X, n_instances):
        return informativeness_query_strategy_2(lambda_mode, classifier, X, n_instances)
    return lonely_info
""" End of factory methods"""