# 2DIP Programming Internal Assessment - GPMe

## Brief
A program for diagnosing simple illnesses, through a Feed Forward Neural Network - this makes use of probability to determine the accuracy of the produced result.

Each of the above folders contains individual iterations of the program - the first two are text-based, while the final three are GUI-based (constructed using Tkinter and Figma).


## Requirements

Below are the contents of the requirements.txt file:
```
halo==0.0.31
nltk==3.8.1
numpy==1.24.3
torch==2.0.1
```

Be sure to import these modules/libraries before running the program.
```
$ pip install halo nltk numpy torch
```

Additionally, you'll need to run the following in the terminal (or uncomment line 8 in nltk_utils.py):
```
$ python
>>> import nltk
>>> nltk.download('punkt')
```

This downloads the "bare bones" model through which the neural network can be built on my own data.

### Note:
This program does not at all intend to replace traditional diagnosis methods - it does, however, aim to provide users particularly with low access to medical services to get a simple diagnosis without fear of the constraints on time or money.

The hope is that one day this program transcends to assist the medical field where finance hits hardest.

~ Gladon Chua
