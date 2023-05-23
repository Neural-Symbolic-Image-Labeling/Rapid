import numpy as np
import matplotlib.pyplot as plt

from modAL.models import ActiveLearner
from modAL.uncertainty import *

from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC

n_samples = 500
X = np.random.normal(size=(n_samples, 10))
y = np.array([np.random.choice([1,2,3,4]) for _ in X])
X_train = X[:n_samples//2]
y_train = y[:n_samples//2]
X_test = X[n_samples//2:]
y_test = y[n_samples//2:]
# y = np.array([[int(x1 > 0), int(x2 > 0)] for x1, x2 in X])
# preview the data
print("x: ", X[:3, :])
print("y: ", y[:3])

n_initial = 10 # 设定开始时已标记的数量
initial_idx = np.random.choice(range(len(y_train)), size=n_initial, replace=False)
print("initial_idx: ", initial_idx)
X_initial, y_initial = X_train[initial_idx], y_train[initial_idx]
# 剩余unlabeled数据池
X_pool, y_pool = np.delete(X_train, initial_idx, axis=0), np.delete(y_train, initial_idx, axis=0)

# 创建 ActiveLearner
leaner = ActiveLearner(
    estimator=LogisticRegression(penalty='l2', C=1.0, solver='lbfgs', multi_class='multinomial'),
    query_strategy=entropy_sampling,
    X_training=X_initial, 
    y_training=y_initial
)

query_round = 5
for round in range(query_round):
    query_idx, query_item = leaner.query(X_pool, n_instances=10)
    leaner.teach(X_pool[query_idx], y_pool[query_idx])
    X_pool = np.delete(X_pool, query_idx, axis=0)
    y_pool = np.delete(y_pool, query_idx, axis=0)
    print(f"=============Round {round}==================")
    print("query_idx: ", query_idx)
    # print("query_item: ", query_item)
    print("leaner.score: ", leaner.score(X_test, y_test))
