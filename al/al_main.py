from .al_strategies import none_query_strategy
from .al_round import ALRound
from config import ALConfig
from conf_comps import AL_RUNS
from .al_types import Round, Comp
from .al_foils import get_foil_label_fn

from modAL.models import ActiveLearner
import sys
import os
import numpy as np
import json
from tqdm import tqdm
from datetime import datetime
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

from foil.foil_model import FoilImageClassifier
from data.data_loader import ClassificationDataManager

def get_query_hit_rate(learner, query_idx, query_X, y_pool) -> float:
    hit = 0.0
    for idx, item in zip(query_idx, query_X):
        pred = learner.estimator.predict([item])
        if y_pool[idx] in pred[0]:
            hit += 1
    return hit / len(query_idx)

def al_main(config: ALConfig):
    final_report = {
        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'note': config.note,
        'dataset': config.data_path,
        'data_config': config.data_split_config,
        'foil_model': config.foil_model,
        'num_comps': len(AL_RUNS),
        'max_only': config.save_only_max,
        'max_comp_info': {
            'name': '',
            'max_acc': 0.0,
            'seed': 0,
        },
        'comps': [],
    }
    for comp_idx, comp in tqdm(enumerate(AL_RUNS), desc="Process", total=len(AL_RUNS), disable=config.tqdm_disable):
        seed = comp.get_seed()
        np.random.seed(seed)
        ## Get data and set init data 
        # #####TODO: change data extraction implementation
        # X_train = []
        # y_train = []
        # X_test = []
        # y_test = []
        # X_val = []
        # y_val = []
        data_parser = ClassificationDataManager()
        X_train, X_test, X_val, y_train, y_test, y_val = data_parser.split_data(final_report['dataset'], final_report['data_config'], task="bird")
        # X_train, _, y_train = data_parser.get_data_from_file(filename='FOIL/data_file/ad/ad_initial_train')
        # X_test, _, y_test = data_parser.get_data_from_file(filename='FOIL/data_file/ad/ad_initial_test')
        # X_val, _, y_val = data_parser.get_data_from_file(filename='FOIL/data_file/ad/ad_initial_val')

        X_train = np.array(X_train)
        y_train = np.array(y_train)
        X_test = np.array(X_test)
        y_test = np.array(y_test)
        X_val = np.array(X_val)
        y_val = np.array(y_val)

        initial_idx = comp.get_init_idx(X_training=X_train, y_training=y_train)
        X_initial = X_train[initial_idx]
        y_initial = y_train[initial_idx]
        X_pool = np.delete(X_train, initial_idx, axis=0)
        y_pool = np.delete(y_train, initial_idx, axis=0)
        
        ## Build AL learner
        FOIL, LAEBL = get_foil_label_fn(config.foil_model)
        model = FoilImageClassifier(f_FOIL=FOIL, f_LABEL=LAEBL)
        learner = ActiveLearner(
            estimator=model,
            query_strategy = none_query_strategy,
            X_training=X_initial, y_training=y_initial
        )

        round_idx = 0
        finished = False
        curr_round: ALRound = None
        comp_report = {
            'name': comp.get_comp_desc(),
            'seed': comp.get_seed(),
            'max_acc': 0.0,
            'test_acc': [],
            'init_imgs': [x['imageId'] for x in X_train[initial_idx]],
        }
        if config.show_hit_rate:
            comp_report['hit_rates'] = []
        if config.show_query_imgs:
            comp_report['query_imgs'] = []
        if config.show_max_rule:
            comp_report['max_rule'] = []
        if config.show_rules_every_round:
            comp_report['rules'] = []
        if config.show_val_acc:
            comp_report['val_acc'] = []
        # For editing mode
        locked = {}
        deleted = {}
        if config.enable_editing:
            comp_report['edits'] = []
            
        ## Run rounds
        with tqdm(total=None, desc="Running comp", leave=False, disable=config.tqdm_disable) as pbar:
            while not finished:
                # 1. find curr round type and set seed
                finished = True
                for round in comp.rounds:
                    if round_idx in round:
                        curr_round = round
                        finished = False
                        round_idx += 1
                        pbar.set_description(f"Round {round_idx}({curr_round.get_rounds_desc()})")
                        break
                if finished:
                    # print("No more round")
                    break
                # 2. record acc and max rule info
                test_acc = learner.score(X_test, y_test)
                comp_report['test_acc'].append(test_acc)
                if config.show_rules_every_round:
                    comp_report['rules'].append(learner.estimator.get_rules())
                if test_acc > comp_report['max_acc']:
                    comp_report['max_acc'] = test_acc
                    comp_report['seed'] = seed
                    if config.show_max_rule:
                        comp_report['max_rule'] = learner.estimator.get_rules()
                
                if config.show_val_acc:
                    comp_report['val_acc'].append(learner.score(X_val, y_val))

                # 3. query items
                query_idx, query_ids, query_items = curr_round.query(learner, X_pool)
                # print(f"Query {query_idx}")
                # 4. record other query info
                if config.show_hit_rate:
                    comp_report['hit_rates'].append(get_query_hit_rate(learner, query_idx, query_items, y_pool))
                if config.show_query_imgs:
                    # if len(set(comp_report['query_imgs']).intersection(set(query_ids))) > 0:
                    #     raise Exception("Duplicate query image")
                    comp_report['query_imgs'].extend(query_ids)

                # 5. update learner and pool
                learner.teach(X_pool[query_idx], y_pool[query_idx], d=deleted, l=locked)
                X_pool = np.delete(X_pool, query_idx, axis=0)
                y_pool = np.delete(y_pool, query_idx, axis=0)

                # 6. update progress bar
                pbar.update()
            
            ## Record last round acc and max rule info
            test_acc = learner.score(X_test, y_test)
            comp_report['test_acc'].append(test_acc)
            if config.show_rules_every_round:
                comp_report['rules'].append(learner.estimator.get_rules())
            if test_acc > comp_report['max_acc']:
                comp_report['max_acc'] = test_acc
                comp_report['seed'] = seed
                if config.show_max_rule:
                    comp_report['max_rule'] = learner.estimator.get_rules()
            if config.show_val_acc:
                comp_report['val_acc'].append(learner.score(X_val, y_val))
                
            ## Report round info if editing mode is enabled
            if config.enable_editing:
                print(f"\n\nRound {round_idx}: Accuracy = {test_acc}")
                print("Current rules: ", learner.estimator.get_rules())
                print("Current locked: ", locked)
                print("Current deleted: ", deleted)
            
            ## Start editing section
            if config.enable_editing:
                editing_report = {}
                input_text = input("\n*Enter rule string:")
                new_acc = None
                while input_text != "continue" and input_text != "c":
                    try:
                        input_text = input_text.replace("\'", "\"")
                        new_rule = json.loads(input_text)
                        learner.estimator.set_rules(new_rule)
                        new_acc = learner.score(X_test, y_test)
                        print("Get Rule: \n", new_rule)
                        print("New Accuracy: ", new_acc)
                    except Exception as e:
                        print(e)

                    input_text = input("\n*Enter \"c\" to continue, or enter new rule string:")

                editing_report['acc_change'] = f"({test_acc} -> {new_acc})"
                editing_report['input_rule'] = input_text
                
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
                
                editing_report['locked'] = str(locked)
                editing_report['deleted'] = str(deleted)

            ## Update final report
            new_max = False
            if not (curr_round.type is Round.AL and curr_round.strategy in config.max_acc_ignore):
                if comp_report['max_acc'] > final_report['max_comp_info']['max_acc']:
                    final_report['max_comp_info']['max_acc'] = comp_report['max_acc']
                    final_report['max_comp_info']['name'] = comp_report['name']
                    final_report['max_comp_info']['seed'] = comp_report['seed']
                    new_max = True

            if config.save_only_max and new_max:
                if len(final_report['comps']) == 0:
                    final_report['comps'].append(comp_report)
                else:
                    final_report['comps'][0] = comp_report
            elif not config.save_only_max:
                final_report['comps'].append(comp_report)

            ## Save progress
            if comp_idx % config.save_every == 0:
                with open(config.output_path, mode='w', encoding='utf-8') as f:
                    json.dump(final_report, f, ensure_ascii=False)
    ## Save final report
    with open(config.output_path, mode='w', encoding='utf-8') as f:
        json.dump(final_report, f, ensure_ascii=False)

                



        


    