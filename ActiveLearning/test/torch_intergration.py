import torch
import numpy as np

import matplotlib.pyplot as plt

from sklearn.metrics import accuracy_score

from torch import nn
from torch.utils.data import DataLoader
from torchvision.transforms import ToTensor
from torchvision.datasets import MNIST
from skorch import NeuralNetClassifier

from modAL.models import ActiveLearner
from modAL.uncertainty import entropy_sampling

np.random.seed(0)
torch.manual_seed(0)


# build class for the skorch API
class Torch_Model(nn.Module):
    def __init__(self,):
        super(Torch_Model, self).__init__()
        self.conv1 = nn.Sequential(
            nn.Conv2d(
                in_channels=1,
                out_channels=12,
                kernel_size=3,
                stride=1,
                padding=1,
            ),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2),
        )
        self.conv2 = nn.Sequential(
            nn.Conv2d(12, 24, 3, 1, 1),     
            nn.ReLU(),                      
            nn.MaxPool2d(2),
        )
        self.fcs = nn.Sequential(
            nn.Linear(24 * 7 * 7, 64),
            nn.ReLU(),
            nn.Dropout(p=0.2),
            nn.Linear(64, 10),
        )

    def forward(self, x):
        out = x
        out = self.conv1(out)
        out = self.conv2(out)
        out = out.view(x.size(0), -1)
        out = self.fcs(out)
        return out


# create the classifier
device = "cuda" if torch.cuda.is_available() else "cpu"
classifier1 = NeuralNetClassifier(Torch_Model,
                                  max_epochs=250,
                                  criterion=nn.CrossEntropyLoss,
                                  optimizer=torch.optim.Adam,
                                #   optimizer__lr=0.001,
                                  train_split=None,
                                  warm_start=False,
                                  verbose=False,
                                  device=device)

classifier2 = NeuralNetClassifier(Torch_Model,
                                  max_epochs=250,
                                  criterion=nn.CrossEntropyLoss,
                                  optimizer=torch.optim.Adam,
                                  train_split=None,
                                  warm_start=False,
                                  verbose=False,
                                  device=device)

"""
Data wrangling
1. Reading data from torchvision
2. Assembling initial training data for ActiveLearner
3. Generating the pool
"""

mnist_data = MNIST('.', download=False, transform=ToTensor())
dataloader = DataLoader(mnist_data, shuffle=False, batch_size=60000)
X, y = next(iter(dataloader))
X = X.detach().cpu().numpy()
y = y.detach().cpu().numpy()

# read training data
X_train, X_test, y_train, y_test = X[:50000], X[50000:], y[:50000], y[50000:]
X_train = X_train.reshape(50000, 1, 28, 28)
X_test = X_test.reshape(10000, 1, 28, 28)

# assemble initial data
n_initial = 10
initial_idx = np.random.choice(
    range(len(X_train)), size=n_initial, replace=False)
X_initial = X_train[initial_idx]
y_initial = y_train[initial_idx]

# generate the pool
# remove the initial data from the training dataset
X_pool = np.delete(X_train, initial_idx, axis=0)
y_pool = np.delete(y_train, initial_idx, axis=0)

# idx_list = np.random.choice(range(X_train.shape[0]), size=100, replace=False)
# print("=============================================")
# for idx in range(1):
#     print("Iteration: ", idx)
#     classifier1.fit(X_train[idx_list], y_train[idx_list])
#     # print(X_train[idx_list].shape, y_train[idx_list].shape)
#     # print(y_test[[0,1,2,3,4,5]])
#     # print(classifier1.predict(X_test[[0,1,2,3,4,5]]))
#     print("Accuracy: ", accuracy_score(y_test[[0,1,2,3,4,5]], classifier1.predict(X_test[[0,1,2,3,4,5]])))
# exit()

"""
Training the ActiveLearner
"""
def random_query_strategy(classifier, X, n_instances=1):
    query_idx = np.random.choice(range(len(X)), size=n_instances, replace=False)
    return query_idx, X[query_idx]

# initialize ActiveLearner
learner1 = ActiveLearner(
    estimator=classifier1,
    query_strategy=entropy_sampling,
    X_training=X_initial, y_training=y_initial,
)


learner2 = ActiveLearner(
    estimator=classifier2,
    query_strategy=random_query_strategy,
    X_training=X_initial, y_training=y_initial,
)

# the active learning loop
AL_scores = []
R_scores = []
n_queries = 150
print(f"Training size: {len(learner1.X_training)}")
for idx in range(n_queries):
    curr_accuracy = learner1.score(X_test, y_test)
    # print(f"Acc: {curr_accuracy}, CurrTraining size: {len(learner1.X_training)}")
    AL_scores.append(curr_accuracy)
    query_idx, query_instance = learner1.query(X_pool, n_instances=1)
    learner1.teach(X_pool[query_idx], y_pool[query_idx], only_new=False)
    # remove queried instance from pool
    X_pool = np.delete(X_pool, query_idx, axis=0)
    y_pool = np.delete(y_pool, query_idx, axis=0)

plt.figure()
plt.plot(np.arange(n_queries), AL_scores)
plt.title('Entropy-based Active Learning')
plt.legend(['entropy-based'])
plt.ylabel('accuracy')
plt.xlabel('query iteration')

X_pool = np.delete(X_train, initial_idx, axis=0)
y_pool = np.delete(y_train, initial_idx, axis=0)
for idx in range(n_queries):
    curr_accuracy = learner2.score(X_test, y_test)
    R_scores.append(curr_accuracy)
    query_idx, query_instance = learner2.query(X_pool, n_instances=1)
    learner2.teach(X_pool[query_idx], y_pool[query_idx], only_new=False)
    # remove queried instance from pool
    X_pool = np.delete(X_pool, query_idx, axis=0)
    y_pool = np.delete(y_pool, query_idx, axis=0)

plt.plot(np.arange(n_queries), R_scores)
plt.legend(['ramdom-based'])

plt.show()
