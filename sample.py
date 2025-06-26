import tkinter as tk
from tkinter import messagebox
from collections import deque
from PIL import Image, ImageTk

# BFS algorithm to find the minimum moves
def BFS(start, n, ladder, snake):
    q = deque([(start, 0, [], [])])  # Store (current position, moves, path, rolls)
    visited = [False] * (n + 1)
    visited[start] = True

    while q:
        current_position, moves, path, rolls = q.popleft()
        path.append(current_position)

        if current_position == n:
            return moves, path, rolls

        for dice_roll in range(1, 7):
            next_position = current_position + dice_roll
            if next_position > n:
                continue

            # Check for ladders and snakes
            if next_position in ladder:
                next_position = ladder[next_position]
            elif next_position in snake:
                next_position = snake[next_position]

            if not visited[next_position]:
                visited[next_position] = True
                q.append((next_position, moves + 1, path.copy(), rolls + [dice_roll]))

    return -1, [], []  # In case no solution is found

def findMinimumMoves(ladder, snake):
    n = 100
    moves, path, rolls = BFS(1, n, ladder, snake)
    return moves, path, rolls

class SnakesAndLaddersGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snakes and Ladders")

        self.bg_image = Image.open(r"C:\Users\bhavya\OneDrive\Desktop\AI_CaseStudy\Board.jpg")  # Ensure the correct path
        self.bg_image = self.bg_image.resize((400, 400), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        self.canvas = tk.Canvas(self.root, width=400, height=400)
        self.canvas.pack()
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_photo)

        self.token_radius = 15
        self.token = self.canvas.create_oval(0, 0, self.token_radius * 2, self.token_radius * 2, fill='blue')

        self.token_outside_x = 420
        self.token_outside_y = 50
        self.canvas.coords(self.token, self.token_outside_x - self.token_radius, self.token_outside_y - self.token_radius,
                           self.token_outside_x + self.token_radius, self.token_outside_y + self.token_radius)

        self.ladder = {
            4: 14,
            9: 31,
            21: 42,
            28: 84,
            51: 67,
            72: 91,
            80: 99
        }
        self.snake = {
            17: 7,
            54: 34,
            62: 19,
            64: 60,
            87: 36,
            93: 73,
            95: 75,
            98: 79
        }

        self.current_position = 1
        self.total_moves, self.path_taken, self.dice_rolls = findMinimumMoves(self.ladder, self.snake)
        self.move_index = 0  # Index to track the path during moves

        self.dice_button = tk.Button(self.root, text="Roll Dice", command=self.roll_dice)
        self.dice_button.pack(pady=10)

        self.position_label = tk.Label(self.root, text="Player Position: 1")
        self.position_label.pack(pady=10)

        self.result_label = tk.Label(self.root, text="Minimum Moves: " + str(self.total_moves))
        self.result_label.pack(pady=10)

        self.path_label = tk.Label(self.root, text="Path Taken: " + str(self.path_taken))
        self.path_label.pack(pady=10)

        self.rolls_label = tk.Label(self.root, text="Dice Rolls: " + str(self.dice_rolls))
        self.rolls_label.pack(pady=10)

    def update_token_position(self, position):
        if position > 1:
            x, y = self.get_position(position)
            self.canvas.coords(self.token, x - self.token_radius, y - self.token_radius,
                               x + self.token_radius, y + self.token_radius)
        else:
            self.canvas.coords(self.token, self.token_outside_x - self.token_radius,
                               self.token_outside_y - self.token_radius,
                               self.token_outside_x + self.token_radius, self.token_outside_y + self.token_radius)

    def get_position(self, position):
        square_size = 40
        row = (position - 1) // 10
        col = (position - 1) % 10

        if row % 2 == 0:
            x = col * square_size + (square_size // 2)
        else:
            x = (9 - col) * square_size + (square_size // 2)

        y = (9 - row) * square_size + (square_size // 2)
        return x, y

    def roll_dice(self):
        if self.move_index < len(self.path_taken):
            # Update the current position based on the pre-calculated path
            self.current_position = self.path_taken[self.move_index]
            self.position_label.config(text=f"Player Position: {self.current_position}")

            # Update token position
            self.update_token_position(self.current_position)

            self.move_index += 1  # Move to the next position in the path

            if self.current_position == 100:
                messagebox.showinfo("Game Over", f"Congratulations! You reached the end in {self.total_moves} moves!")
        else:
            messagebox.showinfo("Game Over", "You have completed the path!")

if __name__ == '__main__':
    root = tk.Tk()
    game = SnakesAndLaddersGame(root)
    root.mainloop()
