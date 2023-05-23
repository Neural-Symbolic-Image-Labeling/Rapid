from modAL.models import ActiveLearner
import json
import sys
import os
import pickle
from tqdm import tqdm

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
from combinationstrategy import *

np.random.seed(18)
# 14

DISABLE_TQDM = False

class ActiveLearningManager:
    def __init__(self, learner: ActiveLearner, X_pool, y_pool, X_test, y_test, X_val, y_val) -> None:
        self.learner = learner
        self.X_pool = X_pool
        self.y_pool = y_pool
        self.X_test = X_test
        self.y_test = y_test
        self.X_val = X_val
        self.y_val = y_val
        from datetime import datetime
        self.image_name = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.png"
        self.display_method = 'show'

    def set_display_method(self, method: str) -> None:
        self.display_method = method

    def set_image_name(self, name: str) -> None:
        self.image_name = name

    def _get_query_hit_rate(self, query_idx, query_items, y) -> float:
        hit = 0.0
        for idx, item in zip(query_idx, query_items):
            pred = self.learner.estimator.predict([item])
            # print("=========== HIT RATE ===========")
            # print(y[idx], pred)
            # print("=========== END HIT RATE ===========")
            if y[idx] in pred[0]:
                hit += 1
        return hit / len(query_idx)

    def lonely_run(self, n_queries: int, n_instances: int, **query_args):
        learner = copy.deepcopy(self.learner)
        X_pool = copy.deepcopy(self.X_pool)
        query_idx, query_item = learner.query(X_pool, n_instances=n_instances, **query_args)
        return query_idx, query_item

    def _al_helper(self, learner: ActiveLearner, n_queries: int, n_instances: int, plot=True, name="N/A", **query_args):
        X_pool = copy.deepcopy(self.X_pool)
        y_pool = copy.deepcopy(self.y_pool)
        X_test = copy.deepcopy(self.X_test)
        y_test = copy.deepcopy(self.y_test)
        X_val = copy.deepcopy(self.X_val)
        y_val = copy.deepcopy(self.y_val)
        # print(f"Running AL on strategy: {name}")
        # print(f"Init AL with {len(X_pool)} samples.")
        # learner.estimator.print_rules()

        query_lst = []
        test_acc_lst = []
        val_acc_lst = []
        hit_rate_lst = []
        img_idx_lst = []
        for i in tqdm(range(n_queries), desc=f"Running AL on strategy: {name}", leave=False, disable=DISABLE_TQDM):
            test_acc = learner.score(X_test, y_test)
            test_acc_lst.append(test_acc)

            val_acc = learner.score(X_val, y_val)
            val_acc_lst.append(val_acc)

            query_idx, query_item = learner.query(X_pool, n_instances=n_instances, **query_args)
            for item in query_item:
                img_idx_lst.append(item['imageId'])
            hit_rate_lst.append(self._get_query_hit_rate(query_idx, query_item, y_pool))
            query_lst.append((query_idx, query_item))
            learner.teach(X_pool[query_idx], y_pool[query_idx])

            # print(f'Rule in round {i}: {learner.estimator._rules}')

            X_pool = np.delete(X_pool, query_idx, axis=0)
            y_pool = np.delete(y_pool, query_idx, axis=0)

        test_acc = learner.score(X_test, y_test)
        test_acc_lst.append(test_acc)

        val_acc = learner.score(X_val, y_val)
        val_acc_lst.append(val_acc)

        return query_lst, test_acc_lst, val_acc_lst, hit_rate_lst, img_idx_lst

    def run_active_learning(self, n_queries: int, n_instances: int, plot=True, **query_args):

        learner = copy.deepcopy(self.learner)
        learner.query_strategy = sim_2_strategy_1_init_2
        _, acc_lst, hit_rate_lst = self._al_helper(learner, n_queries, n_instances, plot, **query_args)

        if plot:
            import matplotlib.pyplot as plt
            with plt.style.context('seaborn-whitegrid'):
                plt.figure(figsize=(10, 10))
                # Accuracy plot
                plt.subplot(2, 1, 1)
                plt.plot(np.arange(n_queries, dtype=int), acc_lst, label='Accuracy')
                plt.xlabel(f"Query(+{n_instances} instance(s) per round)")
                plt.ylabel('Accuracy')
                plt.legend()

                # Hit rate plot
                plt.subplot(2, 1, 2)
                plt.plot(np.arange(n_queries, dtype=int), hit_rate_lst, label='Hit rate')
                plt.xlabel(f"Query(+{n_instances} instance(s) per round)")
                plt.ylabel('Hit rate')
                plt.legend()

                plt.savefig("result.png")

                if self.display_method == 'show':
                    plt.show()
                # elif self.display_method == 'save':
                #     plt.savefig(self.image_name)
        # return _, acc_lst, hit_rate_lst

    def run_against_random(self, n_queries: int, n_instances: int, plot=True, **query_args) -> None:
        # For random
        random_leaner = copy.deepcopy(self.learner)
        random_leaner.query_strategy = random_query_strategy
        _, random_acc_lst, random_hit_rate_lst = self._al_helper(random_leaner, n_queries, n_instances, plot, **query_args)

        # For active learning
        learner = copy.deepcopy(self.learner)
        _, acc_lst, hit_rate_lst = self._al_helper(learner, n_queries, n_instances, plot, **query_args)

        if plot:
            import matplotlib.pyplot as plt
            with plt.style.context('seaborn-whitegrid'):
                # Accuracy plot
                plt.figure(figsize=(10, 10))
                plt.subplot(2, 1, 1)

                plt.plot(np.arange(n_queries, dtype=int), random_acc_lst, label='Random')
                plt.plot(np.arange(n_queries, dtype=int), acc_lst, label='Active Learning')
                plt.xlabel(f"Query(+{n_instances} instance(s) per round)")
                plt.ylabel('Accuracy')
                plt.legend()

                # Hit rate plot
                plt.subplot(2, 1, 2)
                plt.plot(np.arange(n_queries, dtype=int), random_hit_rate_lst, label='Random')
                plt.plot(np.arange(n_queries, dtype=int), hit_rate_lst, label='Active Learning')
                plt.xlabel(f"Query(+{n_instances} instance(s) per round)")
                plt.ylabel('Hit rate')
                plt.legend()

                # Mode 1
                # plt.savefig("result_s1_m1.png")
                # plt.savefig("result_s1_m1_j.png")

                # plt.savefig("result_s2_m1.png")
                # Mode 2
                # plt.savefig("result_s1_m2.png")
                # plt.savefig("result_s2_m2.png")
                # Mode 3
                plt.savefig("result_s1_m3.png")
                # plt.savefig("result_s2_m3.png")
                if self.display_method == 'show': # Windows
                    plt.show()
                # elif self.display_method == 'save': # Other
                # plt.savefig(self.image_name)
    def _run_test_helper(self, name: str, dsname: str, strategy_func, learner: ActiveLearner, n_queries: int, n_instances: int, plot=True, **query_args) -> None:
        curr_result = {'name': name}
        learner_cpy = copy.deepcopy(learner)
        learner_cpy.query_strategy = strategy_func
        _, acc_lst, val_acc_lst, hit_rate_lst, img_idx_lst = self._al_helper(learner_cpy, n_queries, n_instances, plot, name=name, **query_args)
        curr_result['test_acc'] = acc_lst
        curr_result['val_acc'] = val_acc_lst
        curr_result['hit_rate'] = hit_rate_lst
        curr_result['img_idx'] = img_idx_lst

        with open(f'FOIL/resultdata/{dsname}/{name}', 'wb') as f:
            pickle.dump(curr_result, f)

        return curr_result

    def run_test(self, dsname: str, n_queries: int, n_instances: int, plot=True, **query_args) -> None:
        # This test contains similarity 1, 2, 3; lambda 0.2, 0.6, 1.0; intermediate set size 20, 50, 100; entropy, conflict, random
        # This test only contains lambda = 0.6 when comparing the size
        # Returns a json file contains all test result
        result = []
        # strategy_lst = [random_query_strategy, strategy_1_entro, strategy_1_conflict, sim_1_strategy_1_init_2,
        #                 sim_1_strategy_1_init_6, sim_1_strategy_1_init_1, sim_2_strategy_1_init_2, sim_2_strategy_1_init_6, sim_2_strategy_1_init_1,
        #                 sim_3_strategy_1_init_2, sim_3_strategy_1_init_6, sim_3_strategy_1_init_1, stra1_sim_1_6_20, stra1_sim_1_6_50, stra1_sim_1_6_100,
        #                 stra1_sim_2_6_20, stra1_sim_2_6_50, stra1_sim_2_6_100, stra1_sim_3_6_20, stra1_sim_3_6_50, stra1_sim_3_6_100, stra1_sim_1_2_20,
        #                 stra1_sim_1_2_50, stra1_sim_1_2_100, stra1_sim_2_2_20, stra1_sim_2_2_50, stra1_sim_2_2_100, stra1_sim_3_2_20, stra1_sim_3_2_50,
        #                 stra1_sim_3_2_100, stra1_sim_1_1_20, stra1_sim_1_1_50, stra1_sim_1_1_100, stra1_sim_2_1_20, stra1_sim_2_1_50, stra1_sim_2_1_100,
        #                 stra1_sim_3_1_20, stra1_sim_3_1_50, stra1_sim_3_1_100]
        # name_lst = ['random', 'entropy', 'conflict', 'sim1_lambda02', 'sim1_lambda06', 'sim1_lambda1', 'sim2_lambda02', 'sim2_lambda06', 'sim2_lambda1',
        #             'sim3_lambda02', 'sim3_lambda06', 'sim3_lambda1', 'sim1_lambda06_size20', 'sim1_lambda06_size50', 'sim1_lambda06_size100',
        #             'sim2_lambda06_size20', 'sim2_lambda06_size50', 'sim2_lambda06_size100', 'sim3_lambda06_size20', 'sim3_lambda06_size50', 'sim3_lambda06_size100',
        #             'sim1_lambda02_size20', 'sim1_lambda02_size50', 'sim1_lambda02_size100', 'sim2_lambda02_size20', 'sim2_lambda02_size50', 'sim2_lambda02_size100',
        #             'sim3_lambda02_size20', 'sim3_lambda02_size50', 'sim3_lambda02_size100', 'sim1_lambda1_size20', 'sim1_lambda1_size50', 'sim1_lambda1_size100',
        #             'sim2_lambda1_size20', 'sim2_lambda1_size50', 'sim2_lambda1_size100', 'sim3_lambda1_size20', 'sim3_lambda1_size50', 'sim3_lambda1_size100']
        strategy_lst = [random_query_strategy, strategy_1_entro, strategy_1_conflict, stra1_sim_1_6_20, stra1_sim_1_6_50, stra1_sim_1_6_100, stra1_sim_1_2_20,
                        stra1_sim_1_2_50, stra1_sim_1_2_100, stra1_sim_1_1_20, stra1_sim_1_1_50, stra1_sim_1_1_100, lonely_diverse]
        name_lst = ['random', 'entropy', 'conflict', 'sim1_lambda06_size20', 'sim1_lambda06_size50', 'sim1_lambda06_size100',
                    'sim1_lambda02_size20', 'sim1_lambda02_size50', 'sim1_lambda02_size100', 'sim1_lambda1_size20', 'sim1_lambda1_size50', 'sim1_lambda1_size100', 'diversity']

        strategy_lst = [strategy_lst[-1]]
        name_lst = [name_lst[-1]]
        
        assert len(strategy_lst) == len(name_lst)
        
        combined = zip(strategy_lst, name_lst)
        for strategy, name in tqdm(combined, desc='Main Progress', leave=True, total=len(strategy_lst), disable=DISABLE_TQDM):
            curr = self._run_test_helper(name, dsname, strategy, self.learner, n_queries, n_instances, plot, **query_args)
            result.append(curr)
        
        with open(f'FOIL/resultdata/{dsname}/result.json', 'w') as f:
            json.dump(result, f)


    def run_single_criteria(self, dsname: str, n_queries: int, n_instances: int, plot=True, **query_args) -> None:
        # This test contains random, conflict, entropy, diversity, informative, suggested multi-criteria
        result = []
        strategy_lst = [random_query_strategy, lonely_diverse, lonely_info, stra1_sim_1_1_100]
        name_lst = ['random', 'diversity', 'informative', 'sim1_lambda1_size100']

        assert len(strategy_lst) == len(name_lst)
        
        combined = zip(strategy_lst, name_lst)
        for strategy, name in tqdm(combined, desc='Main Progress', leave=True, total=len(strategy_lst), disable=DISABLE_TQDM):
            curr = self._run_test_helper(name, dsname, strategy, self.learner, n_queries, n_instances, plot, **query_args)
            result.append(curr)
        
        with open(f'FOIL/resultdata/{dsname}/compareall.json', 'w') as f:
            json.dump(result, f)


