print("Loading...")

# Imports the necessary libraries and modules
import random
import json
import torch
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize

# If running chatbot for the first time
# with open("train.py") as train_file:
#     exec(train_file.read())

# If the laptop has a GPU, it will be used with training/running the chatbot (faster) - if not, the CPU will be used instead
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Uploads the JSON file as a dictionary
with open("intents.json", "r") as file:
    intents = json.load(file)

# Greps the values of the following variables/lists from the "data.pth" file
FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data["all_words"]
tags = data["tags"]
model_state = data["model_state"]

# Runs the feed forward network
model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "GP"

print("""\nWelcome to

 ██████╗ ██████╗ ███╗   ███╗███████╗
██╔════╝ ██╔══██╗████╗ ████║██╔════╝
██║  ███╗██████╔╝██╔████╔██║█████╗  
██║   ██║██╔═══╝ ██║╚██╔╝██║██╔══╝  
╚██████╔╝██║     ██║ ╚═╝ ██║███████╗
 ╚═════╝ ╚═╝     ╚═╝     ╚═╝╚══════╝
 

Here to give you quick and efficient diagnoses.

Type 'quit' to exit.""")

# Infinite loop (for the chatting system)
while True:
    # Tells the user when to input
    sentence = input("\nYou: ")

    # If the user types "quit", the program will end
    if sentence == "quit":
        # Exit message for when the user wishes to quit the program
        print(f"{bot_name}: Okay - see you later!")
        break

    sentence = tokenize(sentence)
    x = bag_of_words(sentence, all_words)
    x = x.reshape(1, x.shape[0])
    x = torch.from_numpy(x)

    output = model(x)
    _, predicted = torch.max(output, dim=1)
    tag = tags[predicted.item()]

    # Gets the probability of accuracy for a given response
    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]

    # The response will only be outputted if the probability of accuracy is greater than 75%
    if prob.item() > 0.75:
        for intent in intents["intents"]:
            if tag == intent["tag"]:
                print(f"{bot_name}: {random.choice(intent['responses'])}")
    else:
        print(f"{bot_name}: Sorry - I don't understand.")