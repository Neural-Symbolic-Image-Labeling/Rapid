from modAL.models import ActiveLearner

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "AL"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", '..'))
import numpy as np

from AL.al_comp import RandomComp, ManualComp, ALComp
from AL.al_round import ManualRound, StraRound
from AL.al_strategies import Strategies, none_query_strategy
from AL.al_foils import get_foil_label_fn

from data import ClassificationDataManager
from FoilModel import FoilImageClassifier

np.random.seed(88)
class Config:
    ## Data
    data_path = 'FOIL/data_file/ad/ad_initial.json'  # Path to the dataset
    data_split_config = 'FOIL/data_file/ad/config_ad_initial.json'  # Path to the data split config file

    ## Active Learning
    al_comp: ALComp = RandomComp(init_size=5,
                       rounds=[
                           StraRound(query_rounds=range(20),
                                     strategy="sim1_lambda2_size100",
                                     n_instances=3)
                       ])
    '''al_comp: ALComp = ManualComp(init_imgIds=[
        "173.Orange_crowned_Warbler/Orange_Crowned_Warbler_0040_168029.jpg",
"172.Nashville_Warbler/Nashville_Warbler_0048_167071.jpg",
"171.Myrtle_Warbler/Myrtle_Warbler_0094_166922.jpg"
    ],
    rounds=[
                           StraRound(query_rounds=range(33),
                                     strategy="sim1_lambda6_size50",
                                     n_instances=3)
                       ])'''
    

    foil_model: str = 'ad_prof_neg_nocolor'    # Choose foil and label functions from
                                # ['ad_prof', 'ad_prof_neg_color', 'ad_prof_neg_nocolor', 'bird1', 'medical']

# def predict(X, rules, LABEL, **kwargs) -> list[list[str]]:
#     # Can show the rules here
#     result, satis_list = LABEL(dict_list=X, rules=rules)
#     # drop '(X)'
#     for l in result:
#         for i in range(len(l)):
#             l[i] = l[i].split('(')[0]
    
#     if 'rt_satis_list' in kwargs and kwargs['rt_satis_list']:
#         return result, satis_list
#     return result

# def score(X, y, rules, LABEL):
#     result = predict(X, rules=rules, LABEL=LABEL)
#     correct = 0
#     total = 0
#     for idx, l in enumerate(result):
#         total += 1
#         if len(l) == 1 and l[0].strip() == y[idx].strip():
#             correct += 1

#     acc = correct / total
#     return acc

if __name__ ==  "__main__":
    config = Config()
    comp = config.al_comp

    data_parser = ClassificationDataManager()
    
    X_train, X_test, _, y_train, y_test, _ = data_parser.split_data(config.data_path, config.data_split_config)
    FOIL, LABEL = get_foil_label_fn(config.foil_model)

    model = FoilImageClassifier(f_FOIL=FOIL, f_LABEL=LABEL)

    X_train = np.array(X_train)
    y_train = np.array(y_train)
    X_test = np.array(X_test)
    y_test = np.array(y_test)

    initial_idx = comp.get_init_idx(X_training=X_train, y_training=y_train)
    # print(f"Initial idx: {initial_idx}")
    X_initial = X_train[initial_idx]
    y_initial = y_train[initial_idx]
    X_pool = np.delete(X_train, initial_idx, axis=0)
    y_pool = np.delete(y_train, initial_idx, axis=0)

    learner = ActiveLearner(
        estimator=model,
        query_strategy = none_query_strategy,
        X_training=X_initial, y_training=y_initial
    )

    # Start AL query process 
    locked = {}
    deleted = {}

    acc = learner.score(X_test, y_test)
    print(f"Before start: Accuracy = {acc}")

    manual = True
    response = input("Do you want to activate manual mode? (y/n): ")
    if response.upper().startswith("N"):
        manual = False

    finished = False
    round_idx = 0
    curr_round = None
    while not finished:
        # 1. find curr round type
        finished = True
        for round in comp.rounds:
            if round_idx in round:
                curr_round = round
                finished = False
                round_idx += 1
                break
        if finished:
            print("No more round, AL finished.")
            break

        print(f"train: {len(X_train)}, pool: {len(X_pool)}, test:{len(X_test)}")
        # 2. query items and update learner
        query_idx, query_ids, query_items = curr_round.query(learner, X_pool)
        # print(f"Query idx: {query_idx}")
        learner.teach(X_pool[query_idx], y_pool[query_idx], d=deleted, l=locked)
        X_pool = np.delete(X_pool, query_idx, axis=0)
        y_pool = np.delete(y_pool, query_idx, axis=0)

        # show test accuracy
        acc = learner.score(X_test, y_test)
        print(f"\n\nRound {round_idx}: Accuracy = {acc}")
        print("Current rules: ", learner.estimator.get_rules())
        print("Current locked: ", locked)
        print("Current deleted: ", deleted)

        if manual:
            # Start manual testing process
            import json
            input_text = input("\n*Enter rule string:")
            while input_text != "continue" and input_text != "c":
                try:
                    input_text = input_text.replace("\'", "\"")
                    new_rule = json.loads(input_text)
                    learner.estimator.set_rules(new_rule)
                    print("Get Rule: \n", new_rule)
                    print("New Accuracy: ", learner.score(X_test, y_test))
                except Exception as e:
                    print(e)

                input_text = input("\n*Enter \"c\" to continue, or enter new rule string:")

            input_text = "n"
            while input_text.upper().startswith("N"):
                try:
                    curr_l = input("*Enter locked: ")
                    if not (curr_l == "c" or curr_l == "continue"):
                        curr_l = curr_l.replace("\'", "\"")
                        locked = json.loads(curr_l)
                        print("Get Locked: \n", locked)

                    curr_d = input("*Enter deleted: ")
                    if not (curr_d == "c" or curr_d == "continue"):
                        curr_d = curr_d.replace("\'", "\"")
                        deleted = json.loads(curr_d)
                        print("Get Deleted: \n", deleted)
                except Exception as e:
                    print(e)

                input_text = input("Do you want to move to the next query? (y/n): ")
            
    
    print("Maximum accuracy: ", learner.estimator.get_max_acc())
    print("Maximum rules: ", learner.estimator.get_max_rules())


            