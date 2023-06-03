from typing import Callable, Union

class ALConfig:
    ## Data
    data_path = 'data/datasets/prof/prof_new.json'  # Path to the dataset
    data_split_config = 'data/datasets/prof/config_prof_new.json'  # Path to the data split config file

    ## Active Learning
    foil_model: str = 'ad_prof_neg_color'    # Choose foil and label functions from
                                # ['ad_prof', 'ad_prof_neg_color', 'ad_prof_neg_nocolor', 'bird', 'medical']
    similarity_func: Union[str, Callable] = 'default' # 'default', 'bird', 'med', or a custom callback function
    enable_editing = False  # Enable manual editing after each round
    ## Results
    output_path = 'outputs/prof/prof_sd267'  # Path to the output directory
    save_only_max = False  # Save only the max accuracy result

    show_hit_rate = True  # Show hit rates for each comp
    show_query_imgs = True  # Show query images for each comp
    show_max_rule = True  # Show max rule for each comp
    show_rules_every_round = False  # Show rules every round
    show_val_acc = True  # Show validation accuracy for each comp

    max_acc_ignore = \
    []# ['random', 'entropy', 'conflict', 'diversity_1', 'diversity_2', 'diversity_3', 'informative_02', 'informative_06', 'informative_1'] 

    save_every = 1  # Save results every n components

    ## Other
    # Extra note for this experiment
    note = '''prof, seed 267, 3+3*32, (June 1, 2023) 
    '''
    # Disable tqdm progress bar (will be auto disabled if manual edtting round exists)
    tqdm_disable = False
    
config = ALConfig()

# disable tqdm if rule editing is enabled
if config.enable_editing:
    config.tqdm_disable = True
    
# add .json suffix if not present
if not config.output_path.endswith('.json'):
    config.output_path += '.json'
