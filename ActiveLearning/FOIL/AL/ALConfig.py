from conf_comps import AL_COMPS
from al_comp import ALComp


class ALConfig:
    ## Data
    data_path = 'FOIL/data_file/ad/ad_initial.json'  # Path to the dataset
    data_split_config = 'FOIL/data_file/ad/config_ad_initial.json'  # Path to the data split config file

    ## Active Learning
    al_comps: list[ALComp] = AL_COMPS  # Active learning components
    foil_model: str = 'ad_prof_neg_nocolor'    # Choose foil and label functions from
                                # ['ad_prof', 'ad_prof_neg_color', 'ad_prof_neg_nocolor', 'bird', 'medical']
    ## Results
    output_path = 'ad_seed1000-1050_random.json'  # Path to the output directory
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
    note = '''seed 1000-1050, random, 3+3*29. 
    '''
    # Disable tqdm progress bar (will be auto disabled if manual edtting round exists)
    tqdm_disable = False
