import tkinter as tk
import random
import time

class MemoryCardGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Memory Card Matching Game")
        self.root.geometry("500x550")
        self.root.resizable(False, False)

        # Game variables
        self.grid_size = 4  # 4x4 grid
        self.num_pairs = (self.grid_size ** 2) // 2
        self.cards = []
        self.buttons = []
        self.flipped = []
        self.matched = []
        self.move_count = 0
        self.start_time = None
        self.timer_running = False
        self.max_moves = 20

        # GUI setup
        self.top_frame = tk.Frame(self.root)
        self.top_frame.pack(pady=10)

        self.move_label = tk.Label(self.top_frame, text="Moves: 0", font=("Arial", 12))
        self.move_label.pack(side=tk.LEFT, padx=20)

        self.timer_label = tk.Label(self.top_frame, text="Time: 0s", font=("Arial", 12))
        self.timer_label.pack(side=tk.LEFT, padx=20)

        self.restart_button = tk.Button(self.top_frame, text="Restart", command=self.restart_game)
        self.restart_button.pack(side=tk.LEFT, padx=20)

        self.board_frame = tk.Frame(self.root)
        self.board_frame.pack(pady=20)

        self.setup_game()

    def setup_game(self):
        # Create pairs of cards
        self.cards = list(range(1, self.num_pairs + 1)) * 2
        random.shuffle(self.cards)

        self.buttons = []
        self.flipped = []
        self.matched = []
        self.move_count = 0
        self.update_move_label()

        # Reset timer
        self.start_time = time.time()
        self.timer_running = True
        self.update_timer()

        # Clear board
        for widget in self.board_frame.winfo_children():
            widget.destroy()

        # Create grid of buttons
        for i in range(self.grid_size):
            row = []
            for j in range(self.grid_size):
                btn = tk.Button(self.board_frame, text="*", width=8, height=4,
                                command=lambda i=i, j=j: self.flip_card(i, j))
                btn.grid(row=i, column=j, padx=5, pady=5)
                row.append(btn)
            self.buttons.append(row)

    def flip_card(self, i, j):
        if (i, j) in self.matched or (i, j) in self.flipped:
            return

        index = i * self.grid_size + j
        card_value = self.cards[index]
        self.buttons[i][j].config(text=str(card_value), state="disabled")
        self.flipped.append((i, j))

        if len(self.flipped) == 2:
            self.root.after(500, self.check_match)
            self.move_count += 1
            self.update_move_label()

    def check_match(self):
        (i1, j1), (i2, j2) = self.flipped
        idx1 = i1 * self.grid_size + j1
        idx2 = i2 * self.grid_size + j2

        if self.cards[idx1] == self.cards[idx2]:
            self.matched.extend([(i1, j1), (i2, j2)])
        else:
            self.buttons[i1][j1].config(text="*", state="normal")
            self.buttons[i2][j2].config(text="*", state="normal")

        self.flipped = []
        self.check_game_over()

    def check_game_over(self):
        if len(self.matched) == len(self.cards):
            self.timer_running = False
            tk.messagebox.showinfo("Game Over", f"Congratulations! You won in {self.move_count} moves and {int(time.time()-self.start_time)} seconds!")
        elif self.move_count >= self.max_moves:
            self.timer_running = False
            tk.messagebox.showinfo("Game Over", "You exceeded the maximum moves. Try again!")

    def update_move_label(self):
        self.move_label.config(text=f"Moves: {self.move_count}")

    def update_timer(self):
        if self.timer_running:
            elapsed = int(time.time() - self.start_time)
            self.timer_label.config(text=f"Time: {elapsed}s")
            self.root.after(1000, self.update_timer)

    def restart_game(self):
        self.setup_game()

if __name__ == "__main__":
    root = tk.Tk()
    import tkinter.messagebox  # for message dialogs
    game = MemoryCardGame(root)
    root.mainloop()
