# Imports the package required for the loader
from halo import Halo

# Starts the loader
spinner = Halo(text='Loading')
spinner.start()

# Imports the necessary libraries and modules - placed under loader due to the long importing period
import random
from pathlib import Path
import json
from pwinput import pwinput
from datetime import datetime
import torch
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize

# Stops the spinner (to signify the end of the importing period)
spinner.stop()

def login():
    print("\n========================= Login Page =========================")
    while True:
        # Queries whether the user already has an account or wants to quit the program
        have_account = input("\nLogging in to an existing account? (y/n/quit) ")

        # Ensures one of the desired responses are given
        while have_account not in ["y", "n", "quit"]:
            have_account = input("Invalid response - logging in to an existing account? (y/n/quit) ")

        # If the user says they have an account, the login procedure is initiated
        if have_account == "y":
            username = input("\nEnter your username: ")
            while username not in users.keys():
                username = input("Unregistered username entered - enter your username: ")

            access_token = pwinput("\nEnter your password: ")
            while access_token != users.get(username):
                access_token = pwinput("Access Denied - enter your password: ")
            
            # Once successfully completed, the user is admitted to the main menu
            main_menu(username)
            break
        # If the user does not have an account, they will undergo the registration process
        elif have_account == "n":
            print("\n------------------------- Account Registration -------------------------")
            new_user = input("\nPick a username (type 'quit' to exit): ")
            
            # Ensures the selected username is unique
            while new_user in users.keys():
                new_user = input("Username already exists - pick another username: ")
            
            # If the user wishes to quit the program (e.g. because they actually wanted to sign in, or want to quit the program), they will be brought back to the login page
            if new_user == "quit":
                print("\n========================= Redirecting to Login Page =========================")
                continue
            
            # Password confirmation - if two passwords aren't the same, the user will be asked to redo the password stage
            passwords_same = "n"
            while passwords_same == "n":
                new_password = pwinput("\nPick a password: ")
                confirm_new_password = pwinput("\nRe-type your password: ")
                if confirm_new_password != new_password:
                    print("\nPasswords do not match! Password prompt reset.")
                else:
                    break
            
            # Appends the newly generated username and password into the "existing_users" file, as well as  into the "user_keylog" database (for "past diagnosis" storage)
            users[new_user] = new_password
            keylog[new_user] = {}

            with open("existing_users.json", "w") as outfile:
                json.dump(users, outfile)
            
            with open("user_keylog.json", "w") as outfile:
                json.dump(keylog, outfile)

            # Informs the user the process was successful, and takes them to the login page
            print("\nAccount successfully registered!")
            print("\n========================= Redirecting to Login Page =========================")
        else:
            print("\nOkay - hope to see you soon!")
            break

def main_menu(username):
    # The user has three options - to initiate the chatbot, view their keylog or quit the program
    option = input("""\nPick an option:
1. Talk to the GP
2. View past diagnoses
3. Log Out
Option: """)
    
    # Ensures a valid option is selected
    while option not in ["1", "2", "3"]:
        option = input("""\nInvalid option selected - pick an option:
1. Talk to the GP
2. View past diagnoses
3. Log Out
Option: """)
    
    # Allows the selected option to take the user to the desired page
    if option == "1":
        chatbot(username)
    elif option == "2":
        view_keylog(username)
    else:
        print("\nLogging out.")
        login()

def chatbot(username):
    # Creates the global variable that records the date of diagnosis (to be accessed in the keylog function)
    global str_timestamp
    
    print("""\n------------------------- Chatbot -------------------------

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
            # Obtains today's date
            current_time = datetime.now()
            timestamp = datetime.fromtimestamp(current_time.timestamp())
            str_timestamp = timestamp.strftime("%d %B, %Y")
            
            # Only appends the timestamp to the keylog database if it isn't already there (to avoid replication)
            if str_timestamp not in keylog[username]:
                time_append = {str_timestamp: []}
                keylog[username] = keylog[username] | time_append

            # Outputs the result
            for intent in intents["intents"]:
                if tag == intent["tag"]:
                    # The printed result
                    chosen_response = random.choice(intent["responses"])
                    print(f"{bot_name}: {chosen_response}")
                    
                    # Only saves the diagnosis into the keylog database if it doesn't already exist in it (to avert duplication)
                    if intent["tag"] not in keylog[username][str_timestamp]:
                        keylog[username][str_timestamp].append(intent["tag"])

                    # Saves the newly entered keylog into the external "user_keylog.json" file
                    with open("user_keylog.json", "w") as outfile:
                        json.dump(keylog, outfile)
        # Otherwise, the chatbot exclaims it does not understand
        else:
            print(f"{bot_name}: Sorry - I don't understand.")
    
    # Redirects the user to the main menu (if they desire to quit)
    main_menu(username)

def view_keylog(username):
    print("\n------------------------- Diagnosis Record -------------------------")

    # A message for users who haven't yet gotten a diagnosis
    if keylog[username] == {}:
        print("\nNo past record.")

    # Outputs the past diagnoses given by the chatbot, in correlation to the date (and order) it was given
    for timestamp in keylog[username]:
        print(f"\n{timestamp}:")
        for diagnosis in keylog[username][timestamp]:
            print(f"- {diagnosis.title()}: {diagnosis_info[diagnosis]}")
    
    # Redirects the user to the main menu
    main_menu(username)

# Imports the "existing users" dictionary into the program
path = Path("existing_users.json")
contents = path.read_text()
users = json.loads(contents)

# Imports the "keylog" dictionary into the program
path = Path("user_keylog.json")
contents = path.read_text()
keylog = json.loads(contents)

# The shortened form of the chatbot's remedies for particular diagnoses (used in the keylog for easy access by the user)
diagnosis_info = {
    "headache": "Apply ice pack, rest, keep from high-stress activities",
    "allergies": "Take antihistamines, decongestants, anti-inflammatory agents (e.g. coticosteroid), an allergy shot",
    "cold": "Visit your local doctor, drink water, rest, eat healthy",
    "conjunctivitis": "Wash hands, avoid contact with eye, visit doctor if no improvement within 2-3 days",
    "nausea": "Drink water or milk (30-60 mins after vomiting), return to normal diet (after 8 hrs), visit doctor if worsened (e.g. bloody vomit)"
    }

# Introduction to the program - the user is asked whether they've run the program before (to determine whether training is required)
train = input("""\nWelcome to

 ██████╗ ██████╗ ███╗   ███╗███████╗
██╔════╝ ██╔══██╗████╗ ████║██╔════╝
██║  ███╗██████╔╝██╔████╔██║█████╗  
██║   ██║██╔═══╝ ██║╚██╔╝██║██╔══╝  
╚██████╔╝██║     ██║ ╚═╝ ██║███████╗
 ╚═════╝ ╚═╝     ╚═╝     ╚═╝╚══════╝
                                    

Here to give you quick and efficient diagnoses.

Is this your first time running GPMe on your device? (y/n) """)

# Ensures the response given is valid
while train not in ["y", "n"]:
    train = input("Invalid response - is this your first time running the program on your device? (y/n) ")

# If running chatbot for the first time, the training file will be run
if train == "y":
    # Loader initiated
    spinner = Halo(text='Training the chatbot')
    spinner.start()

    # Training undertaken
    with open("train.py") as train_file:
        exec(train_file.read())
    
    # Loader stopped once training has completed
    spinner.stop()

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

# Opens the login page
login()