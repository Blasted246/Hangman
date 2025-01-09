import tkinter as tk
from tkinter import messagebox
import requests
import time

class HangmanGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Hangman")
        self.master.attributes("-fullscreen", True)
        self.master.configure(background="black")
        self.word = ""
        self.guessing_word = []
        self.num_guesses = 0
        self.lives = 6
        self.score = 0
        self.apiURL = "https://api.wordnik.com/v4/words.json/randomWord?hasDictionaryDef=true&includePartOfSpeech=noun&minCorpusCount=8000&maxCorpusCount=-1&minDictionaryCount=3&maxDictionaryCount=-1&minLength=3&maxLength=8&api_key=a2a73e7b926c924fad7001ca3111acd55af2ffabf50eb4ae5"

        self.center_window()

        self.exit_button = tk.Button(master, text="Exit", command=master.quit, font=("Helvetica", 20), bg="black", fg="white")
        self.exit_button.place(x=10, y=10)

        self.word_label = tk.Label(master, text="", font=("Helvetica", 40), anchor=tk.CENTER, bg="black", fg="white")
        self.word_label.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

        self.lives_label = tk.Label(master, text="Lives: 6", font=("Helvetica", 40), anchor=tk.CENTER, bg="black", fg="white")
        self.lives_label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

        self.score_label = tk.Label(master, text="Score: 0", font=("Helvetica", 40), anchor=tk.CENTER, bg="black", fg="white")
        self.score_label.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        self.guess_entry = tk.Entry(master, font=("Helvetica", 40), justify=tk.CENTER, bg="black", fg="white", insertbackground="white")
        self.guess_entry.bind("<Return>", self.check_guess)
        self.guess_entry.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.guess_button = tk.Button(master, text="Guess", command=self.check_guess, font=("Helvetica", 40), anchor=tk.CENTER, bg="black", fg="white")
        self.guess_button.configure(relief=tk.FLAT, highlightbackground="#3498db", highlightcolor="#3498db", highlightthickness=2)
        self.guess_button.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

        self.new_game_button = tk.Button(master, text="New Game", command=self.new_game, font=("Helvetica", 40), anchor=tk.CENTER, bg="black", fg="white")
        self.new_game_button.configure(relief=tk.FLAT, highlightbackground="#3498db", highlightcolor="#3498db", highlightthickness=2)
        self.new_game_button.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

        self.new_game()

    def center_window(self):
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        width = 500
        height = 500
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)
        self.master.geometry('%dx%d+%d+%d' % (width, height, x, y))

    def new_game(self):
        self.word = self.get_random_word()
        self.guessing_word = ["_"] * len(self.word)
        self.num_guesses = 0
        self.lives = 6
        self.word_label['text'] = " ".join(self.guessing_word)
        self.lives_label['text'] = "Lives: " + str(self.lives)

    def get_random_word(self):
        while True:
            try:
                response = requests.get(self.apiURL)
                word = response.json()["word"].lower()
                return word
            except KeyError:
                print("Retrying request due to KeyError")
                time.sleep(1)

    def check_guess(self, event=None):
        letterGuess = self.guess_entry.get()
        self.guess_entry.delete(0, tk.END)  # Clear the text box after a guess
        if len(letterGuess) == 1:  # Single letter guess
            if letterGuess in self.word:
                for idx, char in enumerate(self.word):
                    if char == letterGuess:
                        self.guessing_word[idx] = letterGuess
            else:
                self.num_guesses += 1
                self.lives -= 1
        elif len(letterGuess) > 1:  # whole word guess
            if letterGuess == self.word:
                self.guessing_word = list(letterGuess)
                self.score += 1
            else:
                self.num_guesses += 1
                self.lives -= 1
        self.word_label['text'] = " ".join(self.guessing_word)
        self.lives_label['text'] = "Lives: " + str(self.lives)
        self.score_label['text'] = "Score: " + str(self.score)
        if self.lives <= 0:
            messagebox.showinfo("Game Over", "You lost, the word was: " + self.word)
            self.new_game()
        elif "_" not in self.guessing_word:
            messagebox.showinfo("Game Over", "You won")
            self.new_game()

root = tk.Tk()
my_gui = HangmanGUI(root)
root.mainloop()

