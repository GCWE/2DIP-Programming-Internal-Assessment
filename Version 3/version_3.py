# Imports the package required for the loader
from halo import Halo

# Starts the loader
spinner = Halo(text='Loading')
spinner.start()

# Imports the necessary libraries and modules - placed under loader due to the long importing period
from tkinter import *
import random
from pathlib import Path
import json
from datetime import datetime
import torch
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize
import os.path

# If the datafile has not yet been created, the training file will be run
if os.path.isfile("./data.pth") == False:
    import train

# Stops the spinner (to signify the end of the importing period)
spinner.stop()

def login_check():
    """If the username and password match an existing user's credentials, the main menu will open - otherwise, an appropriate invalidity message appears"""
    if str(ent_username.get()) in users.keys() and str(ent_password.get()) == users.get(ent_username.get()):
        main_menu()
    else:
        txt_login_response.delete("1.0", END)
        txt_login_response.insert(END, "Username/Password invalid - try again!")

def signup():
    """Creates the Sign Up page"""
    
    # Closes the login page
    root.withdraw()

    # Creates the sign up page's window
    global signup_page
    signup_page = Toplevel()
    signup_page.title("Sign Up")
    signup_page.geometry("975x542")
    signup_page.configure(bg = "#FFFFFF")

    # Creates a box within the window with which to work from
    signup_canvas = Canvas(
        signup_page,
        bg = "#FFFFFF",
        height = 542,
        width = 975,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    # Establishes the location of the canvas
    signup_canvas.place(x = 0, y = 0)

    # Creates the image located on the side of the signup screen
    signup_canvas.create_image(
        226.0,
        271.0,
        image=side_image
    )

    # The sign up page's title
    signup_canvas.create_text(
        645.0,
        39.0,
        anchor="nw",
        text="Sign Up",
        fill="#000000",
        font=("Inter Regular", 40 * -1)
    )

    # Description of sign up page
    signup_canvas.create_text(
        550.0,
        107.0,
        anchor="nw",
        text="Save your diagnoses, all in one place.",
        fill="#000000",
        font=("Inter Regular", 20 * -1)
    )

    # Label for the username field
    signup_canvas.create_text(
        535.0,
        164.0,
        anchor="nw",
        text="Pick a Username",
        fill="#000000",
        font=("Inter Regular", 20 * -1)
    )

    # Username entry field
    signup_canvas.create_image(
        709.5,
        210.0,
        image=credential_entry_img
    )
    global ent_new_username
    ent_new_username = Entry(
        signup_canvas,
        bd=0,
        bg="#EAE7E7",
        fg="#000716",
        highlightthickness=0
    )
    ent_new_username.place(
        x=546.0,
        y=195.0,
        width=327.0,
        height=28.0
    )

    # Label for the password field
    signup_canvas.create_text(
        535.0,
        251.0,
        anchor="nw",
        text="Pick a Password",
        fill="#000000",
        font=("Inter Regular", 20 * -1)
    )

    # Password entry field
    signup_canvas.create_image(
        709.5,
        296.5,
        image=credential_entry_img
    )
    global ent_new_password
    ent_new_password = Entry(
        signup_canvas,
        bd=0,
        bg="#EAE7E7",
        fg="#000716",
        highlightthickness=0,
        show="*"
    )
    ent_new_password.place(
        x=546.5,
        y=281.0,
        width=326.0,
        height=29.0
    )

    # Label for password confirmation field
    signup_canvas.create_text(
        535.0,
        339.0,
        anchor="nw",
        text="Confirm Password",
        fill="#000000",
        font=("Inter Regular", 20 * -1)
    )

    # Password confirmation entry field
    signup_canvas.create_image(
        709.5,
        384.5,
        image=credential_entry_img
    )
    global ent_confirm_password
    ent_confirm_password = Entry(
        signup_canvas,
        bd=0,
        bg="#EAE7E7",
        fg="#000716",
        highlightthickness=0,
        show="*"
    )
    ent_confirm_password.place(
        x=546.5,
        y=369.0,
        width=326.0,
        height=29.0
    )

    # Button to sign up user-entered credentials - links to the following function
    btn_signup = Button(
        signup_canvas,
        image=signup_button_img,
        borderwidth=0,
        highlightthickness=0,
        command=signup_check,
        relief="flat"
    )
    btn_signup.place(
        x=655.0,
        y=432.0,
        width=110.0,
        height=33.0
    )

    # Creates the invisible textbox from which invalidity messages will appear
    signup_canvas.create_image(
        710.0,
        502.0,
        image=invisible_response_img
    )
    global txt_signup_response
    txt_signup_response = Text(
        signup_canvas,
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0
    )
    txt_signup_response.place(
        x=545.0,
        y=486.0,
        width=330.0,
        height=30.0
    )

    # Ensures the page cannot be resized (considering the "place" method was used)
    signup_page.resizable(False, False)

def signup_check():
    """Ensures the user-entered credentials are unique"""

    # Clears the invisible textbox (in case a message has already been outputted within it)
    txt_signup_response.delete("1.0", END)
    
    # Only saves the credentials if the username is unique, the entered passwords match, and no spaces are blank
    if ent_new_username.get() in users.keys():
        txt_signup_response.insert(END, "Username already taken!")
    elif ent_new_password.get() != ent_confirm_password.get():
        txt_signup_response.insert(END, "Passwords do not match!")
    elif ent_new_password.get() == "" or ent_new_username.get() == "":
        txt_signup_response.insert(END, "Enter a valid username and password!")
    else:
        # Appends the newly generated username and password into the "existing_users" file, as well as  into the "user_keylog" database (for "past diagnosis" storage)
        users[ent_new_username.get()] = ent_new_password.get()
        keylog[ent_new_username.get()] = {}

        with open("existing_users.json", "w") as outfile:
            json.dump(users, outfile)
        
        with open("user_keylog.json", "w") as outfile:
            json.dump(keylog, outfile)

        exit(signup_page)
        txt_login_response.insert(END, "Account created successfully!")

def main_menu():
    """Opens the main menu page"""

    # Closes the login page
    root.withdraw()

    # Builds the main menu window
    global menu_page
    menu_page = Toplevel()
    menu_page.title("Main Menu")
    menu_page.geometry("536x494")
    menu_page.configure(bg = "#FFFFFF")

    # Creates the box from which the labels and buttons may be formed
    main_menu_canvas = Canvas(
        menu_page,
        bg = "#FFFFFF",
        height = 494,
        width = 536,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    # Positions the canvas
    main_menu_canvas.place(x = 0, y = 0)

    # The main menu page's title
    main_menu_canvas.create_text(
        175.0,
        48.0,
        anchor="nw",
        text="Main Menu",
        fill="#000000",
        font=("Inter Regular", 40 * -1)
    )

    # The "Talk to GP" button
    btn_talk = Button(
        main_menu_canvas,
        image=talk_img,
        borderwidth=0,
        highlightthickness=0,
        command=chat,
        relief="flat"
    )
    btn_talk.place(
        x=159.0,
        y=129.0,
        width=216.0,
        height=136.0
    )

    # The "View Past Diagnoses" button
    btn_view_diagnoses = Button(
        main_menu_canvas,
        image=view_diagnoses_img,
        borderwidth=0,
        highlightthickness=0,
        command=view_diagnoses,
        relief="flat"
    )
    btn_view_diagnoses.place(
        x=24.0,
        y=302.0,
        width=216.0,
        height=139.0
    )

    # The "Exit" button
    btn_exit = Button(
        main_menu_canvas,
        image=exit_img,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: exit(menu_page),
        relief="flat"
    )
    btn_exit.place(
        x=295.0,
        y=302.0,
        width=216.0,
        height=139.0
    )

    # Ensures the main menu page cannot be resized (as the "place" method is used)
    menu_page.resizable(False, False)

def exit(page):
    """The function through which the program may quit to the login page"""

    # Closes whichever page the function was called from
    page.withdraw()
    
    # Reopens the login page, and clear the username, password and invisible textbox fields
    root.deiconify()
    ent_username.delete(0, END)
    ent_username.insert(END, "")

    ent_password.delete(0, END)
    ent_password.insert(END, "")

    txt_login_response.delete("1.0", END)

def chat():
    """The chatbot page"""
    
    # Creates the chatbot page window
    global chat_page
    chat_page = Toplevel()
    chat_page.title("Chat")
    chat_page.geometry("354x542")
    chat_page.configure(bg = "#FFFFFF")

    # Creates the box from which the labels and buttons will be created
    chatbot_canvas = Canvas(
        chat_page,
        bg = "#FFFFFF",
        height = 542,
        width = 354,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    # Positions the canvas in the chat window
    chatbot_canvas.place(x = 0, y = 0)

    # Creates the chat page's title
    chatbot_canvas.create_text(
        142.0,
        19.0,
        anchor="nw",
        text="Chat",
        fill="#000000",
        font=("Inter Regular", 36 * -1)
    )

    # The section from which the chat results will be outputted
    chatbot_canvas.create_image(
        176.5,
        270.5,
        image=chat_result_img
    )
    global txt_chat_result
    txt_chat_result = Text(
        chat_page,
        bd=0,
        bg="#EBEBEB",
        fg="#000716",
        highlightthickness=0,
        wrap=WORD
    )
    txt_chat_result.place(
        x=29.0,
        y=82.0,
        width=300.0,
        height=375.0
    )

    # The first message - establishes that the user can begin asking queries
    txt_chat_result.insert(END, f"{bot_name}: Hey there, {ent_username.get()}! What can I do for you today?")
    
    # Ensures the "chat result" section cannot be tampered with
    txt_chat_result.config(state=DISABLED)

    # Creates the entry section from which the user can provide their questions
    chatbot_canvas.create_image(
        131.0,
        508.0,
        image=chat_entry_img
    )
    global ent_chat_entry
    ent_chat_entry = Entry(
        chat_page,
        bd=0,
        bg="#EBEBEB",
        fg="#000716",
        highlightthickness=0
    )
    ent_chat_entry.place(
        x=25.0,
        y=488.0,
        width=212.0,
        height=38.0
    )
    
    # The button which, when clicked, will send the message to the neural network (to be processed)
    btn_send = Button(
        chat_page,
        image=send_img,
        borderwidth=0,
        highlightthickness=0,
        command=send_result,
        relief="flat"
    )
    btn_send.place(
        x=251.725341796875,
        y=484.0,
        width=89.274658203125,
        height=49.0
    )

    # Ensures the program isn't resizable (as the "place" method is being used)
    chat_page.resizable(False, False)

def send_result():
    """The processing of the user input"""

    # Allows the "chat result" section to be editable for a fraction of a moment
    txt_chat_result.config(state=NORMAL)
    
    # Executes the neural network
    sentence = tokenize(ent_chat_entry.get())
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
        if str_timestamp not in keylog[ent_username.get()]:
            time_append = {str_timestamp: []}
            keylog[ent_username.get()] = keylog[ent_username.get()] | time_append

        # Outputs the result
        for intent in intents["intents"]:
            if tag == intent["tag"]:
                # The printed result
                chosen_response = random.choice(intent["responses"])
                txt_chat_result.insert(END, f"\n\nYou: {ent_chat_entry.get()}\n\n{bot_name}: {chosen_response}")
                
                # Only saves the diagnosis into the keylog database if it doesn't already exist in it (to avert duplication)
                if intent["tag"] not in keylog[ent_username.get()][str_timestamp] and intent["tag"] not in ["greeting", "goodbye", "thanks"]:
                    keylog[ent_username.get()][str_timestamp].append(intent["tag"])

                # Saves the newly entered keylog into the external "user_keylog.json" file
                with open("user_keylog.json", "w") as outfile:
                    json.dump(keylog, outfile)
    # Otherwise, the chatbot exclaims it does not understand
    else:
        txt_chat_result.insert(END, f"\n\nYou: {ent_chat_entry.get()}\n\n{bot_name}: Sorry - I don't understand.")

    # Clears the "chat entry" section (to allow the user to enter another query)
    ent_chat_entry.delete(0, END)
    ent_chat_entry.insert(END, "")

    # "Locks" the "chat result" section again
    txt_chat_result.config(state=DISABLED)

    # Ensures the "chat result" section follows the bottom of the textbox (for when queries fill up more than the section's available space)
    txt_chat_result.yview_pickplace("end")

def view_diagnoses():
    """Creates the "View Diagnoses" page"""

    # Builds the diagnoses viewer window
    diagnoses_page = Toplevel()
    diagnoses_page.title("View Diagnoses")
    diagnoses_page.geometry("608x494")
    diagnoses_page.configure(bg = "#FFFFFF")

    # Creates the box from which the labels and textboxes will be built
    diagnoses_canvas = Canvas(
        diagnoses_page,
        bg = "#FFFFFF",
        height = 494,
        width = 608,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    # Positions the canvas within the diagnoses viewer window
    diagnoses_canvas.place(x = 0, y = 0)

    # Creates the diagnoses viewer's title
    diagnoses_canvas.create_text(
        170.0,
        26.0,
        anchor="nw",
        text="Past Diagnoses",
        fill="#000000",
        font=("Inter Regular", 40 * -1)
    )

    # Creates the textbox where the past diagnoses will be outputted
    diagnoses_canvas.create_image(
        303.5,
        278.0,
        image=diagnoses_results_img
    )
    txt_diagnoses_results = Text(
        diagnoses_canvas,
        bd=0,
        bg="#F6F6F6",
        fg="#000716",
        highlightthickness=0,
        wrap=WORD
    )
    txt_diagnoses_results.place(
        x=41.0,
        y=99.0,
        width=525.0,
        height=371.0
    )

    # Clears the "diagnoses results" section (in case previous, outdated information has remained from prior usage of the page)
    txt_diagnoses_results.delete("1.0", END)

    # A message for users who haven't yet gotten a diagnosis
    if keylog[ent_username.get()] == {}:
        txt_diagnoses_results.insert(END, "No past record.")

    # Outputs the past diagnoses given by the chatbot, in correlation to the date (and order) it was given
    for timestamp in keylog[ent_username.get()]:
        txt_diagnoses_results.insert(END, f"{timestamp}:\n")
        for diagnosis in keylog[ent_username.get()][timestamp]:
            txt_diagnoses_results.insert(END, f"- {diagnosis.title()}: {diagnosis_info[diagnosis]}\n")
        txt_diagnoses_results.insert(END, "\n")

    # Ensures the textbox cannot be tampered with
    txt_diagnoses_results.config(state=DISABLED)

    # Establishes that the window isn't resizable (due to the fact that the "place" method is being used)
    diagnoses_page.resizable(False, False)

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
    "allergies": "Take antihistamines, decongestants, anti-inflammatory agents, allergy shot",
    "cold": "Visit your local doctor, drink water, rest, eat healthy",
    "conjunctivitis": "Wash hands, avoid contact with eye, visit doctor if no improvement within 2-3 days",
    "nausea": "Drink water or milk, visit doctor if worsened (e.g. bloody vomit)",
    "back pain": "Keep active - should leave in a couple of weeks",
    "sore throat": "Drink water, suck on ice cubes, rest well.",
    "sinusitis": "Rest lots, drink lots, avoid smoking",
}

# Creates the login page's window
root = Tk()

root.title("Log In")
root.geometry("975x542")
root.configure(bg = "#FFFFFF")

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

# The name of the bot (interchangeable)
bot_name = "GP"

# The image to the left of the login and sign up pages
side_image = PhotoImage(
    file="images/side_image.png")

# The username/password entry field on the login and sign up pages
credential_entry_img = PhotoImage(
    file="images/credential_entry.png")

# The login button styling
login_button_img = PhotoImage(
    file="images/login_button.png")

# The invisible textbox on the login and sign up pages
invisible_response_img = PhotoImage(
    file="images/invisible_response.png")

# The sign up button styling
signup_button_img = PhotoImage(
    file="images/signup_button.png")

# The "Talk to GP" button styling
talk_img = PhotoImage(
    file="images/talk.png")

# The "View Past Diagnoses" button styling
view_diagnoses_img = PhotoImage(
    file="images/past_diagnoses.png")

# The "Exit" button styling
exit_img = PhotoImage(
    file="images/exit.png")

# The "chat result" section
chat_result_img = PhotoImage(
    file="images/chat_output.png")

# The "chat entry" section
chat_entry_img = PhotoImage(
    file="images/chat_entry.png")

# The send button (on the chatbot page) styling
send_img = PhotoImage(
    file="images/send.png")

# The textbox styling for the diagnoses viewer page
diagnoses_results_img = PhotoImage(
    file="images/diagnoses.png")

# Creates the box from which the labels, buttons and textbox will be built
login_canvas = Canvas(
    root,
    bg = "#FFFFFF",
    height = 542,
    width = 975,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

# Positions the canvas in the login page
login_canvas.place(x = 0, y = 0)

# Creates the side image
login_picture = login_canvas.create_image(
    226.0,
    271.0,
    image=side_image
)

# Creates the login page's title
login_canvas.create_text(
    545.0,
    32.0,
    anchor="nw",
    text="Welcome to GPMe.",
    fill="#000000",
    font=("Inter Regular", 40 * -1)
)

# The login page's description
login_canvas.create_text(
    515.0,
    97.0,
    anchor="nw",
    text="Here to give you quick and efficient diagnoses.",
    fill="#000000",
    font=("Inter Regular", 20 * -1)
)

# The sub-heading (telling the user that this is the login page)
login_canvas.create_text(
    660.0,
    140.0,
    anchor="nw",
    text="Login",
    fill="#000000",
    font=("Inter Bold", 40 * -1)
)

# The username field label
login_canvas.create_text(
    530.0,
    204.0,
    anchor="nw",
    text="Username",
    fill="#000000",
    font=("Inter Regular", 20 * -1)
)

# The username entry field
ent_username_bg = login_canvas.create_image(
    709.5,
    250.0,
    image=credential_entry_img
)
ent_username = Entry(
    bd=0,
    bg="#EAE7E7",
    fg="#000716",
    highlightthickness=0
)
ent_username.place(
    x=546.0,
    y=235.0,
    width=327.0,
    height=28.0
)

# The password field label
login_canvas.create_text(
    530.0,
    277.0,
    anchor="nw",
    text="Password",
    fill="#000000",
    font=("Inter Regular", 20 * -1)
)

# The password entry field
ent_password_bg = login_canvas.create_image(
    709.5,
    322.5,
    image=credential_entry_img
)
ent_password = Entry(
    bd=0,
    bg="#EAE7E7",
    fg="#000716",
    highlightthickness=0,
    show="*"
)
ent_password.place(
    x=546.5,
    y=307.0,
    width=326.0,
    height=29.0
)

# The button which, when clicked, check whether the credentials entered are of an existing user's
btn_login = Button(
    image=login_button_img,
    borderwidth=0,
    highlightthickness=0,
    command=login_check,
    relief="flat"
)
btn_login.place(
    x=664.0,
    y=360.0,
    width=90.0,
    height=32.0
)

# The label which "introduces" the sign up button
login_canvas.create_text(
    610.0,
    412.0,
    anchor="nw",
    text="Don’t have an account?",
    fill="#000000",
    font=("Inter Regular", 20 * -1)
)

# The sign up button which, when clicked, will redirect the user to the sign up page
btn_signup = Button(
    image=signup_button_img,
    borderwidth=0,
    highlightthickness=0,
    command=signup,
    relief="flat"
)
btn_signup.place(
    x=654.0,
    y=446.0,
    width=110.0,
    height=33.0
)

# The invisble textbox from which invalidity messages (as well as messages of successful account registrations) are outputted
login_response_bg = login_canvas.create_image(
    710.0,
    511.0,
    image=invisible_response_img
)
txt_login_response = Text(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
txt_login_response.place(
    x=545.0,
    y=495.0,
    width=330.0,
    height=30.0
)

# Ensures the login page isn't resizable (as the "place" method is being used)
root.resizable(False, False)

# Ensures the login page opens
root.mainloop()