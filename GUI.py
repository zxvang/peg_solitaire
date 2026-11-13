import math
import os
import tkinter as tk
from datetime import datetime
from tkinter import filedialog

from game import create_game
from recorder import GameRecorder, GameReplayer

BACKGROUND = "#183b35"
BOARD_COLOR = "#d5b77a"
BOARD_EDGE_COLOR = "#b49a64"
PEG_COLOR = "#355f50"
HOLE_COLOR = "#183b35"
SELECTED_COLOR = "#e8c547"
TEXT_COLOR = "#e8eee5"
HEXAGON_HOLE_SPACING = 56
GRID_HOLE_SPACING = 48
AUTO_MOVE_DELAY_MS = 500
REPLAY_DELAY_MS = 600
RECORDINGS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "recordings")


class PegSolitaire:
    def __init__(self, root):
        self.root = root
        self.root.title("Peg Solitaire")
        self.root.configure(bg=BACKGROUND)
        self.root.resizable(False, False)
        self.size_var = tk.StringVar(value="7")
        self.type_var = tk.StringVar(value="English")
        self.mode_var = tk.StringVar(value="Manual")
        self.record_var = tk.BooleanVar(value=False)
        self.game = create_game("Manual")
        self.board_canvas = None
        self.cell_items = {}
        self.selected = None
        self.game_started = False
        self.pending_job = None
        self.replayer = None

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

        modes = tk.Frame(root, bg=BACKGROUND)
        modes.pack(pady=(0, 12))
        tk.Label(modes, text="Game mode", bg=BACKGROUND, fg=TEXT_COLOR).grid(
            row=0, column=0, padx=(0, 6)
        )
        for column, mode in enumerate(("Manual", "Automated"), start=1):
            tk.Radiobutton(
                modes,
                text=mode,
                value=mode,
                variable=self.mode_var,
                command=self.configuration_changed,
                bg=BACKGROUND,
                fg=TEXT_COLOR,
                selectcolor=BACKGROUND,
                activebackground=BACKGROUND,
                activeforeground=TEXT_COLOR,
            ).grid(row=0, column=column, padx=4)
        tk.Checkbutton(
            modes,
            text="Record game",
            variable=self.record_var,
            bg=BACKGROUND,
            fg=TEXT_COLOR,
            selectcolor=BACKGROUND,
            activebackground=BACKGROUND,
            activeforeground=TEXT_COLOR,
        ).grid(row=0, column=3, padx=(16, 0))

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
        self.randomize_button = tk.Button(
            actions,
            text="Randomize",
            command=self.randomize_board,
            font=("Helvetica", 12),
            state="disabled",
        )
        self.randomize_button.grid(row=0, column=2, padx=4)
        self.replay_button = tk.Button(
            actions,
            text="Replay",
            command=self.replay_game,
            font=("Helvetica", 12),
        )
        self.replay_button.grid(row=0, column=3, padx=4)

        self.status_label = tk.Label(
            root,
            text="Choose a board, then start a game.",
            bg=BACKGROUND,
            fg=TEXT_COLOR,
            font=("Helvetica", 11),
            wraplength=420,
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

        self.cancel_pending()
        self.replayer = None
        size = int(self.size_var.get())
        board_type = self.type_var.get()
        self.game = create_game(self.mode_var.get(), size, board_type)
        self.selected = None
        self.game_started = False
        self.start_button.configure(text="Start Game")
        self.status_label.configure(text="Choose a board, then start a game.")
        self.draw_board()

    def draw_board(self):
        size = self.game.size
        board_type = self.game.board_type
        self.board_canvas = None
        self.cell_items.clear()

        for child in self.board_frame.winfo_children():
            child.destroy()

        radius = size // 2
        margin = 16
        if board_type == "Hexagon":
            spacing = HEXAGON_HOLE_SPACING
            hex_radius = spacing / math.sqrt(3)
            frame_width = math.ceil(
                2 * radius * spacing + 2 * hex_radius + 2 * margin
            )
            frame_height = math.ceil(
                2 * radius * spacing * math.sqrt(3) / 2
                + 2 * hex_radius
                + 2 * margin
            )
        else:
            spacing = GRID_HOLE_SPACING
            hex_radius = spacing / math.sqrt(3)
            frame_width = size * spacing + 2 * margin
            frame_height = size * spacing + 2 * margin

        self.board_frame.pack_propagate(False)
        self.board_frame.configure(width=frame_width, height=frame_height)
        self.board_canvas = tk.Canvas(
            self.board_frame,
            width=frame_width,
            height=frame_height,
            bg=BACKGROUND,
            bd=0,
            highlightthickness=0,
        )
        self.board_canvas.pack()
        center_x = frame_width / 2
        center_y = frame_height / 2
        hole_radius = 5
        peg_radius = spacing * 0.28

        for position in sorted(self.game.cells):
            row, column = position
            axial_row = row - radius
            axial_column = column - radius
            cell_tag = f"cell_{row}_{column}"
            if board_type == "Hexagon":
                x = center_x + spacing * (
                    axial_column + axial_row / 2
                )
                y = center_y + spacing * math.sqrt(3) / 2 * axial_row
                vertices = []
                for corner in range(6):
                    angle = math.radians(-90 + corner * 60)
                    vertices.extend(
                        (
                            x + hex_radius * math.cos(angle),
                            y + hex_radius * math.sin(angle),
                        )
                    )
                tile = self.board_canvas.create_polygon(
                    *vertices,
                    fill=BOARD_COLOR,
                    outline=BOARD_EDGE_COLOR,
                    width=2,
                    tags=(cell_tag,),
                )
            else:
                x = center_x + spacing * axial_column
                y = center_y + spacing * axial_row
                half_tile = (spacing - 4) / 2
                tile = self.board_canvas.create_rectangle(
                    x - half_tile,
                    y - half_tile,
                    x + half_tile,
                    y + half_tile,
                    fill=BOARD_COLOR,
                    outline=BOARD_EDGE_COLOR,
                    width=1,
                    tags=(cell_tag,),
                )

            hole = self.board_canvas.create_oval(
                x - hole_radius,
                y - hole_radius,
                x + hole_radius,
                y + hole_radius,
                fill=HOLE_COLOR,
                outline=HOLE_COLOR,
                tags=(cell_tag,),
            )
            peg = self.board_canvas.create_oval(
                x - peg_radius,
                y - peg_radius,
                x + peg_radius,
                y + peg_radius,
                fill=PEG_COLOR,
                outline=BACKGROUND,
                width=2,
                state="normal" if self.game.is_occupied(position) else "hidden",
                tags=(cell_tag,),
            )
            self.cell_items[position] = (tile, hole, peg)
            self.board_canvas.tag_bind(
                cell_tag,
                "<Button-1>",
                lambda event, cell=position: self.cell_clicked(cell),
            )

        self.refresh()

    def cancel_pending(self):
        if self.pending_job is not None:
            self.root.after_cancel(self.pending_job)
            self.pending_job = None

    def start_game(self):
        self.cancel_pending()
        self.replayer = None
        size = int(self.size_var.get())
        board_type = self.type_var.get()
        mode = self.mode_var.get()
        if (self.game.MODE, self.game.size, self.game.board_type) != (mode, size, board_type):
            self.game = create_game(mode, size, board_type)
            self.draw_board()
        self.game.new_game(size, board_type)
        self.selected = None
        self.game_started = True
        self.start_button.configure(text="New Game")
        if not self.game.PLAYER_CONTROLLED:
            self.status_label.configure(text="Computer is playing...")
            self.pending_job = self.root.after(AUTO_MOVE_DELAY_MS, self.automated_step)
        else:
            self.status_label.configure(text="Select a peg, then select a valid empty hole.")
        self.refresh()

    def automated_step(self):
        self.pending_job = None
        move = self.game.make_automated_move()
        if move is None or self.game.is_game_over():
            self.finish_game()
        else:
            self.status_label.configure(
                text=f"Computer jumped {move[0]} to {move[1]}."
            )
            self.pending_job = self.root.after(AUTO_MOVE_DELAY_MS, self.automated_step)
        self.refresh()

    def cell_clicked(self, position):
        if not self.game_started or not self.game.PLAYER_CONTROLLED or self.replayer:
            return

        if self.game.is_occupied(position):
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
            self.finish_game()
        else:
            self.status_label.configure(text="Select a peg, then select a valid empty hole.")

        self.refresh()

    def finish_game(self):
        self.game_started = False
        if self.game.has_won():
            message = "Game over: win! One peg remains."
        else:
            message = f"Game over: no moves left with {self.game.peg_count} pegs."
        if self.record_var.get() and self.replayer is None:
            os.makedirs(RECORDINGS_DIR, exist_ok=True)
            stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            base = f"{self.game.MODE.lower()}_{self.game.board_type.lower()}_{stamp}"
            path = os.path.join(RECORDINGS_DIR, base + ".txt")
            copy = 2
            while os.path.exists(path):
                path = os.path.join(RECORDINGS_DIR, f"{base}_{copy}.txt")
                copy += 1
            GameRecorder.save(self.game, path)
            message += f" Saved to recordings/{os.path.basename(path)}"
        self.status_label.configure(text=message)

    def randomize_board(self):
        if not self.game_started or not self.game.PLAYER_CONTROLLED:
            return
        self.game.randomize()
        self.selected = None
        if self.game.is_game_over():
            self.finish_game()
        else:
            self.status_label.configure(text="Board randomized. Keep playing.")
        self.refresh()

    def replay_game(self):
        path = filedialog.askopenfilename(
            title="Choose a recorded game",
            initialdir=RECORDINGS_DIR if os.path.isdir(RECORDINGS_DIR) else None,
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )
        if not path:
            return
        self.start_replay(path)

    def start_replay(self, path):
        self.cancel_pending()
        try:
            replayer = GameReplayer(path)
        except (OSError, ValueError) as error:
            self.status_label.configure(text=f"Could not load recording: {error}")
            return
        self.replayer = replayer
        self.game = replayer.game
        self.size_var.set(str(self.game.size))
        self.type_var.set(self.game.board_type)
        self.mode_var.set(self.game.MODE)
        self.selected = None
        self.game_started = False
        self.start_button.configure(text="Start Game")
        self.draw_board()
        self.status_label.configure(text=f"Replaying {os.path.basename(path)}...")
        self.pending_job = self.root.after(REPLAY_DELAY_MS, self.replay_step)

    def replay_step(self):
        self.pending_job = None
        if self.replayer is None:
            return
        try:
            event = self.replayer.step()
        except ValueError as error:
            self.status_label.configure(text=f"Replay stopped: {error}")
            self.replayer = None
            return
        if event is None:
            self.status_label.configure(
                text=f"Replay finished. Pegs left: {self.game.peg_count}"
            )
            self.replayer = None
        else:
            label = {"MOVE": "Move", "RANDOMIZE": "Randomize", "UNDO": "Undo"}[event[0]]
            self.status_label.configure(
                text=f"Replay step {self.replayer.position}/{len(self.replayer.events)}: {label}"
            )
            self.pending_job = self.root.after(REPLAY_DELAY_MS, self.replay_step)
        self.refresh()

    def undo_move(self):
        if not self.game.PLAYER_CONTROLLED or self.replayer or not self.game.undo():
            return

        self.selected = None
        self.game_started = True
        self.status_label.configure(text="Move undone. Select a peg to move.")
        self.refresh()

    def refresh(self):
        self.counter_label.configure(
            text=f"Pegs: {self.game.peg_count}    Moves: {self.game.moves_made}"
        )
        manual_turn = (
            self.game.PLAYER_CONTROLLED and self.replayer is None
        )
        self.undo_button.configure(
            state="normal" if manual_turn and self.game.can_undo() else "disabled"
        )
        self.randomize_button.configure(
            state="normal" if manual_turn and self.game_started else "disabled"
        )
        if self.board_canvas is not None:
            for position, (tile, hole, peg) in self.cell_items.items():
                self.board_canvas.itemconfigure(
                    tile,
                    fill=(
                        SELECTED_COLOR
                        if position == self.selected
                        else BOARD_COLOR
                    ),
                )
                self.board_canvas.itemconfigure(
                    hole,
                    state="hidden" if self.game.is_occupied(position) else "normal",
                )
                self.board_canvas.itemconfigure(
                    peg,
                    state="normal" if self.game.is_occupied(position) else "hidden",
                )
            return


def main():
    root = tk.Tk()
    PegSolitaire(root)
    root.mainloop()


if __name__ == "__main__":
    main()