if __name__ == '__main__':
    model = FoilImageClassifier()
    data_parser = ClassificationDataManager()
    # Train file
    X_train, _, y_train = data_parser.get_data_from_file(filename='FOIL/data_file/bird/bird5_strip_train2')
    # Test file
    X_test, _, y_test = data_parser.get_data_from_file(filename='FOIL/data_file/bird/bird5_strip_test2')
    # Validation file
    X_val, _, y_val = data_parser.get_data_from_file(filename='FOIL/data_file/bird/bird5_strip_val2')
    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=60)
    X_train = np.array(X_train)
    y_train = np.array(y_train)
    X_test = np.array(X_test)
    y_test = np.array(y_test)
    X_val = np.array(X_val)
    y_val = np.array(y_val)

    # for idx, v in enumerate(y_train):
    #     print(f"{idx}: {v}")

    # Change the initial index to the index of first round
    initial_idx = np.array([0, 9, 20, 30, 69])
    # initial_idx = np.random.choice(len(X_train), size=5, replace=False)
    X_initial = X_train[initial_idx]
    y_initial = y_train[initial_idx]
    X_pool = np.delete(X_train, initial_idx, axis=0)
    y_pool = np.delete(y_train, initial_idx, axis=0)

    print(len(X_train), len(X_pool), len(X_test))

