import sys
import os
from tabnanny import verbose
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../.."))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from numbers import Number
import numpy as np

from modAL.models import ActiveLearner
from foil.foil_model import FoilImageClassifier, FoilBase
from .utils import *
from foil.foil_types import *


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

# def measure_individual_informativeness_score(mode, x: FoilXItem, estimator: FoilBase, verbose=False) -> float:
#     rule_result, x_satis_list = estimator.predict([x], rt_satis_list=True)
#     if mode == 0:  # Conflict
#         if len(rule_result[0]) > 1:
#             return len(rule_result[0])
#         return 0
#     # elif mode == 1:  # entropy
#     #     res_score = satis_score_entropy(x_satis_list[0])
#     #     return res_score
#     # else:  # initial
#     #     res_score = satis_score_avg(x_satis_list[0], 1)
#     #     return res_score
#     # x_satis_list = [[0.7, 0.7, 0.7]]
#     # Calculate informativeness score for x
#     # res_score = satis_score(x_satis_list[0])
#     # if verbose:
#     #     print("x_satis_list: ", x_satis_list)
#     #     print("Informativeness score: ", res_score)
#     # return res_score
#
#     # This block is for different lambda values
#     elif mode == 1:  # lambda = 1
#         res_score = satis_score_avg(x_satis_list[0], 1)
#         return res_score
#     elif mode == 2:  # lambda = 0.6
#         res_score = satis_score_avg(x_satis_list[0], 0.6)
#         return res_score
#     else:   # lambda = 0.2
#         res_score = satis_score_avg(x_satis_list[0], 0.2)
#         return res_score


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


if __name__ == '__main__':
    from data import ClassificationDataManager
    dataM = ClassificationDataManager()
    X, X_unlabeled, y = dataM.get_data_from_file()
    model = FoilImageClassifier()
    model.fit(X, y)
    learner = ActiveLearner(
        estimator=model,
        # query_strategy=uncertainty_sampling_strategy,
        query_strategy = informativeness_query_strategy_2,
        X_training=X, y_training=y
    )
    print(measure_individual_informativeness_score(X[1], model, verbose=True))
    # print(informativeness_query_strategy_2(learner, X, n_instances=3))

