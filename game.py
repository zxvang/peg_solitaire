import random


class PegSolitaireGame:
    """Shared board and rules for every game mode.

    Subclasses (ManualGame, AutomatedGame) add only the behavior that is
    specific to how moves are chosen.
    """

    MODE = "Base"
    PLAYER_CONTROLLED = False
    BOARD_SIZES = (5, 7, 9)
    BOARD_TYPES = ("English", "Hexagon", "Diamond", "European")
    MOVE_DIRECTIONS = {
        "English": ((-2, 0), (2, 0), (0, -2), (0, 2)),
        "European": ((-2, 0), (2, 0), (0, -2), (0, 2)),
        "Diamond": ((-2, 0), (2, 0), (0, -2), (0, 2)),
        "Hexagon": (
            (-2, 0), (2, 0), (0, -2), (0, 2), (-2, 2), (2, -2)
        ),
    }

    def __init__(self, size=7, board_type="English"):
        self.size = size
        self.board_type = board_type
        self.cells = set()
        self._pegs = set()
        self._moves_made = 0
        self._history = []
        self.events = []
        self.new_game(size, board_type)

    @classmethod
    def playable_cells(cls, size, board_type):
        if size not in cls.BOARD_SIZES:
            raise ValueError(f"Unsupported board size: {size}")
        if board_type not in cls.BOARD_TYPES:
            raise ValueError(f"Unsupported board type: {board_type}")

        center = size // 2
        cells = set()
        for row in range(size):
            for column in range(size):
                if board_type == "English":
                    playable = (
                        center - 1 <= row <= center + 1
                        or center - 1 <= column <= center + 1
                    )
                elif board_type == "European":
                    corner_size = center - 1
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
                    playable = (
                        abs(row - center) + abs(column - center) <= center
                    )
                else:
                    axial_row = row - center
                    axial_column = column - center
                    playable = max(
                        abs(axial_row),
                        abs(axial_column),
                        abs(axial_row + axial_column),
                    ) <= center

                if playable:
                    cells.add((row, column))

        return cells

    def new_game(self, size=None, board_type=None):
        size = self.size if size is None else size
        board_type = self.board_type if board_type is None else board_type
        cells = self.playable_cells(size, board_type)

        self.size = size
        self.board_type = board_type
        self.cells = cells
        self._pegs = set(cells)
        self._pegs.remove((size // 2, size // 2))
        self._moves_made = 0
        self._history = []
        self.events = []

    @property
    def pegs(self):
        """Read-only view of the peg positions."""
        return frozenset(self._pegs)

    @property
    def peg_count(self):
        return len(self._pegs)

    @property
    def moves_made(self):
        return self._moves_made

    def is_occupied(self, position):
        return position in self._pegs

    def is_legal_move(self, source, target):
        return self._is_legal_for(self._pegs, source, target)

    def _is_legal_for(self, pegs, source, target):
        if (
            source not in pegs
            or target not in self.cells
            or target in pegs
        ):
            return False

        row_delta = target[0] - source[0]
        column_delta = target[1] - source[1]
        if (row_delta, column_delta) not in self.MOVE_DIRECTIONS[self.board_type]:
            return False

        middle = (
            source[0] + row_delta // 2,
            source[1] + column_delta // 2,
        )
        return middle in pegs

    def legal_moves(self):
        """Return every legal (source, target) jump, in a stable order."""
        return self._legal_moves_for(self._pegs)

    def _legal_moves_for(self, pegs):
        moves = []
        for row, column in sorted(pegs):
            for row_delta, column_delta in self.MOVE_DIRECTIONS[self.board_type]:
                target = (row + row_delta, column + column_delta)
                if self._is_legal_for(pegs, (row, column), target):
                    moves.append(((row, column), target))
        return moves

    def make_move(self, source, target):
        if not self.is_legal_move(source, target):
            return False

        middle = (
            (source[0] + target[0]) // 2,
            (source[1] + target[1]) // 2,
        )
        self._history.append((set(self._pegs), self._moves_made))
        self._pegs.remove(source)
        self._pegs.remove(middle)
        self._pegs.add(target)
        self._moves_made += 1
        self.events.append(("MOVE", source, target))
        return True

    def undo(self):
        if not self._history:
            return False

        self._pegs, self._moves_made = self._history.pop()
        self.events.append(("UNDO",))
        return True

    def can_undo(self):
        return bool(self._history)

    def set_pegs(self, pegs):
        """Replace the peg layout (used by randomize and by replay)."""
        pegs = set(pegs)
        if not pegs.issubset(self.cells):
            raise ValueError("Pegs must be on playable cells")
        self._history.append((set(self._pegs), self._moves_made))
        self._pegs = pegs
        self.events.append(("RANDOMIZE", tuple(sorted(pegs))))

    def has_legal_moves(self):
        return bool(self.legal_moves())

    def is_game_over(self):
        return not self.has_legal_moves()

    def has_won(self):
        return len(self._pegs) == 1 and self.is_game_over()


class ManualGame(PegSolitaireGame):
    """A game where the human player picks every move."""

    MODE = "Manual"
    PLAYER_CONTROLLED = True

    def __init__(self, size=7, board_type="English", rng=None):
        self.rng = rng or random.Random()
        super().__init__(size, board_type)

    def randomize(self, attempts=200):
        """Scatter the current pegs over random holes.

        The number of pegs stays the same, so the player keeps their progress.
        A layout with at least one legal jump is preferred so the game does
        not end immediately. Returns True if the board changed.
        """
        if len(self._pegs) < 2:
            return False

        cells = sorted(self.cells)
        layout = None
        for _ in range(attempts):
            candidate = set(self.rng.sample(cells, len(self._pegs)))
            layout = candidate
            if self._legal_moves_for(candidate):
                break

        self.set_pegs(layout)
        return True


class AutomatedGame(PegSolitaireGame):
    """A game where the computer picks every move."""

    MODE = "Automated"

    def __init__(self, size=7, board_type="English", rng=None):
        self.rng = rng or random.Random()
        super().__init__(size, board_type)

    def choose_move(self):
        moves = self.legal_moves()
        if not moves:
            return None
        return self.rng.choice(moves)

    def make_automated_move(self):
        """Make one computer move. Returns the move made, or None if over."""
        move = self.choose_move()
        if move is None:
            return None
        self.make_move(*move)
        return move

    def play_to_end(self):
        """Keep moving until no legal moves remain. Returns moves made."""
        while self.make_automated_move() is not None:
            pass
        return self._moves_made


GAME_MODES = {
    ManualGame.MODE: ManualGame,
    AutomatedGame.MODE: AutomatedGame,
}


def create_game(mode="Manual", size=7, board_type="English", rng=None):
    if mode not in GAME_MODES:
        raise ValueError(f"Unsupported game mode: {mode}")
    return GAME_MODES[mode](size, board_type, rng=rng)
