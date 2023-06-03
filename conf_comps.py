"""Create your own active learning(AL) runs in this file.
- AL runs are defined in the list AL_RUNS.
"""

from al.al_comp import RandomComp, ManualComp, ALComp
from al.al_round import ManualRound, StraRound
from al.al_strategies import Strategies, Strategies_Sim_Only, Strategies_Sim1_Only
AL_RUNS: list[ALComp] = []

###############################################################################
# Create runs of all strategies. Each run starts with 5 random data.          #
# Each run contains 20 rounds which query 5 data points based on its strategy.#
############################################################################### 
# AL_RUNS = [RandomComp(init_size=5,                                          #
#                        rounds=[                                             #
#                            StraRound(query_rounds=range(19),                #
#                                      strategy=stra,                         #
#                                      n_instances=5)                         #
#                        ]) for stra in Strategies.keys()]                    #
###############################################################################

#################################################################################
# Create runs of all strategies. Each run starts with 5 manually selected data. #
# Each run contains 20 rounds which query 5 data points based on its strategy.  #
#################################################################################
# AL_RUNS = [ManualComp(init_imgIds=[                                           #
#     "168.Kentucky_Warbler/Kentucky_Warbler_0010_795912.jpg",                  #
#     "168.Kentucky_Warbler/Kentucky_Warbler_0063_795904.jpg",                  #
#     "171.Myrtle_Warbler/Myrtle_Warbler_0015_166713.jpg",                      #
#     "168.Kentucky_Warbler/Kentucky_Warbler_0033_165271.jpg",                  #
#     "170.Mourning_Warbler/Mourning_Warbler_0077_166567.jpg"                   #
# ],                                                                            #
#     rounds=[                                                                  #
#     StraRound(query_rounds=range(19),                                         #
#               strategy=stra,                                                  #
#               n_instances=5)                                                  #
# ]) for stra in Strategies.keys()]                                             #
#################################################################################

#################################################################################
# Create a single run starting with 5 random data.                              #
# For round 0,2,4,6,8, randomly query 5 data.                                   #
# For round 1,3,5,7,9, query 5 data using strategy 'sim2_lambda06_size50'.      #
#################################################################################
# AL_RUNS = [RandomComp(init_size=5,                                            #
#                        rounds=[                                               #
#                            StraRound(query_rounds=[0,2,4,6,8],                #
#                                      strategy='random',                       #
#                                      n_instances=5),                          #
#                            StraRound(query_rounds=[1,3,5,7,9],                #
#                                      strategy='sim2_lambda06_size50',         #
#                                      n_instances=5),                          #
#                        ])]                                                    #
#################################################################################

#################################################################################
# Create runs with just different seeds.                                        # 
#################################################################################
# AL_RUNS = [ManualComp(init_imgIds=[                                           #
#     "634787e0e69f25e2eb46e254",                                               #
#     "63478a8ae69f25e2eb46e29c",                                               #
#     "6348942ace71d0106eadeb83"],                                              #
#     rounds=[                                                                  #
#         StraRound(query_rounds=range(33),                                     #
#                   strategy="sim2_lambda1_size100", n_instances=3),            #
# ], seed=sd) for sd in range(2000, 3000)]                                      #
#################################################################################

AL_RUNS = [ManualComp(init_imgIds=[
    "22cook",
    "305teacher",
    "100farmer"
],
    seed=267,
    rounds=[
    StraRound(query_rounds=range(32),
              strategy=strat,
              n_instances=3)
]) for strat in list(Strategies.keys())]


if __name__ == '__main__':
    from pprint import pprint
    pprint(AL_RUNS)
