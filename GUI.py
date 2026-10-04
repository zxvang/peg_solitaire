import tkinter as tk


BOARD_SIZE = 7
BACKGROUND = "#183b35"
HOLE_COLOR = "#d5b77a"
PEG_COLOR = "#e8eee5"
SELECTED_COLOR = "#f0a34a"


def is_playable(row, column):
    return 2 <= row <= 4 or 2 <= column <= 4


def legal_moves(board):
    moves = []
    for row in range(BOARD_SIZE):
        for column in range(BOARD_SIZE):
            if not is_playable(row, column) or not board[row][column]:
                continue
            for row_step, column_step in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                middle_row = row + row_step
                middle_column = column + column_step
                target_row = row + 2 * row_step
                target_column = column + 2 * column_step
                if not (0 <= target_row < BOARD_SIZE and 0 <= target_column < BOARD_SIZE):
                    continue
                if (
                    is_playable(target_row, target_column)
                    and board[middle_row][middle_column]
                    and not board[target_row][target_column]
                ):
                    moves.append(((row, column), (target_row, target_column)))
    return moves


class PegSolitaire:
    def __init__(self, root):
        self.root = root
        self.root.title("Peg Solitaire")
        self.root.configure(bg=BACKGROUND)
        self.root.resizable(False, False)
        self.selected = None
        self.move_count = 0

        tk.Label(
            root,
            text="PEG SOLITAIRE",
            bg=BACKGROUND,
            fg=PEG_COLOR,
            font=("Helvetica", 20, "bold"),
        ).pack(pady=(18, 4))
        self.status = tk.Label(
            root,
            bg=BACKGROUND,
            fg=PEG_COLOR,
            font=("Helvetica", 12),
        )
        self.status.pack(pady=(0, 12))

        self.board_frame = tk.Frame(root, bg=BACKGROUND)
        self.board_frame.pack(padx=18)
        self.cells = {}
        for row in range(BOARD_SIZE):
            for column in range(BOARD_SIZE):
                if not is_playable(row, column):
                    tk.Label(
                        self.board_frame,
                        bg=BACKGROUND,
                        width=6,
                        height=3,
                    ).grid(row=row, column=column)
                    continue
                cell = tk.Button(
                    self.board_frame,
                    command=lambda position=(row, column): self.click_cell(position),
                    relief="flat",
                    bd=0,
                    width=5,
                    height=2,
                    font=("Helvetica", 18, "bold"),
                    activebackground=SELECTED_COLOR,
                )
                cell.grid(row=row, column=column, padx=3, pady=3)
                self.cells[(row, column)] = cell

        tk.Button(
            root,
            text="New Game",
            command=self.reset,
            font=("Helvetica", 12, "bold"),
            padx=14,
            pady=5,
        ).pack(pady=15)
        self.reset()

    def reset(self):
        self.board = [
            [
                is_playable(row, column) and (row, column) != (3, 3)
                for column in range(BOARD_SIZE)
            ]
            for row in range(BOARD_SIZE)
        ]
        self.selected = None
        self.move_count = 0
        self.refresh()

    def click_cell(self, position):
        row, column = position
        if self.selected is None:
            if self.board[row][column]:
                self.selected = position
                self.refresh()
            return

        if position == self.selected:
            self.selected = None
        elif self.board[row][column]:
            self.selected = position
        else:
            source_row, source_column = self.selected
            middle = ((source_row + row) // 2, (source_column + column) // 2)
            if (
                abs(source_row - row) + abs(source_column - column) == 2
                and (source_row == row or source_column == column)
                and self.board[middle[0]][middle[1]]
            ):
                self.board[source_row][source_column] = False
                self.board[middle[0]][middle[1]] = False
                self.board[row][column] = True
                self.move_count += 1
            self.selected = None
        self.refresh()

    def refresh(self):
        remaining = sum(sum(row) for row in self.board)
        for position, cell in self.cells.items():
            row, column = position
            if position == self.selected:
                color = SELECTED_COLOR
            elif self.board[row][column]:
                color = PEG_COLOR
            else:
                color = HOLE_COLOR
            cell.configure(bg=color, text="●" if self.board[row][column] else "")

        self.status.configure(text=f"Pegs: {remaining}    Moves: {self.move_count}")
        if not legal_moves(self.board):
            result = (
                "Excellent! One peg remains."
                if remaining == 1
                else "No moves remain. Start a new game to play again."
            )
            self.status.configure(text=f"Pegs: {remaining}    {result}")


def main():
    root = tk.Tk()
    PegSolitaire(root)
    root.mainloop()


if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()