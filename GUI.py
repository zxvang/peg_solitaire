import math
import tkinter as tk

from game import PegSolitaireGame

BACKGROUND = "#183b35"
BOARD_COLOR = "#d5b77a"
PEG_COLOR = "#355f50"
SELECTED_COLOR = "#e8c547"
TEXT_COLOR = "#e8eee5"
HEXAGON_HOLE_SPACING = 46


class PegSolitaire:
    def __init__(self, root):
        self.root = root
        self.root.title("Peg Solitaire")
        self.root.configure(bg=BACKGROUND)
        self.root.resizable(False, False)
        self.size_var = tk.StringVar(value="7")
        self.type_var = tk.StringVar(value="English")
        self.game = PegSolitaireGame()
        self.buttons = {}
        self.selected = None
        self.game_started = False

        tk.Label(
            root,
            text="PEG SOLITAIRE",
            bg=BACKGROUND,
            fg=TEXT_COLOR,
            font=("Helvetica", 20, "bold"),
        ).pack(pady=(18, 12))

        options = tk.Frame(root, bg=BACKGROUND)
        options.pack(padx=18, pady=(0, 12))
        tk.Label(options, text="Board size", bg=BACKGROUND, fg=TEXT_COLOR).grid(
            row=0, column=0, padx=(0, 6)
        )
        tk.OptionMenu(
            options,
            self.size_var,
            *(str(size) for size in self.game.BOARD_SIZES),
            command=self.configuration_changed,
        ).grid(row=0, column=1, padx=(0, 16))
        tk.Label(options, text="Board type", bg=BACKGROUND, fg=TEXT_COLOR).grid(
            row=0, column=2, padx=(0, 6)
        )
        tk.OptionMenu(
            options,
            self.type_var,
            *self.game.BOARD_TYPES,
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
        self.undo_button = tk.Button(
            actions,
            text="Undo",
            command=self.undo_move,
            font=("Helvetica", 12),
            state="disabled",
        )
        self.undo_button.grid(row=0, column=1, padx=4)

        self.status_label = tk.Label(
            root,
            text="Choose a board, then start a game.",
            bg=BACKGROUND,
            fg=TEXT_COLOR,
            font=("Helvetica", 11),
        )
        self.status_label.pack(pady=(0, 8))
        self.counter_label = tk.Label(
            root,
            text="Pegs: 0    Moves: 0",
            bg=BACKGROUND,
            fg=TEXT_COLOR,
            font=("Helvetica", 11, "bold"),
        )
        self.counter_label.pack(pady=(0, 10))

        self.board_frame = tk.Frame(root, bg=BACKGROUND)
        self.board_frame.pack(padx=18, pady=(0, 18))

        self.configuration_changed()

    def configuration_changed(self, value=None):
        if value is not None:
            size_options = {str(size) for size in self.game.BOARD_SIZES}
            if value in size_options:
                self.size_var.set(value)
            else:
                self.type_var.set(value)

        size = int(self.size_var.get())
        board_type = self.type_var.get()
        self.game.new_game(size, board_type)
        self.buttons.clear()
        self.selected = None
        self.game_started = False
        self.start_button.configure(text="Start Game")
        self.undo_button.configure(state="disabled")
        self.status_label.configure(text="Choose a board, then start a game.")

        for child in self.board_frame.winfo_children():
            child.destroy()

        if board_type == "Hexagon":
            radius = size // 2
            board_width = 2 * radius * HEXAGON_HOLE_SPACING + 56
            board_height = (
                2 * radius * HEXAGON_HOLE_SPACING * math.sqrt(3) / 2 + 56
            )
            frame_width = math.ceil(board_width)
            frame_height = math.ceil(board_height)
            self.board_frame.pack_propagate(False)
            self.board_frame.configure(
                width=frame_width,
                height=frame_height,
            )
        else:
            self.board_frame.pack_propagate(True)
            self.board_frame.configure(width=1, height=1)

        for row in range(size):
            for column in range(size):
                position = (row, column)
                if position not in self.game.cells:
                    if board_type != "Hexagon":
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
                    font=("Arial", 22, "bold"),
                    text="",
                    disabledforeground=PEG_COLOR,
                    command=lambda cell=position: self.cell_clicked(cell),
                )
                if board_type == "Hexagon":
                    radius = size // 2
                    center_x = frame_width / 2
                    center_y = frame_height / 2
                    axial_row = row - radius
                    axial_column = column - radius
                    x = center_x + HEXAGON_HOLE_SPACING * (
                        axial_column + axial_row / 2
                    )
                    y = center_y + (
                        HEXAGON_HOLE_SPACING
                        * math.sqrt(3)
                        / 2
                        * axial_row
                    )
                    button.place(anchor="center", x=round(x), y=round(y))
                else:
                    button.grid(row=row, column=column, padx=2, pady=2)
                self.buttons[position] = button

        self.refresh()

    def start_game(self):
        size = int(self.size_var.get())
        board_type = self.type_var.get()
        self.game.new_game(size, board_type)
        self.selected = None
        self.game_started = True
        self.start_button.configure(text="New Game")
        self.status_label.configure(text="Select a peg, then select a valid empty hole.")
        self.undo_button.configure(state="disabled")
        self.refresh()

    def cell_clicked(self, position):
        if not self.game_started:
            return

        if position in self.game.pegs:
            self.selected = None if self.selected == position else position
            self.status_label.configure(
                text="Select a destination two holes away." if self.selected else "Select a peg to move."
            )
            self.refresh()
            return

        if self.selected is None:
            self.status_label.configure(text="Select a peg first.")
            return

        source = self.selected
        if not self.game.make_move(source, position):
            self.status_label.configure(text="Invalid move. Choose a hole two spaces away over a peg.")
            return

        self.selected = None

        if self.game.is_game_over():
            if self.game.has_won():
                message = "You win! One peg remains."
            else:
                message = f"No moves left. Game over with {len(self.game.pegs)} pegs."
            self.status_label.configure(text=message)
            self.game_started = False
        else:
            self.status_label.configure(text="Select a peg, then select a valid empty hole.")

        self.refresh()

    def undo_move(self):
        if not self.game.undo():
            return

        self.selected = None
        self.game_started = True
        self.status_label.configure(text="Move undone. Select a peg to move.")
        self.refresh()

    def refresh(self):
        self.counter_label.configure(
            text=f"Pegs: {len(self.game.pegs)}    Moves: {self.game.moves_made}"
        )
        self.undo_button.configure(
            state="normal" if self.game.moves_made else "disabled"
        )
        for position, button in self.buttons.items():
            occupied = position in self.game.pegs
            button.configure(
                text="●" if occupied else "",
                bg=(
                    SELECTED_COLOR
                    if position == self.selected
                    else BOARD_COLOR
                ),
                activebackground=(
                    SELECTED_COLOR
                    if position == self.selected
                    else BOARD_COLOR
                ),
                fg=PEG_COLOR,
                state="normal" if self.game_started else "disabled",
            )


def main():
    root = tk.Tk()
    PegSolitaire(root)
    root.mainloop()


if __name__ == "__main__":
    main()

#test