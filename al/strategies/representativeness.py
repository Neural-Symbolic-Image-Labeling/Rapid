
from numbers import Number
import numpy as np
from modAL.models import ActiveLearner
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from foil.foil_model import FoilImageClassifier

from .utils import similarity_sample


def representativeness_query_strategy(classifier: ActiveLearner, X, n_instances=1):
    model: FoilImageClassifier = classifier.estimator
    X_utility = compute_utility(X, model)
    X_utility_sorted_idx = np.argsort(X_utility)
    print(f"Selected idx by representative: {X_utility_sorted_idx[-n_instances:]}")
    return X_utility_sorted_idx[-n_instances:], X[-n_instances:]

def compute_rep_against_all(x, X, test, classifier):
    """
    Compute utility of x against all other data in X.
    """
    density = 0
    for i in range(len(X)):
        if x == X[i]:
            continue
        density += similarity_sample(x, X[i], test, classifier)
    return density / (len(X) - 1)

# Helpers

def compute_utility(X, model: FoilImageClassifier):
    """
    Compute the utility of the given data.
    """
    X_vec_basic = featurelize_basic(X, model.get_object_list())
    n = len(X)
    result = []
    for i in range(n):
        density = 0
        for j in range(n):
            if i == j:
                continue
            # concat new features on xi and xj
            ## xi
            xi_basic_vec = X_vec_basic[i]
            xi_overlap_vec = featurelize_overlap(X[i], X[j])

            xi_vec = np.array(xi_basic_vec + xi_overlap_vec)
            ## xj
            xj_basic_score = X_vec_basic[j]
            xj_overlap_vec = featurelize_overlap(X[i], X[j])

            xj_vec = np.array(xj_basic_score + xj_overlap_vec)

            # calculate similarity
            # density += compute_similarity_measure(xi_vec, xj_vec)
            density += similarity_sample(X[i], X[j])
        result.append(density / (n - 1))
    
    
def featurelize_overlap(x1, x2):
    """
    Featurelize the given data X by counting same overlaps.

    @param X: The data to featurelize.
    @param object_lst: The list of objects for the data.
    @return: The featurelized data for overlap only.
    """
    return []

def compute_similarity_measure(x1, x2):
    """
    Compute the similarity measure of the given data.
    formula: (x1 * x2) / ||x1|| ||x2||
    """
    return np.dot(x1, x2) / (np.linalg.norm(x1) * np.linalg.norm(x2))

def featurelize_basic(X, object_lst: list[str]):
    """
    Featurelize the given data X by mapping objects to one-hot vectors.

    @param X: The data to featurelize.
    @param object_lst: The list of objects for the data.
    @return: The featurelized data.
    """
    X_objs = get_objects(X)
    X_vectors = []
    for x in X_objs:
        vec = [0 for _ in range(len(object_lst))]
        for obj in x:
            if obj in object_lst:
                vec[object_lst.index(obj)] = 1
            # else:
            #     print(f"Object not found: {obj}")
        X_vectors.append(vec)
    return X_vectors

def get_objects(X) -> list[list[str]]:
    """
    Parse each input into a list of objects it contains.

    @param X: The data to get the list of objects from.
    @return: The 2d list of objects.
    """
    X_objs = []
    for x in X:
        objs = []
        objs_raw: dict[str, object] = x['object_detect']['object']
        for idx, value in objs_raw.items():
            objs.append(value['name'])
        X_objs.append(objs)
    return X_objs

if __name__ == '__main__':
    from data import ClassificationDataManager
    dataM = ClassificationDataManager()
    X, X_unlabeled, y = dataM.get_data_from_file()
    model = FoilImageClassifier()
    model.fit(X, y)
    # print(model.print_object_list())
    print('====================')
    result = featurelize_basic(X, model.get_object_list())
    print(compute_similarity_measure(result[0], result[2]))
    pass