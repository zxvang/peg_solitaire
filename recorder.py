"""Save a finished game to a text file and replay it step by step.

File format (one event per line, '#' lines are comments):

    MODE Manual
    SIZE 7
    TYPE English
    MOVE 3,1 3,3
    RANDOMIZE 0,2;0,3;2,2
    UNDO
"""

from game import create_game


def _cell_text(cell):
    return f"{cell[0]},{cell[1]}"


def _parse_cell(text):
    row, column = text.split(",")
    return int(row), int(column)


class GameRecorder:
    @staticmethod
    def save(game, path):
        lines = [
            "# Peg Solitaire recording",
            f"MODE {game.MODE}",
            f"SIZE {game.size}",
            f"TYPE {game.board_type}",
        ]
        for event in game.events:
            kind = event[0]
            if kind == "MOVE":
                lines.append(f"MOVE {_cell_text(event[1])} {_cell_text(event[2])}")
            elif kind == "RANDOMIZE":
                lines.append("RANDOMIZE " + ";".join(_cell_text(c) for c in event[1]))
            elif kind == "UNDO":
                lines.append("UNDO")
        with open(path, "w", encoding="utf-8") as handle:
            handle.write("\n".join(lines) + "\n")
        return path

    @staticmethod
    def load(path):
        """Return (mode, size, board_type, events) read from a file."""
        mode, size, board_type, events = "Manual", 7, "English", []
        with open(path, encoding="utf-8") as handle:
            for raw in handle:
                line = raw.strip()
                if not line or line.startswith("#"):
                    continue
                keyword, _, rest = line.partition(" ")
                if keyword == "MODE":
                    mode = rest
                elif keyword == "SIZE":
                    size = int(rest)
                elif keyword == "TYPE":
                    board_type = rest
                elif keyword == "MOVE":
                    source, target = rest.split()
                    events.append(("MOVE", _parse_cell(source), _parse_cell(target)))
                elif keyword == "RANDOMIZE":
                    cells = tuple(_parse_cell(c) for c in rest.split(";") if c)
                    events.append(("RANDOMIZE", cells))
                elif keyword == "UNDO":
                    events.append(("UNDO",))
                else:
                    raise ValueError(f"Unknown line in recording: {line}")
        return mode, size, board_type, events


class GameReplayer:
    """Rebuilds a recorded game and applies one event per step()."""

    def __init__(self, path):
        mode, size, board_type, self.events = GameRecorder.load(path)
        self.game = create_game(mode, size, board_type)
        self.position = 0

    def is_finished(self):
        return self.position >= len(self.events)

    def step(self):
        if self.is_finished():
            return None
        event = self.events[self.position]
        self.position += 1
        if event[0] == "MOVE":
            if not self.game.make_move(event[1], event[2]):
                raise ValueError(f"Recorded move is illegal: {event}")
        elif event[0] == "RANDOMIZE":
            self.game.set_pegs(event[1])
        elif event[0] == "UNDO":
            self.game.undo()
        return event