##########
    learner = ActiveLearner(
        estimator=model,
        # query_strategy=uncertainty_sampling_strategy,
        query_strategy = strategy_1_entro,
        X_training=X_initial, y_training=y_initial
    )

    active_learner = ActiveLearningManager(learner, X_pool, y_pool, X_test, y_test, X_val, y_val)
    active_learner.set_display_method('show' if platform.system() == 'Windows' else 'save')
    # active_learner.run_par_com_sim1(n_queries=20, n_instances=12)
    # active_learner.run_par_com_sim2(n_queries=20, n_instances=12)
    # active_learner.run_par_com_sim3(n_queries=20, n_instances=12)
    # active_learner.run_active_learning(n_queries=12, n_instances=24, plot=True)
    # active_learner.run_size_com(n_queries=20, n_instances=12, plot=True)
    # active_learner.run_measure_com(n_queries=20, n_instances=12, plot=True)
    active_learner.run_test(dsname='bird', n_queries=2, n_instances=5, plot=True)
    # active_learner.run_single_criteria(dsname='bird', n_queries=2, n_instances=5, plot=True)

###########
    # print(similarity_sample(X_train[2], X_train[1]))
    # print(diversity_sampling_strategy_global(None, X, 5))
###########
    # learner = ActiveLearner(
    #     estimator=model,
    #     # query_strategy=uncertainty_sampling_strategy,
    #     query_strategy = strategy_2,
    #     X_training=X_initial, y_training=y_initial
    # )
    #
    # active_learner = ActiveLearningManager(learner, X_pool, y_pool, X_test, y_test)
    # active_learner.set_display_method('show' if platform.system() == 'Windows' else 'save')
    # # # active_learner.set_image_name('result1.png')
    # query_idx, query_item = active_learner.lonely_run(n_queries=1, n_instances=3)
    # print(query_idx)
    # print(query_item)

########
    # print(strategy_1(model, X, 3))
    # learner = ActiveLearner(
    #     estimator=model,
    #     # query_strategy=uncertainty_sampling_strategy,
    #     query_strategy=representativeness_query_strategy,
    #     X_training=X_initial, y_training=y_initial
    # )
    #
    # print("sim1", similarity_sample(X[27], X[27]))
    # print("sim2", similarity_sample(X[27], X[75]))

    # Yifeng Testing
    # Change n_queries to the number of rounds you want to run
    # Change n_instances to the number of instances you want to query each round
    # active_learner.run_active_learning(n_queries=20, n_instances=12, plot=True)
