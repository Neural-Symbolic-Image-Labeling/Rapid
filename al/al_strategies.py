import sys
import os
from collections import OrderedDict
sys.path.insert(0, '/home/ubuntu/ActiveLearning')
sys.path.insert(0, os.path.join(os.path.dirname(
    os.path.abspath(__file__)), "..", ".."))

from al.combinationstrategy import *

def none_query_strategy(classifier, X_pool):
    return [], []


_strategy_lst = [random_query_strategy]
_strategy_lst.extend([informative_factory(lambda_mode)for lambda_mode in [0, 10]])
_strategy_lst.extend([diversity_factory(sim_mode)for sim_mode in [1, 2, 3]])
_strategy_lst.extend([informative_factory(lambda_mode)for lambda_mode in [2, 6, 1]])

_strategy_lst.extend([strategy_factory(sim_mode, lambda_mode, m)
   for sim_mode in [1, 2, 3]
   for lambda_mode in [2, 6, 1]
   for m in [20, 50, 100]])


_name_template = r"sim{0}_lambda{1}_size{2}"
_name_lst = ['random', 'entropy', 'conflict']
_name_lst.extend(['diversity_1', 'diversity_2', 'diversity_3', 'informative_02', 'informative_06', 'informative_1'])
_name_lst.extend([_name_template.format(sim_mode, lambda_mode, m)
   for sim_mode in [1, 2, 3]
   for lambda_mode in [2, 6, 1]
   for m in [20, 50, 100]])

Strategies = OrderedDict(zip(_name_lst, _strategy_lst))
Strategies_Sim_Only = OrderedDict(zip(_name_lst[10:], _strategy_lst[10:]))
Strategies_Sim1_Only = OrderedDict(zip(_name_lst[:18], _strategy_lst[:18]))

if __name__ == '__main__':
    # print(_name_lst[:18])
    print(len(Strategies))
    # print(_strategy_lst)
