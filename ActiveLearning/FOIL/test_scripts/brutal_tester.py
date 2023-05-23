from modAL.models import ActiveLearner

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", '..'))
import numpy as np
import json
import heapq

from sklearn.model_selection import train_test_split
from tqdm import tqdm

from FoilModel import FoilImageClassifier
from data import ClassificationDataManager
from FOIL.strategies.informativeness import *
from FOIL.strategies.utils import *
from FOIL.strategies.representativeness import *
from combinationstrategy import *

from AL.al_foils import get_foil_label_fn

DISABLE_TQDM = False
class Config:
    def __init__(self):
        self.data_path = "FOIL/data_file/ad/ad_initial.json"
        self.split_config_path = "FOIL/data_file/ad/config_ad_initial.json"
        self.foil_model: str = 'ad_prof_neg_nocolor'    # Choose foil and label functions from
                                # ['ad_prof', 'ad_prof_neg_color', 'ad_prof_neg_nocolor', 'bird', 'medical']
        self.n_init = 5
        self.n_query_total = 95
        self.testround = 50000
        self.save_every = 5
        self.track_num_high = 10
        self.track_num_low = 10
        self.bar_hits_high = 0.6
        self.bar_hits_low = 0.2
        self.output_file = f"ad_initial_{self.testround}rounds.json"

def tracker_builder(acc, initial_imageIds, query_imageIds, max_rules):
    trakcer = {
        "acc": acc, # highest accuracy value
        "initial_imageIds": initial_imageIds,
        "query_imageIds": query_imageIds,
        "max_rules": max_rules,
    }
    return trakcer

def run_test(config: Config):
    FOIL, LAEBL = get_foil_label_fn(config.foil_model)
    model = FoilImageClassifier(f_FOIL=FOIL, f_LABEL=LAEBL)
    data_parser = ClassificationDataManager()
    X_train, X_test, _, y_train, y_test, _ = data_parser.split_data(data_file=config.data_path, config_file=config.split_config_path)
    X_train = np.array(X_train)
    y_train = np.array(y_train)
    X_test = np.array(X_test)
    y_test = np.array(y_test)

    initial_idx = np.random.choice(len(X_train), size=config.n_init, replace=False)
    # print(f"Seleted initial idx: {initial_idx}")
    X_initial = X_train[initial_idx]
    y_initial = y_train[initial_idx]
    X_pool = np.delete(X_train, initial_idx, axis=0)
    y_pool = np.delete(y_train, initial_idx, axis=0)
    initial_imageIds = [X_train[i]['imageId'] for i in initial_idx]

    learner = ActiveLearner(
        estimator=model,
        query_strategy = random_query_strategy,
        X_training=X_initial, y_training=y_initial
    )
    # print("Start training")
    acc_lst, img_lst, rules = _al_helper(learner, config, X_pool, y_pool, X_test, y_test)
    # print("End training")
    return max(acc_lst), initial_imageIds, img_lst, rules

def _al_helper(learner: ActiveLearner, config: Config, X_pool, y_pool, X_test, y_test):
        test_acc_lst = []
        img_idx_lst = []
        query_idx, query_item = learner.query(X_pool, n_instances=config.n_query_total)
        for item in query_item:
            img_idx_lst.append(item['imageId'])
        learner.teach(X_pool[query_idx], y_pool[query_idx])

        X_pool = np.delete(X_pool, query_idx, axis=0)
        y_pool = np.delete(y_pool, query_idx, axis=0)

        test_acc = learner.score(X_test, y_test)
        test_acc_lst.append(test_acc)

        return test_acc_lst, img_idx_lst, learner.estimator.get_rules()


if __name__ == '__main__':
    config = Config()
    error_rounds = 0
    bar_hits_high = 0
    bar_hits_low = 0
    max_acc = -1
    min_acc = 2
    rounds_finished = 0
    high_trackers = []
    low_trackers = []

    if os.path.exists(config.output_file):
        with open(config.output_file, "r") as f:
            data = json.load(f)
            rounds_finished = data['rounds_finished']
            error_rounds = data['error_rounds']
            bar_hits_high = data['bar_hits_high']
            bar_hits_low = data['bar_hits_low']
            max_acc = data['max_acc']
            min_acc = data['min_acc']
            high_trackers = data['max_rounds']
            low_trackers = data['min_rounds']

    def compare_acc(tracker):
        return tracker['acc']

    for i in tqdm(range(rounds_finished, config.testround), desc=f"Progress:", disable=DISABLE_TQDM):
        try:    
            curr_acc, curr_initial_imageIds, curr_query_imageIds, curr_max_rules = run_test(config)
            curr_tracker = tracker_builder(curr_acc, curr_initial_imageIds, curr_query_imageIds, curr_max_rules)
        except Exception as e: # inital error caused by foil
            # print(f"Error occured, {e}")
            error_rounds += 1
            if i % config.save_every == 0:
                with open(config.output_file, "w") as f:
                    json.dump({
                        "rounds_finished": i+1,
                        "error_rounds": error_rounds,
                        "bar_hits_high": bar_hits_high,
                        "bar_hits_low": bar_hits_low,
                        "max_acc": max_acc,
                        "min_acc": min_acc,
                        f"max_rounds": high_trackers,
                        f"min_rounds": low_trackers,
                    }, f)
            continue
        bar_hits_high += 1 if compare_acc(curr_tracker) >= config.bar_hits_high else 0
        bar_hits_low += 1 if compare_acc(curr_tracker) <= config.bar_hits_low else 0

        if compare_acc(curr_tracker) > max_acc:
            max_acc = compare_acc(curr_tracker)
        if compare_acc(curr_tracker) < min_acc:
            min_acc = compare_acc(curr_tracker)

        high_trackers.append(curr_tracker)
        high_trackers = sorted(high_trackers, key=compare_acc, reverse=True)[:config.track_num_high]

        low_trackers.append(curr_tracker)
        low_trackers = sorted(low_trackers, key=compare_acc, reverse=False)[:config.track_num_low]

        if i % config.save_every == 0:
            # print(f"Saved")
            with open(config.output_file, "w") as f:
                json.dump({
                    "rounds_finished": i+1,
                    "error_rounds": error_rounds,
                    "bar_hits_high": bar_hits_high,
                    "bar_hits_low": bar_hits_low,
                    "max_acc": max_acc,
                    "min_acc": min_acc,
                    f"max_rounds": high_trackers,
                    f"min_rounds": low_trackers,
                }, f)
            