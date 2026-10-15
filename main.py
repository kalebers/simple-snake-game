import random
import tkinter as tk


class SnakeGame:
    CELL_SIZE = 20
    COLUMNS = 30
    ROWS = 20
    WIDTH = CELL_SIZE * COLUMNS
    HEIGHT = CELL_SIZE * ROWS
    BACKGROUND = "#101820"
    SNAKE_COLOR = "#4ade80"
    FOOD_COLOR = "#fb7185"

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Snake")
        self.root.resizable(False, False)
        self.root.configure(bg=self.BACKGROUND)
        self.root.bind("<KeyPress>", self.handle_key)

        self.menu = tk.Frame(root, bg=self.BACKGROUND, padx=48, pady=42)
        tk.Label(
            self.menu,
            text="SNAKE",
            font=("Helvetica", 36, "bold"),
            fg=self.SNAKE_COLOR,
            bg=self.BACKGROUND,
        ).pack(pady=(8, 4))
        tk.Label(
            self.menu,
            text="Uma demonstração clássica",
            font=("Helvetica", 13),
            fg="#cbd5e1",
            bg=self.BACKGROUND,
        ).pack(pady=(0, 24))
        self.make_button(self.menu, "Play", self.start_game).pack(fill="x", pady=5)
        self.make_button(self.menu, "Exit", self.root.destroy).pack(fill="x", pady=5)

        self.game = tk.Frame(root, bg=self.BACKGROUND, padx=16, pady=14)
        self.score_label = tk.Label(
            self.game,
            text="Pontos: 0",
            font=("Helvetica", 14, "bold"),
            fg="#f8fafc",
            bg=self.BACKGROUND,
            anchor="w",
        )
        self.score_label.pack(fill="x", pady=(0, 8))
        self.canvas = tk.Canvas(
            self.game,
            width=self.WIDTH,
            height=self.HEIGHT,
            bg="#17232e",
            highlightthickness=0,
        )
        self.canvas.pack()
        self.controls = tk.Frame(self.game, bg=self.BACKGROUND)
        self.controls.pack(fill="x", pady=(10, 0))
        self.hint = tk.Label(
            self.controls,
            text="Use as setas ou WASD para se mover",
            font=("Helvetica", 11),
            fg="#cbd5e1",
            bg=self.BACKGROUND,
        )
        self.hint.pack(side="left", pady=6)
        self.end_buttons = tk.Frame(self.controls, bg=self.BACKGROUND)
        self.make_button(self.end_buttons, "Jogar novamente", self.start_game).pack(
            side="left", padx=4
        )
        self.make_button(self.end_buttons, "Menu", self.show_menu).pack(
            side="left", padx=4
        )
        self.make_button(self.end_buttons, "Exit", self.root.destroy).pack(
            side="left", padx=4
        )

        self.after_id: str | None = None
        self.running = False
        self.score = 0
        self.show_menu()

    def make_button(
        self, parent: tk.Misc, text: str, command: object
    ) -> tk.Button:
        return tk.Button(
            parent,
            text=text,
            command=command,
            font=("Helvetica", 12, "bold"),
            fg="#101820",
            bg=self.SNAKE_COLOR,
            activebackground="#86efac",
            activeforeground="#101820",
            relief="flat",
            padx=16,
            pady=9,
            cursor="hand2",
        )

    def show_menu(self) -> None:
        self.stop_game()
        self.game.pack_forget()
        self.menu.pack()

    def start_game(self) -> None:
        self.stop_game()
        self.menu.pack_forget()
        self.game.pack()

        center = (self.COLUMNS // 2, self.ROWS // 2)
        self.snake = [center, (center[0] - 1, center[1]), (center[0] - 2, center[1])]
        self.direction = (1, 0)
        self.next_direction = self.direction
        self.score = 0
        self.running = True
        self.score_label.config(text="Pontos: 0")
        self.hint.pack(side="left", pady=6)
        self.end_buttons.pack_forget()
        self.place_food()
        self.draw()
        self.root.focus_set()
        self.tick()

    def stop_game(self) -> None:
        self.running = False
        if self.after_id is not None:
            self.root.after_cancel(self.after_id)
            self.after_id = None

    def handle_key(self, event: tk.Event) -> None:
        key_directions = {
            "Up": (0, -1),
            "w": (0, -1),
            "W": (0, -1),
            "Down": (0, 1),
            "s": (0, 1),
            "S": (0, 1),
            "Left": (-1, 0),
            "a": (-1, 0),
            "A": (-1, 0),
            "Right": (1, 0),
            "d": (1, 0),
            "D": (1, 0),
        }
        new_direction = key_directions.get(event.keysym)
        if (
            self.running
            and new_direction is not None
            and new_direction != (-self.direction[0], -self.direction[1])
        ):
            self.next_direction = new_direction

    def place_food(self) -> None:
        available = [
            (x, y)
            for x in range(self.COLUMNS)
            for y in range(self.ROWS)
            if (x, y) not in self.snake
        ]
        self.food = random.choice(available) if available else None

    def tick(self) -> None:
        if not self.running:
            return

        self.direction = self.next_direction
        head_x, head_y = self.snake[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        eating = new_head == self.food
        body_to_check = self.snake if eating else self.snake[:-1]

        if (
            not 0 <= new_head[0] < self.COLUMNS
            or not 0 <= new_head[1] < self.ROWS
            or new_head in body_to_check
        ):
            self.finish_game("Fim de jogo!")
            return

        self.snake.insert(0, new_head)
        if eating:
            self.score += 1
            self.score_label.config(text=f"Pontos: {self.score}")
            self.place_food()
            if self.food is None:
                self.finish_game("Você venceu!")
                return
        else:
            self.snake.pop()

        self.draw()
        self.after_id = self.root.after(115, self.tick)

    def draw(self) -> None:
        self.canvas.delete("all")
        if self.food is not None:
            self.draw_cell(self.food, self.FOOD_COLOR, inset=3)
        for index, segment in enumerate(self.snake):
            self.draw_cell(
                segment,
                "#86efac" if index == 0 else self.SNAKE_COLOR,
                inset=2,
            )

    def draw_cell(
        self, position: tuple[int, int], color: str, inset: int
    ) -> None:
        x, y = position
        left = x * self.CELL_SIZE + inset
        top = y * self.CELL_SIZE + inset
        self.canvas.create_rectangle(
            left,
            top,
            (x + 1) * self.CELL_SIZE - inset,
            (y + 1) * self.CELL_SIZE - inset,
            fill=color,
            outline="",
        )

    def finish_game(self, message: str) -> None:
        self.running = False
        self.after_id = None
        self.canvas.create_rectangle(
            0,
            self.HEIGHT // 2 - 48,
            self.WIDTH,
            self.HEIGHT // 2 + 48,
            fill="#101820",
            outline="",
        )
        self.canvas.create_text(
            self.WIDTH // 2,
            self.HEIGHT // 2 - 10,
            text=message,
            fill="#f8fafc",
            font=("Helvetica", 26, "bold"),
        )
        self.canvas.create_text(
            self.WIDTH // 2,
            self.HEIGHT // 2 + 24,
            text=f"Pontuação: {self.score}",
            fill="#cbd5e1",
            font=("Helvetica", 14),
        )
        self.hint.pack_forget()
        self.end_buttons.pack(side="right")


def main() -> None:
    root = tk.Tk()
    SnakeGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()
