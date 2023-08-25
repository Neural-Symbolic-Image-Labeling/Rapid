from modAL import ActiveLearner
from algo_capsule import strategy_factory
from foil.foil_model import FoilImageClassifier
import numpy as np
# Medical
from foil.model_label.medical_foil_for_vscode import FOIL as med_foil
from foil.model_label.medical_label_for_vscode import label as med_label
# Bird

# Default

defualt_strategy = strategy_factory(sim_mode=1, lambda_mode=6, m=50)

def query(al_type, X_init, y_init, X_pool, n_instances=10, strategy=defualt_strategy, **kwargs):
    """ Query data from X_pool.
    
    @param al_type: str, type of active learning(Default | Medical | Bird).
    @param X_init: list, initial data, aka the already labeled data.
    @param y_init: list, labels of X_init.
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
        strategy = strategy_factory(sim_mode=1, lambda_mode=6, m=50, al_type='Medical')
    elif al_type == 'Bird':
        #TODO
        strategy = strategy_factory(sim_mode=1, lambda_mode=6, m=50, al_type='Bird')
        
    elif al_type == 'Default':
        #TODO
        strategy = strategy_factory(sim_mode=1, lambda_mode=6, m=50)
        
    else:
        raise NotImplementedError
    
    model = FoilImageClassifier(fn_FOIL, fn_label)
    learner = ActiveLearner(
        estimator=model,
        query_strategy = strategy,
        X_training=np.array(X_init), y_training=np.array(y_init),
    )
    
    # Query data
    query_idx, query_items = learner.query(X_pool, n_instances=len(X_pool) if len(X_pool) < n_instances else n_instances, **kwargs)
    query_ids = [x['imageId'] for x in query_items]
    
    return query_ids, query_items

if __name__ == '__main__':
    import random
    import numpy as np
    from data.data_loader import ClassificationDataManager
    data_parser = ClassificationDataManager()
    X_train, X_test, X_val, y_train, y_test, y_val = data_parser.split_data("F:\GitHub_Repos\Rapid\data\datasets\medical\medical.json", "F:\GitHub_Repos\Rapid\data\datasets\medical\config_medical.json", task="medical")
    X_train = np.array(X_train)
    y_train = np.array(y_train)
    init_idx = random.sample(range(len(X_train)), 10)
    X_initial = X_train[init_idx]
    y_inital = y_train[init_idx]
    X_pool = np.delete(X_train, init_idx, axis=0)
    
    print(query('Medical', X_initial, y_inital, X_pool, n_instances=8)[0])
    