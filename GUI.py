# GUI: Tkinter GUI for Peg Solitaire Game

import tkinter as tk
from tkinter import messagebox

def show_message(title,message):
    messagebox.showinfo(title, message)

def main():
    root = tk.Tk()
    root.title("Peg Solitaire Game")

    #Simple Label
    label = tk.Label(root, text="Welcome to Peg Solitaire Game")
    label.pack(pady=50)

    #Add Lines
    line1 = tk.Label(root, text="------------------------------")
    line1.pack()

    #Simple Button
    button = tk.Button(root, text="Click Here to Start the Game", command=lambda: show_message("Game Start", "Starting the Peg Solitaire Game..."))
    button.pack(pady=15)

    #Radio Button
    radio_var = tk.StringVar(value="Language")
    radio1 = tk.Radiobutton(root, text="English", variable=radio_var, value="English")
    radio1.pack(pady=5)
    radio2 = tk.Radiobutton(root, text="Spanish", variable=radio_var, value="Spanish")
    radio2.pack(pady=5)
    root.mainloop()

if __name__ =="__main__":
    main()