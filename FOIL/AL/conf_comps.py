from al_comp import RandomComp, ManualComp, ALComp
from al_round import ManualRound, StraRound
from al_strategies import Strategies, Strategies_Sim_Only, Strategies_Sim1_Only
AL_COMPS: list[ALComp] = []

# Define active learning components below

# AL_COMPS = [RandomComp(init_size=5,
#                        rounds=[
#                            StraRound(query_rounds=range(19),
#                                      strategy=stra,
#                                      n_instances=5)
#                        ]) for stra in Strategies.keys()]

# AL_COMPS = [ManualComp(init_imgIds=[
#     "168.Kentucky_Warbler/Kentucky_Warbler_0010_795912.jpg",
#     "168.Kentucky_Warbler/Kentucky_Warbler_0063_795904.jpg",
#     "171.Myrtle_Warbler/Myrtle_Warbler_0015_166713.jpg",
#     "168.Kentucky_Warbler/Kentucky_Warbler_0033_165271.jpg",
#     "170.Mourning_Warbler/Mourning_Warbler_0077_166567.jpg"
# ],
#     rounds=[
#     StraRound(query_rounds=range(19),
#               strategy=stra,
#               n_instances=5)
# ]) for stra in Strategies.keys()]

# AL_COMPS = [RandomComp(init_size=5,
#                        rounds=[
#                            StraRound(query_rounds=[0,2,4,6,8],
#                                      strategy='random',
#                                      n_instances=5),
#                            StraRound(query_rounds=[1,3,5,7,9],
#                                      strategy='sim2_lambda06_size50',
#                                      n_instances=5),
#                        ])]

# AL_COMPS = [ManualComp(init_imgIds=[
#     "634787e0e69f25e2eb46e254",
#     "63478a8ae69f25e2eb46e29c",
#     "6348942ace71d0106eadeb83"],
#     rounds=[
#         StraRound(query_rounds=range(33),
#                   strategy="sim2_lambda1_size100", n_instances=3),
# ], seed=sd) for sd in range(2000, 3000)]

AL_COMPS = [ManualComp(init_imgIds=[
    "634787e0e69f25e2eb46e254",
    "63478a8ae69f25e2eb46e29c",
    "6348942ace71d0106eadeb83"],
    rounds=[
        StraRound(query_rounds=range(29),
                  strategy="random", n_instances=3),
], seed=sd) for sd in range(1000,1051)]


if __name__ == '__main__':
    from pprint import pprint
    pprint(AL_COMPS)
