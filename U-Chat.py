
# for securit of personal api key
import os
from urllib import response
from dotenv import load_dotenv

# GUI
import tkinter as tk # Python’s built-in GUI toolkit.
from tkinter import DISABLED, scrolledtext  # to display chat conversations

# core
import google.generativeai as genai

# Load API key from .env file
load_dotenv()
api_key=os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("API key not found! Make sure you have a .env file with GOOGLE_API_KEY set.")

genai.configure(api_key = api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

 

# MAIN APP
root = tk.Tk() # initializes the main application window.
root.title("U-Chat") # sets the window title bar.
root.geometry("500x600") # defines the size of the window in pixels. "widget * height".

# Chat display (read-only)
chat_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Arial", 12))
chat_display.config(state=tk.DISABLED)
chat_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

#  User input
user_input = tk.Entry(root, font=('Arial', 12))
user_input.pack(padx=10, pady=10, fill=tk.X)

#  Send button and logic
def send_message():
    prompt = user_input.get().strip()
    if prompt:
        chat_display.config(state=tk.NORMAL)
        chat_display.insert(tk.END , f"You: {prompt}\n\n")
        chat_display.config(state=tk.DISABLED)
        user_input.delete(0,tk.END)

        # Get Gemini Response 
        try:
            response = model.generate_content(prompt)
            bot_reply = response.text.strip()
        except Exception as e:
            bot_reply= f"Error:{str(e)}"
        
        # Display Gemini (bot) message
        chat_display.config(state=tk.NORMAL)
        chat_display.insert(tk.END, f"Gemini: {bot_reply}\n\n")
        chat_display.config(state=tk.DISABLED)

        # Save the conversation to history
        with open("chat_history.txt", "a", encoding="utf-8") as file:
            file.write(f"You: {prompt}\nGemini: {bot_reply}\n\n")


user_input.bind("<Return>", lambda event: send_message())  # to send message by pressing Enter Key

def clear_chat():
    chat_display.config(state=tk.NORMAL)
    chat_display.delete(1.0, tk.END)
    chat_display.config(state=tk.DISABLED)

    # Optional: clear the chat history file
    with open("chat_history.txt", "w", encoding="utf-8") as file:
        file.write("")


send_button = tk.Button(root, text="Send", command=send_message, width=10, height=2)
send_button.pack(pady=(0, 5))

clear_button = tk.Button(root, text="Clear Chat", command=clear_chat, width=10, height=2)
clear_button.pack(pady=(0, 10))


# Start the App
root.mainloop()


"""
def ask():
    que = input("ask Question:(or press 1 to quit):")
    if que == "1":
        print("thank You!! See You soon!!")
        return 0

    load_dotenv()
    api_key=os.getenv("GOOGLE_API_KEY")

    if not api_key:
        raise ValueError("API key not found! Make sure you have a .env file with GOOGLE_API_KEY set.")

    genai.configure(api_key = api_key)


    # Create a model instance   
    model = genai.GenerativeModel("gemini-1.5-flash")

    # Generate content
    response = model.generate_content(que)

    # Print the result
    print(response.text)
    ask()

ask()
"""
