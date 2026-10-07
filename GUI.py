import tkinter as tk


BOARD_SIZES = tuple(range(3, 11))
BOARD_TYPES = ("English", "European", "Diamond")
BACKGROUND = "#183b35"
BOARD_COLOR = "#d5b77a"



def playable_cells(size, board_type):
    cells = set()
    middle_start = (size - 3) // 2
    middle_end = middle_start + 3
    corner_size = (size - 3) // 2

    for row in range(size):
        for column in range(size):
            if board_type == "English":
                playable = (
                    middle_start <= row < middle_end
                    or middle_start <= column < middle_end
                )
            elif board_type == "European":
                in_corner = (
                    row < corner_size
                    and column < corner_size
                    and row + column < corner_size
                ) or (
                    row < corner_size
                    and column >= size - corner_size
                    and row + size - 1 - column < corner_size
                ) or (
                    row >= size - corner_size
                    and column < corner_size
                    and size - 1 - row + column < corner_size
                ) or (
                    row >= size - corner_size
                    and column >= size - corner_size
                    and size - 1 - row + size - 1 - column < corner_size
                )
                playable = not in_corner
            elif board_type == "Diamond":
                center = (size - 1) / 2
                playable = abs(row - center) + abs(column - center) <= (size - 1) / 2
            else:
                playable = False

            if playable:
                cells.add((row, column))

    return cells


def initial_pegs(cells, board_type, size):
    empty_cell = (size // 2, size // 2) if board_type in {"English", "European", "Diamond"} else (0, 0)
    return set(cells) - {empty_cell}


class PegSolitaire:
    def __init__(self, root):
        self.root = root
        self.root.title("Peg Solitaire")
        self.root.configure(bg=BACKGROUND)
        self.root.resizable(False, False)
        self.size_var = tk.StringVar(value="7")
        self.type_var = tk.StringVar(value="English")
        self.cells = set()
        self.pegs = set()
        self.buttons = {}

        tk.Label(
            root,
            text="PEG SOLITAIRE",
            bg=BACKGROUND,
            fg="#e8eee5",
            font=("Helvetica", 20, "bold"),
        ).pack(pady=(18, 12))

        options = tk.Frame(root, bg=BACKGROUND)
        options.pack(padx=18, pady=(0, 12))
        tk.Label(options, text="Board size", bg=BACKGROUND, fg="#e8eee5").grid(
            row=0, column=0, padx=(0, 6)
        )
        tk.OptionMenu(
            options,
            self.size_var,
            *(str(size) for size in BOARD_SIZES),
            command=self.configuration_changed,
        ).grid(row=0, column=1, padx=(0, 16))
        tk.Label(options, text="Board type", bg=BACKGROUND, fg="#e8eee5").grid(
            row=0, column=2, padx=(0, 6)
        )
        tk.OptionMenu(
            options,
            self.type_var,
            *BOARD_TYPES,
            command=self.configuration_changed,
        ).grid(row=0, column=3)

        actions = tk.Frame(root, bg=BACKGROUND)
        actions.pack(pady=(0, 12))
        self.start_button = tk.Button(
            actions,
            text="Start Game",
            command=self.start_game,
            font=("Helvetica", 12, "bold"),
        )
        self.start_button.grid(row=0, column=0, padx=4)

        self.board_frame = tk.Frame(root, bg=BACKGROUND)
        self.board_frame.pack(padx=18, pady=(0, 18))

        self.configuration_changed()

    def configuration_changed(self, _value=None):
        size = int(self.size_var.get())
        board_type = self.type_var.get()
        self.cells = playable_cells(size, board_type)
        self.buttons.clear()
        self.pegs = set()
        self.start_button.configure(text="Start Game")

        for child in self.board_frame.winfo_children():
            child.destroy()

        for row in range(size):
            for column in range(size):
                position = (row, column)
                if position not in self.cells:
                    tk.Label(
                        self.board_frame,
                        bg=BACKGROUND,
                        width=4,
                        height=2,
                    ).grid(row=row, column=column, padx=2, pady=2)
                    continue

                button = tk.Button(
                    self.board_frame,
                    bg=BOARD_COLOR,
                    activebackground=BOARD_COLOR,
                    relief="flat",
                    bd=0,
                    width=3,
                    height=1,
                    font=("Helvetica", 14, "bold"),
                    text="",
                )
                button.grid(row=row, column=column, padx=2, pady=2)
                self.buttons[position] = button

        self.refresh()

    def start_game(self):
        size = int(self.size_var.get())
        board_type = self.type_var.get()
        self.cells = playable_cells(size, board_type)
        self.pegs = initial_pegs(self.cells, board_type, size)
        self.start_button.configure(text="New Game")
        self.refresh()

    def refresh(self):
        for position, button in self.buttons.items():
            occupied = position in self.pegs
            button.configure(
                text="●" if occupied else "",
                bg=BOARD_COLOR,
                activebackground=BOARD_COLOR,
                state="disabled",
            )


def main():
    root = tk.Tk()
    PegSolitaire(root)
    root.mainloop()


if __name__ == "__main__":
    main()