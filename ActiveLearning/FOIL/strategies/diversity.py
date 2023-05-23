import random
import numpy as np
import pandas as pd
from FOIL.FoilModel import FoilImageClassifier, FoilBase

from FOIL.strategies.utils import *

def diversity_sampling_strategy_global(classifier, X, test, n_instances=1):

    # Global Consideration
    # print(f'X_pool: {X.shape}, n_instances: {n_instances}\n')
    centroids = np.random.choice(range(len(X)), size=n_instances, replace=False)
    # print("centroids：", centroids)
    changed, newCentroids = Update_cen(X, centroids, n_instances, test, classifier)
    # print("length of centriod of first update_cen", len(newCentroids))
    # print("Current cen", newCentroids)
    while changed > 0:
        changed, newCentroids = Update_cen(X, newCentroids, n_instances, test, classifier)

    # centroids = sorted(newCentroids.tolist())
    centroids = newCentroids
    cluster = []
    dis = Distance(X, centroids, n_instances, test, classifier)
    maxIndex = np.argmax(dis, axis=1)
    for i in range(n_instances):
        cluster.append([])
    for i, j in enumerate(maxIndex):
        cluster[j].append(i)

    # return centroids, cluster
    # print("Diversity Success")
    # print(type(centroids))
    # print(type(np.array(X)[centroids]))

    return centroids, np.array(X)[centroids]


# Helper
def Distance(dataSet, centroids, k, test, estimator: FoilBase) -> np.array:
    # print("current length of centroids", len(centroids))
    # print("Current cen", centroids)
    dis = []
    for idex, sample in enumerate(dataSet):
        # if sample not in centroids:
        cent_sim = []
        for cent in centroids:
            if idex != cent:
                cent_sim.append(similarity_sample(sample, dataSet[cent], test, estimator))
            else:
                cent_sim.append(9999)
        dis.append(np.array(cent_sim))
    dis = np.array(dis)
    return dis


def Update_cen(dataSet, centroids, k, test, estimator: FoilBase):
    distance = Distance(dataSet, centroids, k, test, estimator)
    # print(distance)
    maxIndex = np.argmax(distance, axis=1)
    # print("len(dataset)", len(dataSet))
    # print("len(maxIndex)", len(maxIndex))
    # print("maxIndex: ", maxIndex)
    cluster = []
    for i in range(k):
        cluster.append([])
    for i, j in enumerate(maxIndex):
        cluster[j].append(i)
    # print("cluster: ", cluster)
    # Find centroid for each cluster
    newCentroids = []
    for i in range(k):
        sam_sum_lst = []
        for sample in cluster[i]:
            sam_sum = 0
            for other_sam in cluster[i]:
                sam_sum += similarity_sample(dataSet[sample], dataSet[other_sam], test, estimator)
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
    # print(type(centroids))
    for cen in newCentroids:
        if cen not in centroids:
            changed += 1
    # print(changed)

    return changed, newCentroids


