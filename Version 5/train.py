# Imports the necessary libraries and modules
import json
from nltk_utils import tokenize, stem, bag_of_words
import numpy as np

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

from model import NeuralNet

# Uploads the JSON file as a dictionary
with open("intents.json", "r") as file:
    intents = json.load(file)

# Creates an empty list for all the words, the various tags and the pattern-tag pair
all_words = []
tags = []
xy = []

for intent in intents["intents"]:
    # Adds every tag in the intents.json file to the tags list
    tag = intent["tag"]
    tags.append(tag)
    
    # Tokenizes all words from the pattern into the all_words and xy lists (the latter of which will contain an array)
    for pattern in intent["patterns"]:
        tokenized_pattern = tokenize(pattern)
        all_words.extend(tokenized_pattern)
        xy.append((tokenized_pattern, tag))

# For word stemming, only characters besides those below will be "rooted"
ignore_words = ["?", "!", ".", ","]

all_words = [stem(word) for word in all_words if word not in ignore_words]

# Sorts all words alphabetically and removes duplicates
all_words = sorted(set(all_words))

# Alphabetical order
tags = sorted(set(tags))

# x_train for patterns, y_train for tags
x_train = []
y_train = []

for (pattern_sentence, tag) in xy:
    # Converts the sentences to "0" and "1" values (in correspondence with all words)
    bag = bag_of_words(pattern_sentence, all_words)
    x_train.append(bag)

    # Gets the index of each tag
    label = tags.index(tag)
    y_train.append(label)

x_train = np.array(x_train)
y_train = np.array(y_train)

# Uses the bag of words to fuel the pattern and tag data
class ChatDataset(Dataset):
    def __init__(self):
        self.number_of_samples = len(x_train)
        self.x_data = x_train
        self.y_data = y_train

    # dataset[index]

    def __getitem__(self, index):
        return self.x_data[index], self.y_data[index]
    
    def __len__(self):
        return self.number_of_samples

# Hyperparameters
batch_size = 8
hidden_size = 8
output_size = len(tags)
input_size = len(x_train[0]) # Same as len(all_words)
learning_rate = 0.001
num_epochs = 10000

# Loads x_data and y_data
dataset = ChatDataset()
train_loader = DataLoader(dataset=dataset, batch_size = batch_size, shuffle=True, num_workers=0)

# Uses the device's GPU if available - if not, the CPU is used instead
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = NeuralNet(input_size, hidden_size, output_size).to(device)

# Loss and optimiser
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

# Training Loop
for epoch in range(num_epochs):
    for (words, labels) in train_loader:
        words = words.to(device)
        labels = labels.to(device, dtype=torch.int64)

    # Forward pass
    outputs = model(words)
    loss = criterion(outputs, labels)

    # Backward and optimizer step
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

# Allows the dataset to be accessed elsewhere by exporting it to a Pytorch file
data = {
    "model_state": model.state_dict(),
    "input_size": input_size,
    "output_size": output_size,
    "hidden_size": hidden_size,
    "all_words": all_words,
    "tags": tags
}

FILE = "data.pth"
torch.save(data, FILE)