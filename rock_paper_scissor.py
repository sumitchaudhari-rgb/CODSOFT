import tkinter as tk
from tkinter import messagebox
import random

CHOICES = ["Rock", "Paper", "Scissors"]

def get_computer_choice():
    return random.choice(CHOICES)

def decide_winner(user, computer):
    if user == computer:
        return "tie"
    if (
        (user == "Rock" and computer == "Scissors") or
        (user == "Scissors" and computer == "Paper") or
        (user == "Paper" and computer == "Rock")
    ):
        return "win"
    return "lose"

class RPSGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Rock, Paper, Scissors")
        self.root.resizable(False, False)

        # Colors
        self.bg_color = "#1e1f2e"
        self.card_color = "#2e3047"
        self.accent_color = "#ffb347"
        self.win_color = "#4caf50"
        self.lose_color = "#f44336"
        self.tie_color = "#03a9f4"
        self.text_color = "#f5f5f5"

        self.root.configure(bg=self.bg_color)

        self.user_score = 0
        self.computer_score = 0

        # Main container "card"
        main_frame = tk.Frame(root, bg=self.card_color, bd=2, relief="ridge", padx=15, pady=15)
        main_frame.pack(padx=20, pady=20)

        # Title
        title_label = tk.Label(
            main_frame,
            text="Rock • Paper • Scissors",
            font=("Segoe UI", 20, "bold"),
            fg=self.accent_color,
            bg=self.card_color
        )
        title_label.pack(pady=(0, 10))

        # Instructions
        instr = (
            "Choose Rock, Paper, or Scissors.\n"
            "Rock beats Scissors, Scissors beat Paper, Paper beats Rock."
        )
        instr_label = tk.Label(
            main_frame,
            text=instr,
            justify="center",
            font=("Segoe UI", 10),
            fg=self.text_color,
            bg=self.card_color
        )
        instr_label.pack(pady=(0, 10))

        # Scoreboard
        score_frame = tk.Frame(main_frame, bg=self.card_color)
        score_frame.pack(pady=5)
        self.user_score_label = tk.Label(
            score_frame,
            text="Your Score: 0",
            font=("Segoe UI", 11, "bold"),
            fg="#8bc34a",
            bg=self.card_color
        )
        self.user_score_label.pack(side="left", padx=10)

        self.comp_score_label = tk.Label(
            score_frame,
            text="Computer Score: 0",
            font=("Segoe UI", 11, "bold"),
            fg="#e57373",
            bg=self.card_color
        )
        self.comp_score_label.pack(side="left", padx=10)

        # Separator
        sep = tk.Frame(main_frame, bg="#44475a", height=2)
        sep.pack(fill="x", pady=10)

        # Choices
        choice_label = tk.Label(
            main_frame,
            text="Make your choice:",
            font=("Segoe UI", 12, "bold"),
            fg=self.text_color,
            bg=self.card_color
        )
        choice_label.pack(pady=(0, 5))

        btn_frame = tk.Frame(main_frame, bg=self.card_color)
        btn_frame.pack(pady=5)

        self.create_choice_button(btn_frame, "Rock", "#ff7043").pack(side="left", padx=5)
        self.create_choice_button(btn_frame, "Paper", "#29b6f6").pack(side="left", padx=5)
        self.create_choice_button(btn_frame, "Scissors", "#ab47bc").pack(side="left", padx=5)

        # Result area "card"
        result_frame = tk.Frame(main_frame, bg="#242538", bd=1, relief="groove", padx=10, pady=10)
        result_frame.pack(pady=10, fill="x")

        self.choices_label = tk.Label(
            result_frame,
            text="You chose: -   |   Computer chose: -",
            font=("Segoe UI", 10),
            fg=self.text_color,
            bg="#242538"
        )
        self.choices_label.pack(pady=(0, 5))

        self.result_label = tk.Label(
            result_frame,
            text="Result: -",
            font=("Segoe UI", 14, "bold"),
            fg=self.tie_color,
            bg="#242538"
        )
        self.result_label.pack()

        # Bottom controls
        bottom_frame = tk.Frame(main_frame, bg=self.card_color)
        bottom_frame.pack(pady=(10, 0))

        self.play_again_btn = self.create_small_button(
            bottom_frame, "Play Again", self.ask_play_again, "#66bb6a"
        )
        self.play_again_btn.pack(side="left", padx=5)

        reset_btn = self.create_small_button(
            bottom_frame, "Reset Scores", self.reset_scores, "#ffa726"
        )
        reset_btn.pack(side="left", padx=5)

        quit_btn = self.create_small_button(
            bottom_frame, "Quit", self.root.quit, "#ef5350"
        )
        quit_btn.pack(side="left", padx=5)

    def create_choice_button(self, parent, text, color):
        return tk.Button(
            parent,
            text=text,
            width=10,
            font=("Segoe UI", 11, "bold"),
            fg="white",
            bg=color,
            activebackground=color,
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=lambda t=text: self.play_round(t)
        )

    def create_small_button(self, parent, text, command, color):
        return tk.Button(
            parent,
            text=text,
            font=("Segoe UI", 10, "bold"),
            fg="white",
            bg=color,
            activebackground=color,
            activeforeground="white",
            relief="flat",
            padx=10,
            pady=4,
            cursor="hand2",
            command=command
        )

    def play_round(self, user_choice):
        computer_choice = get_computer_choice()
        result = decide_winner(user_choice, computer_choice)

        self.choices_label.config(
            text=f"You chose: {user_choice}   |   Computer chose: {computer_choice}"
        )

        if result == "win":
            self.user_score += 1
            self.result_label.config(text="Result: You WIN!", fg=self.win_color)
        elif result == "lose":
            self.computer_score += 1
            self.result_label.config(text="Result: You LOSE!", fg=self.lose_color)
        else:
            self.result_label.config(text="Result: It's a TIE!", fg=self.tie_color)

        self.update_scores()

    def update_scores(self):
        self.user_score_label.config(text=f"Your Score: {self.user_score}")
        self.comp_score_label.config(text=f"Computer Score: {self.computer_score}")

    def ask_play_again(self):
        answer = messagebox.askyesno("Play Again", "Do you want to continue playing?")
        if not answer:
            self.root.quit()
        else:
            self.choices_label.config(text="You chose: -   |   Computer chose: -")
            self.result_label.config(text="Result: -", fg=self.tie_color)

    def reset_scores(self):
        self.user_score = 0
        self.computer_score = 0
        self.update_scores()
        self.choices_label.config(text="You chose: -   |   Computer chose: -")
        self.result_label.config(text="Result: -", fg=self.tie_color)

if __name__ == "__main__":
    root = tk.Tk()
    app = RPSGame(root)
    root.mainloop()