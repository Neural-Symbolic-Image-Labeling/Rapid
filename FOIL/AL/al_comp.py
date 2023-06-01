from al_types import Comp
from al_round import ALRound

import numpy as np

class ALComp:
    """A Component defines an active learning process.
    Specifically, it defines:
        - Inital data.
        - A list of rounds performed in the active learning process.
    """
    type: Comp
    rounds: list[ALRound] = []
    seed: int = 0

    def append_round(self, round: ALRound):
        self.rounds.append(round)

    def set_rounds(self, rounds: list[ALRound]):
        self.rounds = rounds

    def set_seed(self, seed: int):
        self.seed = seed

    def get_seed(self):
        return self.seed
    
    def get_comp_desc(self):
        return "+".join(list(dict.fromkeys([r.get_rounds_desc() for r in self.rounds])))

    def get_init_idx(self, X_training, y_training=None):
        """Get initial data."""
        raise NotImplementedError(f"{self} has not implemented 'get_init_data'.")

class RandomComp(ALComp):
    """Component with random selected initial data."""
    init_size: int
    def __init__(self, init_size: int, rounds: list[ALRound]=[], seed=0):
        super().__init__()
        self.type = Comp.RANDOM
        self.init_size = init_size
        self.rounds = rounds
        self.seed = seed

    def set_init_size(self, init_size: int):
        self.init_size = init_size

    def get_init_idx(self, X_training, y_training):
        #TODO: add init foil error handling
        valid = False
        idx_lst = []
        while not valid:
            idx_lst = np.random.choice(len(y_training), size=self.init_size, replace=False)
            if len(set(y_training[idx_lst])) >= 2:
                valid = True
        return idx_lst

class ManualComp(ALComp):
    """Component with manually selected initial data."""
    init_imgIds: list[str] = []
    def __init__(self, init_imgIds: list[str]=[], rounds: list[ALRound]=[], seed=0):
        super().__init__()
        self.type = Comp.MANUAL
        self.init_imgIds = init_imgIds
        self.rounds = rounds
        self.seed = seed
    
    def set_init_imgIds(self, init_imgIds: list[str]):
        self.init_imgIds = init_imgIds

    def get_init_idx(self, X_training, y_training=None):
        init_idx = []
        for idx, x in enumerate(X_training):
            if x['imageId'] in self.init_imgIds:
                init_idx.append(idx)
        if len(init_idx) != len(self.init_imgIds):
            raise Exception(f"Cannot find all imageIds in training_data.")
        return np.array(init_idx)

