# [KDD 23] Rapid Image Labeling via Neuro-Symbolic Learning
This is the official Github repository for ``[Rapid Image Labeling via Neuro-Symbolic Learning](https://arxiv.org/abs/2306.10490)'' (KDD2023 Acceptance). 

RAPID is a tool with a neuro-symbolic learning method. Rapid combines pre-trained CV models and inductive logic learning to infer logic-based labeling rules with a small amount of labeled data. Please look into our [dataset](https://drive.google.com/drive/folders/1gBw0Rn2MfhCbzPZxCVuIld-DmALN9bPA?usp=share_link) here. We recommand you to directly use the json data in our data/datasets file, which are generated from the CV model with images as input.

![RAPID Overview](https://github.com/Neural-Symbolic-Image-Labeling/Rapid/blob/main/picture/teaser.png)


## Installation
You should follow the [instruction](https://docs.python.org/3/library/venv.html) to create a virtual environment with Python 3.10 and activate it. Here we provide an example on Windows with pip (You can choose conda following the [instruction](https://numdifftools.readthedocs.io/en/stable/how-to/create_virtual_env_with_conda.html)):
1. Go to your 3.10 base
2. Create the virtual environment (the env just for example, you can change it to the name you like)   
```
python -m venv env
```
3. Activate
```
.\env\Scripts\Activate
```
After you get the virtual environment, you can install our requirment.txt (mainly for Active Learning module)
```
pip install -r requirements.txt
```
**Done!**

## Usage
![Method Overview](https://github.com/Neural-Symbolic-Image-Labeling/Rapid/blob/main/picture/pipeline-1.png)

We put 4 datasets on it, called ad, prof, medical and bird, meaning Trafic Scene, Occupation, Glaucoma and Bird Species. You can find the json files under FOIL/data_file. These files are generated from the CV model with images as input.

Before you run the code, please check the config.py file first:

1. You should choose the correct Foil model in line foil_model: str =, the _default should be choosed when using ad and prof dataset, the med corresponds to medical and bird for bird. **Please choose the right one before running the system.**
2. You should choose the right data file for running. In config.py, for data_path and data_split_config, please choose the right json file and config file for corresponding dataset you want.
3. If you want choose manual mode, which means you can change, delete and lock the rules as you want, please set enable_editing = True in config.py.
<!--3. You can select some initial images before training, using the id in config file. If so, you should use al_comp ManualComp to choose the initial images. If you don't want manually select, you can choose al_comp RandomComp to select randomly. Besides you need to choose rounds and instance number per round for AL. There are also different AL strategies you can use. （Add a table here to help users）-->


Then you can directly run main.py to see the result!

If you choose manual mode, in each iteration, you can enter the rule and press enter to see the accuracy. If you don't want to change the rule anymore, you can enter c, it will jump to the lock and delete mode. An example for delete (lock) format on trafic scene dataset : {'downtown': [[['building'], ['building'], 0]], 'highway': [], 'mountain road': []} (This means you will delete building clause from downtown rule). If you donnot want to enter delete or lock, just enter c to skip this. Then you can see a question: Do you want to move to the next query? Choose y to go to next iteration or n to go back to lock and delet mode. (These characters should be in lower case).

**Notice**: when typing in the terminal, make sure the rules you enter is in one line, else it will raise error.


## Citation
```
@inproceedings{
wang2023rapid,
title={Rapid Image Labeling via Neuro-Symbolic Learning},
author={Wang, Yifeng and Tu, Zhi and Xiang, Yiwen and Zhou, Shiyuan and Chen, Xiyuan and Li, bingxuan and Zhang, Tianyi},
booktitle={29th SIGKDD Conference on Knowledge Discovery and Data Mining - Research Track},
year={2023},
}
```
