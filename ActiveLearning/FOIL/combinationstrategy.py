import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

import matplotlib as mpl

mpl.use('Agg')

import numpy as np
import copy
import platform

from sklearn.model_selection import train_test_split

from FoilModel import FoilImageClassifier
from data import ClassificationDataManager
from FOIL.strategies.informativeness import *
from FOIL.strategies.diversity import diversity_sampling_strategy_global
from FOIL.strategies.utils import *
from FOIL.strategies.representativeness import *


def strategy_factory(sim_mode, lambda_mode, m):
    def strat(classifier, X, n_instances):
        # intermediate set m
        interm_idx, interm_set = informativeness_query_strategy_2(lambda_mode, classifier, X, n_instances=m)
        n = n_instances
        cent = []
        centx = None
        while n != 0:
            a, b = diversity_sampling_strategy_global(classifier.estimator, interm_set, sim_mode, n)
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


def diversity_factory(sim_mode):
    def diversity(classifier, X, n_instances):
        X_use = np.copy(X)
        n = n_instances
        cent = []
        centx = None
        while n != 0:
            a, b = diversity_sampling_strategy_global(classifier.estimator, X_use, sim_mode, n)
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


# # Conflict
# def strategy_1_conflict(classifier, X, n_instances):
#     interm_idx, interm_set = informativeness_query_strategy_2(0, classifier, X, n_instances)
#     return interm_idx, interm_set
#
#
# # Entropy
# def strategy_1_entro(classifier, X, n_instances):
#     interm_idx, interm_set = informativeness_query_strategy_2(10, classifier, X, n_instances)
#     return interm_idx, interm_set


def random_query_strategy(classifier, X, n_instances=1):
    query_idx = np.random.choice(range(len(X)), size=n_instances, replace=False)
    # print(f"Seleted idx by random: {query_idx}")
    return query_idx, X[query_idx]


def uncertainty_sampling_strategy(classifier, X, n_instances=1):
    probs = np.array(classifier.predict_proba(X))
    # print(f"Uncertianty: {probs}")
    query_idx = np.argsort(probs)[-n_instances:]
    # print(f"Seleted to label: {query_idx}")
    return query_idx, X[query_idx]

# def strategy_2_conflcit(classifier, X, n_instances):
#     # Testing add FOIL inter to similarity
#     test = 0
#     batch = []
#     info_result = [measure_individual_informativeness_score(0, sample, classifier.estimator) for sample in X]
#     if max(info_result) - min(info_result) != 0:
#         normal_info_result = [x - min(info_result) / max(info_result) - min(info_result) for x in info_result]
#     else:
#         normal_info_result = info_result
#     rep_result = [compute_rep_against_all(sample, X, test, classifier.estimator) for sample in X]
#     rep_info_result = [0.8 * normal_info_result[i] + 0.2 * rep_result[i] for i in range(len(X))]
#     order = np.argsort(-np.array(rep_info_result))
#     for idx in order:
#         if not rep_info_result:
#             batch.append(idx)
#         else:
#             add = 1
#             for sam in batch:
#                 # Threshold 0
#                 if similarity_sample(X[idx], X[sam], test, classifier.estimator) > 0:
#                     add = 0
#             if add:
#                 batch.append(idx)
#         if len(batch) == n_instances:
#             break
#     if len(batch) != n_instances:
#         sim_result = []
#         new_od = order[len(batch):]
#         for idx in new_od:
#             sim_val = 0
#             for sam in batch:
#                 sim_val += similarity_sample(X[idx], X[sam], test, classifier.estimator)
#             sim_result.append(sim_val)
#         sorted_sim_idx = sorted(range(len(sim_result)), key=lambda x: sim_result[x])[:n_instances - len(batch)]
#         for a in sorted_sim_idx:
#             batch.append(new_od[a])
#     return batch, np.array(X)[batch]

#
#
# def strategy_2_entro(classifier, X, n_instances):
#     # Testing add FOIL inter to similarity
#     test = 0
#     batch = []
#     info_result = [measure_individual_informativeness_score(1, sample, classifier.estimator) for sample in X]
#     normal_info_result = [x - min(info_result) / max(info_result) - min(info_result) for x in info_result]
#     rep_result = [compute_rep_against_all(sample, X, test, classifier.estimator) for sample in X]
#     rep_info_result = [0.8 * normal_info_result[i] + 0.2 * rep_result[i] for i in range(len(X))]
#     order = np.argsort(-np.array(rep_info_result))
#     for idx in order:
#         if not rep_info_result:
#             batch.append(idx)
#         else:
#             add = 1
#             for sam in batch:
#                 # Threshold 0
#                 if similarity_sample(X[idx], X[sam], test, classifier.estimator) > 0:
#                     add = 0
#             if add:
#                 batch.append(idx)
#         if len(batch) == n_instances:
#             break
#     if len(batch) != n_instances:
#         sim_result = []
#         new_od = order[len(batch):]
#         for idx in new_od:
#             sim_val = 0
#             for sam in batch:
#                 sim_val += similarity_sample(X[idx], X[sam], test, classifier.estimator)
#             sim_result.append(sim_val)
#         sorted_sim_idx = sorted(range(len(sim_result)), key=lambda x: sim_result[x])[:n_instances - len(batch)]
#         for a in sorted_sim_idx:
#             batch.append(new_od[a])
#     return batch, np.array(X)[batch]


# Initial

# def strategy_1_init(classifier, X, n_instances):
#     # intermediate set 100
#     # Testing add FOIL inter to similarity
#     test = 0
#     m = 100
#     interm_idx, interm_set = informativeness_query_strategy_2(1, classifier, X, n_instances=m)
#
#     n = n_instances
#     cent = []
#     centx = None
#     while n != 0:
#         a, b = diversity_sampling_strategy_global(classifier.estimator, interm_set, test, n)
#         interm_set = np.delete(interm_set, a, axis=0)
#         cent.extend(a)
#         if not centx:
#             centx = b
#         else:
#             centx.extend(b)
#         n -= len(a)
#     return cent, centx


# def strategy_2_init(classifier, X, n_instances):
#     # Testing add FOIL inter to similarity
#     test = 0
#     batch = []
#     info_result = [measure_individual_informativeness_score(2, sample, classifier.estimator) for sample in X]
#     normal_info_result = [x - min(info_result) / max(info_result) - min(info_result) for x in info_result]
#     rep_result = [compute_rep_against_all(sample, X, test, classifier.estimator) for sample in X]
#     rep_info_result = [0.8 * normal_info_result[i] + 0.2 * rep_result[i] for i in range(len(X))]
#     order = np.argsort(-np.array(rep_info_result))
#     for idx in order:
#         if not rep_info_result:
#             batch.append(idx)
#         else:
#             add = 1
#             for sam in batch:
#                 # Threshold 0
#                 if similarity_sample(X[idx], X[sam], test, classifier.estimator) > 0:
#                     add = 0
#             if add:
#                 batch.append(idx)
#         if len(batch) == n_instances:
#             break
#     if len(batch) != n_instances:
#         sim_result = []
#         new_od = order[len(batch):]
#         for idx in new_od:
#             sim_val = 0
#             for sam in batch:
#                 sim_val += similarity_sample(X[idx], X[sam], test, classifier.estimator)
#             sim_result.append(sim_val)
#         sorted_sim_idx = sorted(range(len(sim_result)), key=lambda x: sim_result[x])[:n_instances - len(batch)]
#         for a in sorted_sim_idx:
#             batch.append(new_od[a])
#     return batch, np.array(X)[batch]

