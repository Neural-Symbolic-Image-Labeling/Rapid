from modAL import ActiveLearner
from al.combinationstrategy import strategy_factory
from foil.foil_model import FoilImageClassifier
# Medical
from foil.model_label.medical_foil_for_vscode import FOIL as med_foil
from foil.model_label.medical_label_for_vscode import label as med_label
# Bird

# Default

defualt_strategy = strategy_factory(sim_mode=1, lambda_mode=6, m=50)


def query(al_type, X_init, X_pool, n_instances=10, strategy=defualt_strategy, **kwargs):
    """ Query data from X_pool.
    
    @param al_type: str, type of active learning(Default | Medical | Bird).
    @param X_init: list, initial data, aka the already labeled data.
    @param X_pool: list, unlabeled data.
    @param n_instances: int, number of instances to query.
    @param strategy: str, query strategy function.
    @param kwargs: dict, other parameters that will be directly passed into the query strategy functions.
    
    return: 
        query_ids: list, querried image UUIDs, 
        query_items: list, querried image data
    """
    # Build ActiveLearner
    fn_FOIL = None
    fn_label = None
    if al_type == 'Medical':
        fn_FOIL = med_foil
        fn_label = med_label
    elif al_type == 'Bird':
        #TODO
        pass
    elif al_type == 'Default':
        #TODO
        pass
    else:
        raise NotImplementedError
    
    model = FoilImageClassifier(fn_FOIL, fn_label)
    learner = ActiveLearner(
        estimator=model,
        query_strategy = strategy,
        X_training=X_init, y_training=[],
    )
    
    # Query data
    query_idx, query_items = learner.query(X_pool, n_instances=len(X_pool) if len(X_pool) < n_instances else n_instances, **kwargs)
    query_ids = [x['imageId'] for x in query_items]
    
    return query_ids, query_items