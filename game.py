class PegSolitaireGame:
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
        self.pegs = set()
        self.moves_made = 0
        self._history = []
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
        self.pegs = set(cells)
        self.pegs.remove((size // 2, size // 2))
        self.moves_made = 0
        self._history = []

    def is_legal_move(self, source, target):
        if (
            source not in self.pegs
            or target not in self.cells
            or target in self.pegs
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
        return middle in self.pegs

    def make_move(self, source, target):
        if not self.is_legal_move(source, target):
            return False

        middle = (
            (source[0] + target[0]) // 2,
            (source[1] + target[1]) // 2,
        )
        self._history.append(set(self.pegs))
        self.pegs.remove(source)
        self.pegs.remove(middle)
        self.pegs.add(target)
        self.moves_made += 1
        return True

    def undo(self):
        if not self._history:
            return False

        self.pegs = self._history.pop()
        self.moves_made -= 1
        return True

    def has_legal_moves(self):
        for row, column in self.pegs:
            for row_delta, column_delta in self.MOVE_DIRECTIONS[self.board_type]:
                target = (row + row_delta, column + column_delta)
                if self.is_legal_move((row, column), target):
                    return True
        return False

    def is_game_over(self):
        return not self.has_legal_moves()

    def has_won(self):
        return len(self.pegs) == 1 and self.is_game_over()
