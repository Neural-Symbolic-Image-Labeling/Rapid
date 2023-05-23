from al_types import Round
from al_strategies import Strategies

from modAL.models import ActiveLearner

class ALRound():
    type: Round

    def query(self, learner, X_pool, **kwargs):
        """Query data from X_pool.
        reutrn: query_idx, query_ids, query_instance
        """
        raise NotImplementedError(f"{self} has not implemented 'query'.")
    
    def get_rounds_desc(self) -> str:
        raise NotImplementedError(f"{self} has not implemented 'get_rounds_desc'.")
    
class ManualRound(ALRound):
    def __init__(self, query_round_idx: int, imageIds: list[str]):
        super().__init__()
        self.type = Round.MANUAL
        self.query_round_idx = query_round_idx
        self.imageIds = imageIds

    def __contains__(self, query_round: int):
        return query_round == self.query_round_idx
    
    def get_rounds_desc(self):
        return "manual"
    
    def query(self, learner, X_pool, **kwargs):
        query_idx = []
        query_items = []
        for idx, x in enumerate(X_pool):
            if x['imageId'] in self.imageIds:
                query_items.append(x)
                query_idx.append(idx)
        if len(query_items) != len(self.imageIds):
            raise Exception(f"Cannot find all imageIds in X_pool.")
        return query_idx, self.imageIds, query_items
    
class StraRound(ALRound):
    def __init__(self, query_rounds: list[int], strategy: str, n_instances: int):
        super().__init__()
        self.type = Round.AL
        self.query_rounds = query_rounds
        self.strategy = strategy
        self.n_instances = n_instances

    def __contains__(self, query_round: int):
        return query_round in self.query_rounds
    
    def get_rounds_desc(self):
        return self.strategy
    
    def query(self, learner: ActiveLearner, X_pool, **kwargs):
        learner.query_strategy = Strategies[self.strategy]
        query_idx, query_items = learner.query(X_pool, n_instances=self.n_instances)
        query_ids = [x['imageId'] for x in query_items]

        return query_idx, query_ids, query_items