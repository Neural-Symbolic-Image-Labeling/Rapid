# Rapid
This is an official Github repository for RAPID, a tool with neuro-symbolic learning method. Rapid combines pre-trained CV models and inductive logic learning to infer logic-based labeling rules with a small amount of labeled data. （This codebase is still under construction, and the possible finish date is xxx）

![RAPID Overview](https://github.com/Neural-Symbolic-Image-Labeling/Rapid/blob/main/picture/teaser.png)


## Installation
You should follow the [instruction](https://docs.python.org/3/library/venv.html) to create a virtual environment with Python 3.10 and activate it. Here we provide an example on Windows:
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

Before you run the code, some parts need to be chosen:

1. You should choose the correct Active Learning (AL) strategy in FOIL/strategies/utils.py, in similarity_sample(*args) function, the _default should be choosed when using ad and prof dataset, the med corresponds to medical and bird for bird. **Please choose the right one before running the system.**
2. You should choose the right data file for running. In ActiveLearning/FOIL/rule_format_deamon.py, for data_path and data_split_config, please choose the right json file and config file for corresponding dataset you want.
3. You can select some initial images before training, using the id in config file. If so, you should use al_comp ManualComp to choose the initial images. If you don't want manually select, you can choose al_comp RandomComp to select randomly. Besides you need to choose rounds and instance number per round for AL. There are also different AL strategies you can use. （Add a table here to help users）
4. Choose the correspond foil model to use. "bird1" means bird dataset and "medical" means medical dataset. Other models can be used by either ad or prof dataset.

Then you can directly run our ActiveLearning/FOIL/rule_format_deamon.py to see the result!

When running, you can also choose manual mode (by typing "y" in terminal), which means you can change, delete and lock the rules as you want. However, you can also refuse the function if you just want the AL choose the picture and update the rules automatically. (by typing "n" in terminal)

If you choose y, in each iteration, you can enter the rule and press enter to see the accuracy. If you don't want to change the rule anymore, you can enter c, it will jump to the lock and delete mode. An example for delete (lock) format on trafic scene dataset : {'downtown': [[['building'], ['building'], 0]], 'highway': [], 'mountain road': []} (This means you will delete building clause from downtown rule).

**Notice**: when typing in the terminal, make sure the rules you enter is in one line, else it will raise error.


## Citation
