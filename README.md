# Rapid
This is a github repository for RAPID, a tool with neuro-symbolic learning method. Rapid combines pre-trained CV models and inductive logic learning to infer logic-based labeling rules with a small amount of labeled data.

![RAPID Overview](https://github.com/Neural-Symbolic-Image-Labeling/Rapid/blob/main/teaser.png)


## Installation
You should follow the instruction (https://docs.python.org/3/library/venv.html) to create a virtual environment with Python 3.10 and activate it. Here we provide an example on Windows:
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
![Method Overview](https://github.com/Neural-Symbolic-Image-Labeling/Rapid/blob/main/pipeline-1.png)

We put 4 datasets on it, called ad, prof, medical and bird. You can find the json files under FOIL/data_file. These files are generated from the CV model with images as input.

Before you run the code, some parts need to be chosen:

1.You should choose the correct Active Learning strategy in FOIL/strategies/utils.py, in similarity_sample(*args) function, the _default should be choosed when using ad and prof dataset, the med corresponds to medical and bird for bird. **Please choose the right one before running the system.**

2. You should choose the right file

You can directly run our ActiveLearning/FOIL/rule_format_deamon.py to see the result!

## Contributing
All students below contribute a lot to this work, under supervision of Prof. Tianyi Zhang from Purdue CS.

Yifeng Wang, Zhi Tu, Yiwen Xiang, Shiyuan Zhou, Xiyuan Chen, Bingxuan Li

If you have any questions, either about the code or paper, welcome to contact us via email!

## Citation
