import random
import tkinter as tk
import threading
import time

games = [
    "Fortnite",
    "Apex Legends",
    "Call of Duty: Warzone",
    "Valorant",
    "Rocket League",
    "Overwatch 2",
    "League of Legends",
    "Counter-Strike 2",
    "Minecraft",
    "Destiny 2",
    "PUBG: Battlegrounds",
    "Rainbow Six Siege",
    "Dota 2",
    "Among Us",
    "Fall Guys",
    "Battlefield"
]

def suggest_game():
    return random.choice(games)


def animate_suggestion(label):
    label.config(text="Spinning the wheel...")
    for i in range(15):
        label.config(text=random.choice(games))
        label.update()
        time.sleep(0.08 + i*0.01)
    final_suggestion = suggest_game()
    label.config(text=f"Suggestion: {final_suggestion}")


def show_gui():
    root = tk.Tk()
    root.title("What Game To Play Tonight?")
    root.geometry("400x200")
    root.resizable(False, False)
    label = tk.Label(root, text="What game should you play tonight?", font=("Arial", 16))
    label.pack(pady=40)
    def start_animation():
        threading.Thread(target=animate_suggestion, args=(label,), daemon=True).start()
    button = tk.Button(root, text="Spin!", font=("Arial", 14), command=start_animation)
    button.pack(pady=10)
    root.mainloop()

if __name__ == "__main__":
    show_gui()
