import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

def get_foil_label_fn(type):
    if type == 'ad_prof':
        from foil.model_label.foil import FOIL
        from foil.model_label.label2 import label as LABEL
    elif type == 'ad_prof_neg_color':
        from foil.model_label.foil_neg_vscode import neg_FOIL as FOIL
        from foil.model_label.label_neg_vscode import label as LABEL
    elif type == 'ad_prof_neg_nocolor':
        from foil.model_label.foil_neg_nocolor import neg_FOIL as FOIL
        from foil.model_label.label_neg_nocolor import label as LABEL
    elif type == 'bird1':
        from foil.model_label.bird_foil_for_vscode import FOIL
        from foil.model_label.bird_label_for_vscode import label as LABEL
    elif type == 'bird2':
        from foil.model_label.bird_foil_for_vscode_2 import FOIL
        from foil.model_label.bird_label_for_vscode import label as LABEL
    elif type == 'bird3':
        from foil.model_label.bird_foil_for_vscode_3 import FOIL
        from foil.model_label.bird_label_for_vscode import label as LABEL
    elif type == 'bird4':
        from foil.model_label.bird_foil_for_vscode_4 import FOIL
        from foil.model_label.bird_label_for_vscode import label as LABEL
    elif type == 'medical':
        from foil.model_label.medical_foil_for_vscode import FOIL
        from foil.model_label.medical_label_for_vscode import label as LABEL
    else:
        raise Exception('Invalid type')
    
    return FOIL, LABEL

