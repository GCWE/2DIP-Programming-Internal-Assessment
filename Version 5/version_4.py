# Imports the package required for the loader
from halo import Halo

# Starts the loader
spinner = Halo(text="Loading")
spinner.start()

# Imports the necessary libraries and modules - placed under loader due to the long importing period

# Creates the GUI and "Lato" font
from tkinter import *
from tkinter.font import Font
from tkinter import messagebox

# Imports the JSON files (housing the multiple dictionaries)
from pathlib import Path
import json

# Picks a rnadom response from the "intents" file
import random

# Grabs the "timestamp" for user registration and diagnoses
from datetime import datetime

# Imports the PyTorch neural network and additional chatbot utilities
import torch
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize

# Used to identify whether the datafile exists
import os.path

# The Python regex module
import re

# For sending emails securely
from email.message import EmailMessage
import ssl
import smtplib

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
        messagebox.showerror("Invalid", "Invalid username and/or password.")

def signup():
    """Creates the Sign Up page"""

    # Closes the login page
    root.withdraw()
    
    # Creates the sign up page's window
    global signup_page
    signup_page = Toplevel()
    signup_page.title("Sign Up")
    signup_page.geometry("625x632")
    signup_page.configure(bg = "#E4F0FA")

    # The canvas in which the widgets are placeed
    signup_canvas = Canvas(
        signup_page,
        bg = "#E4F0FA",
        height = 632,
        width = 625,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    # Positions the canvas in the page
    signup_canvas.place(x = 0, y = 0)
    
    # The signup page title
    signup_canvas.create_text(
        231.0,
        46.0,
        anchor="nw",
        text="Sign Up",
        fill="#334669",
        font=Font(family="Lato", weight="bold", size=48 * -1)
    )

    # The signup page description
    signup_canvas.create_text(
        115.0,
        123.0,
        anchor="nw",
        text="Save your diagnoses, all in one place.",
        fill="#334669",
        font=Font(family="Lato", size=24 * -1)
    )
    
    # The "new username" label
    signup_canvas.create_text(
        78.0,
        196.0,
        anchor="nw",
        text="New Username",
        fill="#334669",
        font=Font(family="Lato", size=24 * -1)
    )

    # Entry field for new username
    signup_canvas.create_image(
        318.1208190917969,
        257.2101745605469,
        image=credential_entry_img
    )
    global ent_new_username
    ent_new_username = Entry(
        signup_canvas,
        bd=0,
        bg="#E3EDF7",
        fg="#000716",
        highlightthickness=0
    )
    ent_new_username.place(
        x=85.0,
        y=245.0,
        width=475.0,
        height=25.0
    )

    # "New password" label
    signup_canvas.create_text(
        75.0,
        306.0,
        anchor="nw",
        text="New Password",
        fill="#334669",
        font=Font(family="Lato", size=24 * -1)
    )

    # Entry for new password
    signup_canvas.create_image(
        319.1208190917969,
        366.2101745605469,
        image=credential_entry_img
    )
    global ent_new_password
    ent_new_password = Entry(
        signup_canvas,
        bd=0,
        bg="#E3EBF7",
        fg="#000716",
        highlightthickness=0,
        show="*"
    )
    ent_new_password.place(
        x=85.0,
        y=354.0,
        width=475.0,
        height=25.0
    )

    # "Confirm password" label
    signup_canvas.create_text(
        75.0,
        416.0,
        anchor="nw",
        text="Confirm Password",
        fill="#334669",
        font=Font(family="Lato", size=24 * -1)
    )

    # Password confirmation field
    signup_canvas.create_image(
        318.6205139160156,
        476.088134765625,
        image=credential_entry_img
    )
    global ent_confirm_password
    ent_confirm_password = Entry(
        signup_canvas,
        bd=0,
        bg="#E3EDF7",
        fg="#000716",
        highlightthickness=0,
        show="*"
    )
    ent_confirm_password.place(
        x=85.0,
        y=465.0,
        width=475.0,
        height=25.0
    )

    # Signup button - checks whether signup credentials are valid
    btn_signup = Button(
        signup_canvas,
        image=signup_button_img,
        borderwidth=0,
        highlightthickness=0,
        command=signup_check,
        relief="flat"
    )
    btn_signup.place(
        x=212.0,
        y=521.0,
        width=208.0,
        height=83.0
    )

    # Ensures the signup page cannot be resized (because place method is used)
    signup_page.resizable(False, False)

def signup_check():
    """Ensures the user-entered credentials are unique"""
    
    # Only saves the credentials if the username is unique, the entered passwords match, and no spaces are blank
    if ent_new_username.get() in users.keys():
        messagebox.showerror("Invalid", "Username already taken.")
    elif ent_new_password.get() != ent_confirm_password.get():
        messagebox.showerror("Invalid", "Passwords do not match.")
    elif ent_new_password.get() == "" or ent_new_username.get() == "":
        messagebox.showerror("Invalid", "Invalid username and/or password.")
    else:
        # Obtains today's date
        current_time = datetime.now()
        timestamp = datetime.fromtimestamp(current_time.timestamp())
        str_reg_date = timestamp.strftime("%d %B, %Y")
        
        # Appends the newly generated username and password into the "existing_users" file, as well as into the "registration date" and "user_keylog" database (for "past diagnosis" storage)
        users[ent_new_username.get()] = ent_new_password.get()
        reg_date[ent_new_username.get()] = str_reg_date
        keylog[ent_new_username.get()] = {}

        # Saves the changes to the corresponding files
        with open("existing_users.json", "w") as outfile:
            json.dump(users, outfile)
        
        with open("user_keylog.json", "w") as outfile:
            json.dump(keylog, outfile)

        with open("reg_date.json", "w") as outfile:
            json.dump(reg_date, outfile)

        # Closes the signup page (which opens the login page), and outputs a success message
        exit(signup_page)
        messagebox.showinfo("Success", "Account successfully registered!")

def main_menu():
    """Opens the main menu page"""

    # Closes the login page
    root.withdraw()

    # Builds the main menu window
    global menu_page
    menu_page = Toplevel()
    menu_page.title("Main Menu")
    menu_page.geometry("752x354")
    menu_page.configure(bg = "#E4F0FA")

    # The canvas through which the widgets will be built
    main_menu_canvas = Canvas(
        menu_page,
        bg = "#E4F0FA",
        height = 354,
        width = 752,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    # Positions the canvas in the main menu page
    main_menu_canvas.place(x = 0, y = 0)

    # Title of page
    main_menu_canvas.create_text(
        253.0,
        40.0,
        anchor="nw",
        text="Main Menu",
        fill="#334669",
        font=Font(family="Lato", weight="bold", size=48 * -1)
    )

    # Label for "Chat" button
    main_menu_canvas.create_text(
        73.0,
        282.0,
        anchor="nw",
        text="Chat with GP",
        fill="#334669",
        font=Font(family="Lato", size=24 * -1)
    )

    # Chat button (opens chat page)
    btn_chat = Button(
        main_menu_canvas,
        image=talk_img,
        borderwidth=0,
        highlightthickness=0,
        command=chat,
        relief="flat"
    )
    btn_chat.place(
        x=81.0,
        y=126.0,
        width=132.0,
        height=142.0
    )

    # Label for "View Past Diagnoses" button
    main_menu_canvas.create_text(
        264.0,
        282.0,
        anchor="nw",
        text="View Past Diagnoses",
        fill="#334669",
        font=Font(family="Lato", size=24 * -1)
    )

    # "View Past Diagnoses" button (opens diagnoses window)
    btn_view_diagnoses = Button(
        main_menu_canvas,
        image=view_diagnoses_img,
        borderwidth=0,
        highlightthickness=0,
        command=view_diagnoses,
        relief="flat"
    )
    btn_view_diagnoses.place(
        x=310.0,
        y=126.0,
        width=132.0,
        height=142.0
    )

    # Label for "Log Out" button
    main_menu_canvas.create_text(
        562.0,
        282.0,
        anchor="nw",
        text="Log Out",
        fill="#334669",
        font=Font(family="Lato", size=24 * -1)
    )

    # Logout button - closes main menu and redirects user to the login page
    btn_exit = Button(
        main_menu_canvas,
        image=exit_img,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: exit(menu_page),
        relief="flat"
    )
    btn_exit.place(
        x=539.0,
        y=126.0,
        width=132.0,
        height=142.0
    )
    
    # "Settings" button (opens the user info page)
    btn_settings = Button(
        main_menu_canvas,
        image=settings_button_img,
        borderwidth=0,
        highlightthickness=0,
        command=settings,
        relief="flat"
    )
    btn_settings.place(
        x=675.0,
        y=17.0,
        width=58.0,
        height=56.0
    )

    # Ensures the main menu cannot be resized (as the place method is used)
    menu_page.resizable(False, False)

def settings():
    """
    The settings page, through which the user may view their account information.
    
    It also offers them the opportunity to change their existing password and delete their account.
    """

    # Builds the settings page window
    global settings_page
    settings_page = Toplevel()
    settings_page.title("Settings")
    settings_page.geometry("434x359")
    settings_page.configure(bg = "#E4F0FA")

    # The canvas through which the widgets will be built
    settings_canvas = Canvas(
        settings_page,
        bg = "#E4F0FA",
        height = 359,
        width = 434,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    # Positions the canvas in the settings page
    settings_canvas.place(x = 0, y = 0)

    # The settings page's title
    settings_canvas.create_text(
        152.0,
        40.0,
        anchor="nw",
        text="Settings",
        fill="#334669",
        font=Font(family="Lato", weight="bold", size=36 * -1)
    )

    # The label describing the username
    settings_canvas.create_text(
        94.0,
        117.0,
        anchor="nw",
        text="Username:",
        fill="#334669",
        font=Font(family="Lato", weight="bold", size=16 * -1)
    )

    # The textbox holding the username
    txt_settings_user = Text(
        settings_canvas,
        bd=0,
        bg="#E4F0FA",
        fg="#000716",
        highlightthickness=0
    )
    txt_settings_user.place(
        x=198.0,
        y=117.5,
        width=218.0,
        height=26.0
    )

    # Outputs the username in the textbox before "locking" it (to prevent users from tampering with it)
    txt_settings_user.insert(END, ent_username.get())
    txt_settings_user.config(state=DISABLED)

    # The label describing the adjacent "change password" button
    settings_canvas.create_text(
        96.0,
        165.0,
        anchor="nw",
        text="Password:",
        fill="#334669",
        font=Font(family="Lato", weight="bold", size=16 * -1)
    )

    # The "change password" button - opens a page through which the user can modify their password
    btn_settings_change = Button(
        settings_canvas,
        image=settings_change_img,
        borderwidth=0,
        highlightthickness=0,
        command=change_password,
        relief="flat"
    )
    btn_settings_change.place(
        x=186.0,
        y=147.5,
        width=163.0,
        height=59.0
    )

    # The label decribing the adjacent registration date
    settings_canvas.create_text(
        41.0,
        216.0,
        anchor="nw",
        text="Registration Date:",
        fill="#334669",
        font=Font(family="Lato", weight="bold", size=16 * -1)
    )

    # The textbox containing the user's registration date
    txt_reg_date = Text(
        settings_canvas,
        bd=0,
        bg="#E4F0FA",
        fg="#000716",
        highlightthickness=0
    )
    txt_reg_date.place(
        x=198.0,
        y=217.0,
        width=218.0,
        height=26.0
    )

    # Outputs the user's registation date in the textbox before locking it (to prevent tampering)
    txt_reg_date.insert(END, reg_date[ent_username.get()])
    txt_reg_date.config(state=DISABLED)

    # The button allowing the user to delete their account
    btn_delete_account = Button(
        settings_canvas,
        image=delete_account_img,
        borderwidth=0,
        highlightthickness=0,
        command=delete_account,
        relief="flat"
    )
    btn_delete_account.place(
        x=128.0,
        y=252.0,
        width=176.0,
        height=71.0
    )

    # Ensures the settings page cannot be resized (as the place method is used)
    settings_page.resizable(False, False)

def change_password():
    """The page through which the user can change their existing password - requires confirmation."""

    # Closes the settings page
    settings_page.withdraw()

    # Builds the "Change Password" page
    global change_password_page
    change_password_page = Toplevel()
    change_password_page.title("Change Password")
    change_password_page.geometry("434x359")
    change_password_page.configure(bg = "#E4F0FA")

    # The canvas through which the following widgets are built
    change_password_canvas = Canvas(
        change_password_page,
        bg = "#E4F0FA",
        height = 359,
        width = 434,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    # Positions the canvas in the "Change Password" page
    change_password_canvas.place(x = 0, y = 0)

    # The change password page's title
    change_password_canvas.create_text(
        74.0,
        40.0,
        anchor="nw",
        text="Change Password",
        fill="#334669",
        font=("Lato Bold", 36 * -1)
    )

    # The label describing the "Old Password" entry field
    change_password_canvas.create_text(
        59.0,
        117.0,
        anchor="nw",
        text="Old Password:",
        fill="#334669",
        font=("Lato Bold", 16 * -1)
    )

    # The entry field for the user's "old password"
    change_password_canvas.create_image(
        297.5,
        131.73728942871094,
        image=subpage_entry_img
    )
    global ent_old_password
    ent_old_password = Entry(
        change_password_canvas,
        bd=0,
        bg="#E3EDF7",
        fg="#000716",
        highlightthickness=0,
        show="*"
    )
    ent_old_password.place(
        x=208.0,
        y=127.0,
        width=180.0,
        height=11
    )

    # The label describing the "New Password" entry field
    change_password_canvas.create_text(
        52.0,
        165.0,
        anchor="nw",
        text="New Password:",
        fill="#334669",
        font=("Lato Bold", 16 * -1)
    )

    # The entry field for the user's new password
    change_password_canvas.create_image(
        297.5,
        178.73728942871094,
        image=subpage_entry_img
    )
    global ent_change_password
    ent_change_password = Entry(
        change_password_canvas,
        bd=0,
        bg="#E3EDF7",
        fg="#000716",
        highlightthickness=0,
        show="*"
    )
    ent_change_password.place(
        x=208.0,
        y=174.0,
        width=180.0,
        height=11
    )

    # The label describing the "Confirm Password" field
    change_password_canvas.create_text(
        39.0,
        213.0,
        anchor="nw",
        text="Confirm Password:",
        fill="#334669",
        font=("Lato Bold", 16 * -1)
    )

    # The entry field in which the user must enter the same password as in the "New Password" entry
    change_password_canvas.create_image(
        297.5,
        226.73728942871094,
        image=subpage_entry_img
    )
    global ent_conf_change_password
    ent_conf_change_password = Entry(
        change_password_canvas,
        bd=0,
        bg="#E3EDF7",
        fg="#000716",
        highlightthickness=0,
        show="*"
    )
    ent_conf_change_password.place(
        x=208.0,
        y=222.0,
        width=180.0,
        height=11
    )

    # The button which, when clicked, verifies whether the new password credentials are valid
    btn_change_password = Button(
        change_password_canvas,
        image=change_password_button_img,
        borderwidth=0,
        highlightthickness=0,
        command=check_password_change,
        relief="flat"
    )
    btn_change_password.place(
        x=106.0,
        y=257.0,
        width=220.0,
        height=71.0
    )

    # Ensures the change password page cannot be resized (as the place method is used)
    change_password_page.resizable(False, False)

def check_password_change():
    # Only saves the new credentials if the old password is correctly entered, the new password matches the confirmation password and no spaces are left blank
    if ent_old_password.get() != ent_password.get():
        messagebox.showerror("Invalid", "Old password wrongly entered.")
    elif ent_change_password.get() == ent_old_password.get():
        messagebox.showerror("Invalid", "That's not a new password!")
    elif ent_change_password.get() != ent_conf_change_password.get():
        messagebox.showerror("Invalid", "Password confirmation failed.")
    elif ent_change_password.get() == "":
        messagebox.showerror("Invalid", "Enter a valid new password.")
    else:
        # Appends the newly modified password into the "existing_users" file
        users[ent_username.get()] = ent_change_password.get()

        with open("existing_users.json", "w") as outfile:
            json.dump(users, outfile)

        # Closes the change password page and menu page (to allow the user to login again with the new password, for further confirmation)
        change_password_page.withdraw()
        exit(menu_page)

        # Outputs a message to show the successful password change
        messagebox.showinfo("Success", "Password successfully changed!")

def delete_account():
    """Opens a messagebox that warns the user that they're deleting their entire account - if agreed to, deletion will be executed."""

    # Opens the messagebox querying whether the user really wants to destroy their account
    msg_delete_account = messagebox.askquestion("Warning", "Are you sure you want to delete your account?", icon="warning")

    # If so, the user's data within the external JSON files will be removed
    if msg_delete_account == "yes":
        del users[ent_username.get()]
        del keylog[ent_username.get()]
        del reg_date[ent_username.get()]
        
        with open("existing_users.json", "w") as outfile:
            json.dump(users, outfile)

        with open("user_keylog.json", "w") as outfile:
            json.dump(keylog, outfile)

        with open("reg_date.json", "w") as outfile:
            json.dump(reg_date, outfile)

        # Closes all open windows and redirects the user to the main menu
        settings_page.withdraw()
        exit(menu_page)

        # Outputs a message telling the user the account has successfully deleted
        messagebox.showinfo("Account Deleted", "Account successfully deleted.")
        
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

def chat():
    """The chatbot page"""
    
    # Creates the chatbot page window
    global chat_page
    chat_page = Toplevel()
    chat_page.title("Chat")
    chat_page.geometry("373x634+0+0")
    chat_page.configure(bg = "#E4F0FA")

    # The canvas through which the following widgets will be built
    chatbot_canvas = Canvas(
        chat_page,
        bg = "#E4F0FA",
        height = 634,
        width = 373,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    # Positions the canvas within the chat page
    chatbot_canvas.place(x = 0, y = 0)

    # The chat page's title
    chatbot_canvas.create_text(
        145.0,
        26.0,
        anchor="nw",
        text="Chat",
        fill="#334669",
        font=Font(family="Lato", weight="bold", size=40 * -1)
    )

    # Description of the chat page
    chatbot_canvas.create_text(
        52.0,
        79.0,
        anchor="nw",
        text="Share your problems, in privacy.",
        fill="#334669",
        font=Font(family="Lato", size=20 * -1)
    )

    # The textbox through which the user's conversation with the neural network will be outputted
    chatbot_canvas.create_image(
        185.5,
        340.5,
        image=chat_result_img
    )
    global txt_chat_result
    txt_chat_result = Text(
        chatbot_canvas,
        bd=0,
        bg="#E3EDF7",
        fg="#000716",
        highlightthickness=0,
        wrap=WORD
    )
    txt_chat_result.place(
        x=37.0,
        y=143.0,
        width=297.0,
        height=397.0
    )

    # The first message - establishes that the user can begin asking queries
    txt_chat_result.insert(END, f"{bot_name}: Hey there, {ent_username.get()}! What can I do for you today?")
    
    # Ensures the "chat result" section cannot be tampered with
    txt_chat_result.config(state=DISABLED)

    # The entrybox through which the user may type their questions to the chatbot
    chatbot_canvas.create_image(
        142.0,
        593.5,
        image=chat_entry_img
    )
    global ent_chat_entry
    ent_chat_entry = Entry(
        chatbot_canvas,
        bd=0,
        bg="#E3EDF7",
        fg="#000716",
        highlightthickness=0
    )
    ent_chat_entry.place(
        x=33.0,
        y=584.0,
        width=223.0,
        height=20.0
    )

    # The "send" button - gives the user's input in the entrybox to the neural network
    btn_send = Button(
        chatbot_canvas,
        image=send_img,
        borderwidth=0,
        highlightthickness=0,
        command=send_result,
        relief="flat"
    )
    btn_send.place(
        x=269.0,
        y=558.0,
        width=104.0,
        height=69.0
    )

    # Ensures the chat page cannot be resized (as the place method is used)
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
        # Obtains the date of diagnosis
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
        txt_chat_result.insert(END, f"\n\nYou: {ent_chat_entry.get()}\n\n{bot_name}: Sorry - I don't understand")

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
    global diagnoses_page
    diagnoses_page = Toplevel()
    diagnoses_page.title("View Diagnoses")
    diagnoses_page.geometry("586x431")
    diagnoses_page.configure(bg = "#E4F0FA")

    # Builds the canvas through which the following widgets will be constructed
    diagnoses_canvas = Canvas(
        diagnoses_page,
        bg = "#E4F0FA",
        height = 431,
        width = 586,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    # Positions the canvas within the diagnoses page
    diagnoses_canvas.place(x = 0, y = 0)

    # The title of the "Past Diagnoses" page
    diagnoses_canvas.create_text(
        130.0,
        24.0,
        anchor="nw",
        text="Past Diagnoses",
        fill="#334669",
        font=Font(family="Lato", weight="bold", size=48 * -1)
    )

    # The textbox through which the diagnoses are outputted
    diagnoses_canvas.create_image(
        292.5,
        254.5,
        image=diagnoses_img
    )
    txt_diagnoses_results = Text(
        diagnoses_canvas,
        bd=0,
        bg="#E3EDF7",
        fg="#000716",
        highlightthickness=0,
        wrap=WORD
    )
    txt_diagnoses_results.place(
        x=39.0,
        y=118.0,
        width=507.0,
        height=276.0
    )

    diagnoses_page.resizable(False, False)

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

# Imports the "registration date" dictionary into the program
path = Path("reg_date.json")
contents = path.read_text()
reg_date = json.loads(contents)

# Imports the "keylog" dictionary into the program
path = Path("user_keylog.json")
contents = path.read_text()
keylog = json.loads(contents)

# Creates the login page's window
root = Tk()
root.title("Log In")
root.geometry("567x636+0+0")
root.configure(bg = "#E4F0FA")

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
    "bronchitis": "Eat honey, drink water, rest well and stay away from others",
    "stomachache": "Talk to doctor if intensely painful or hard to swallow",
    "insect bite": "Wash bite with water, apply ice pack, don't scratch - visit doctor if remains for few days"
}

# The username/password entry field on the login and sign up pages
credential_entry_img = PhotoImage(
    file="images/entry_field.png")

# The login button styling
login_button_img = PhotoImage(
    file="images/login_button.png")

# The sign up button styling
signup_button_img = PhotoImage(
    file="images/signup_button.png")

# The "settings" button styling
settings_button_img = PhotoImage(
    file="images/settings_button.png")

# The "Talk to GP" button styling
talk_img = PhotoImage(
    file="images/chat_button.png")

# The "View Past Diagnoses" button styling
view_diagnoses_img = PhotoImage(
    file="images/past_diagnoses_button.png")

# The "Exit" button styling
exit_img = PhotoImage(
    file="images/exit_button.png")

# The "Change Password" button (on settings page) styling
settings_change_img = PhotoImage(
    file="images/settings_change.png")

# The "Delete Account" button (on settings page) styling
delete_account_img = PhotoImage(
    file="images/delete_account.png")

# The entry field styling for the "Change Password" and "Send Diagnoses Data" pages
subpage_entry_img = PhotoImage(
    file="images/subpage_entry.png")

# The "Change Password" button on the "Change Password" page
change_password_button_img = PhotoImage(
    file="images/change_password_button.png")

# The "chat result" section
chat_result_img = PhotoImage(
    file="images/chat_response.png")

# The "chat entry" section
chat_entry_img = PhotoImage(
    file="images/chat_entry.png")

# The send button (on the chatbot page) styling
send_img = PhotoImage(
    file="images/send_button.png")

# The textbox styling for the diagnoses viewer page
diagnoses_img = PhotoImage(
    file="images/diagnoses_output.png")

# Creates the canvas through which the following widgets are built
login_canvas = Canvas(
    root,
    bg = "#E4F0FA",
    height = 636,
    width = 567,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

# Positions the canvas within the login page
login_canvas.place(x = 0, y = 0)

# The login page's title
login_canvas.create_text(
    70.0,
    49.0,
    anchor="nw",
    text="Welcome to GPMe.",
    fill="#334669",
    font=Font(family="Lato", weight="bold", size=48 * -1)
)

# A description of the program as a whole
login_canvas.create_text(
    35.0,
    126.0,
    anchor="nw",
    text="Here to give you quick and efficient diagnoses.",
    fill="#334669",
    font=Font(family="Lato", size=24 * -1)
)

# Label describing the adjacent "Username" entry field
login_canvas.create_text(
    40.0,
    191.0,
    anchor="nw",
    text="Username",
    fill="#334669",
    font=Font(family="Lato", size=24 * -1)
)

# Entry field in which the user enters their existing username
login_canvas.create_image(
    285.8792419433594,
    251.735595703125,
    image=credential_entry_img
)
ent_username = Entry(
    login_canvas,
    bd=0,
    bg="#E3EDF7",
    fg="#000716",
    highlightthickness=0
)
ent_username.place(
    x=53.0,
    y=240,
    width=475.0,
    height=25.0
)

# Label describing the adjacent "Password" entry field
login_canvas.create_text(
    40.0,
    301.0,
    anchor="nw",
    text="Password",
    fill="#334669",
    font=Font(family="Lato", size=24 * -1)
)

# Entrybox for entering password for above username
login_canvas.create_image(
    285.62127685546875,
    360.735595703125,
    image=credential_entry_img
)
ent_password = Entry(
    login_canvas,
    bd=0,
    bg="#E3EDF7",
    fg="#000716",
    highlightthickness=0,
    show="*"
)
ent_password.place(
    x=53.0,
    y=348.0,
    width=475.0,
    height=25.0
)

# Button for validating username and password
btn_login = Button(
    login_canvas,
    image=login_button_img,
    borderwidth=0,
    highlightthickness=0,
    command=login_check,
    relief="flat"
)
btn_login.place(
    x=163.0,
    y=392.0,
    width=241.0,
    height=97.0
)

# Label for describing the "Sign Up" button below
login_canvas.create_text(
    182.0,
    507.0,
    anchor="nw",
    text="Don’t have an account?",
    fill="#334669",
    font=Font(family="Lato", slant="italic", size=20 * -1)
)

# Signup button - takes the user to the signup page if clicked
btn_signup = Button(
    login_canvas,
    image=signup_button_img,
    borderwidth=0,
    highlightthickness=0,
    command=signup,
    relief="flat"
)
btn_signup.place(
    x=183.0,
    y=529.0,
    width=208.0,
    height=83.0
)

# Ensures the login page isn't resizable (as the "place" method is being used)
root.resizable(False, False)

# Calls the login window to open
root.mainloop()