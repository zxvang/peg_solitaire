# CS449 Project Sprint 3

GitHub link: https://github.com/zxvang/peg_solitaire

## 1. Demonstration

The video (5 minutes max) shows:

- (a) A manual game on the English board played until it's over
- (b) A manual game on the Hexagon board played until it's over
- (c) An automated game played until it's over
- (d) A manual game where I randomize the board a few times before it ends
- (e) Unit tests for the manual game mode
- (f) Unit tests for the automated game mode
**Panopto Link**: https://umsystem.hosted.panopto.com/Panopto/Pages/Viewer.aspx?id=b8148028-896a-4cca-9430-b50100fc8bae

## 2. Summary of Source Code

| Source code file name | Production code or test code? | # lines of code |
| --- | --- | ---: |
| `game.py` | Production code | 270 |
| `GUI.py` | Production code | 487 |
| `recorder.py` | Production code | 98 |
| `test_unittest.py` | Test code | 298 |
| **Total** |  | **1153** |

## 3. Production Code vs User Stories / Acceptance Criteria

### User Stories

| User Story ID | User Story Name |
| ---: | --- |
| 1 | Choose a board size and type |
| 2 | Choose the game mode of a chosen board (manual/automated) |
| 3 | Start a new game of the chosen board size and game mode |
| 4 | Make a move in a manual game |
| 5 | A manual game is over |
| 6 | Make a move in an automated game |
| 7 | An automated game is over |
| 8 | Randomize the state of the board during a manual game |

### Production implementation coverage

| User Story ID | AC ID | Class Name(s) | Method Name(s) | Status | Notes |
| ---: | --- | --- | --- | --- | --- |
| 1 | 1.1 | PegSolitaire (`GUI.py`); PegSolitaireGame (`game.py`) | `configuration_changed`, `draw_board`; `playable_cells`, `new_game` | Complete | Size menu offers 5, 7, 9 and redraws the board on a Tkinter canvas |
|  | 1.2 | PegSolitaire; PegSolitaireGame | `configuration_changed`, `draw_board`; `playable_cells`, `MOVE_DIRECTIONS` | Complete | English, Hexagon, Diamond, European shapes |
| 2 | 2.1 | PegSolitaire; ManualGame; `create_game` (`game.py`) | `configuration_changed`, `create_game` | Complete | Manual radio button builds a ManualGame |
|  | 2.2 | PegSolitaire; AutomatedGame; `create_game` | `configuration_changed`, `create_game` | Complete | Automated radio button builds an AutomatedGame |
| 3 | 3.1 | PegSolitaire; PegSolitaireGame | `start_game`, `refresh`; `new_game` | Complete | Full board, center empty, counters reset |
|  | 3.2 | PegSolitaire | `start_game`, `cancel_pending` | Complete | New Game restarts and stops any running automated game or replay |
| 4 | 4.1 | PegSolitaire; PegSolitaireGame | `cell_clicked`, `refresh`; `is_legal_move`, `make_move` | Complete | Board and peg/move counters update |
|  | 4.2 | PegSolitaire; PegSolitaireGame | `cell_clicked`; `is_legal_move` | Complete | Illegal jump shows a message, board unchanged |
| 5 | 5.1 | PegSolitaire; PegSolitaireGame | `finish_game`; `is_game_over`, `has_won` | Complete | Win message when one peg remains |
|  | 5.2 | PegSolitaire; PegSolitaireGame | `finish_game`; `is_game_over`, `legal_moves` | Complete | Game over message with pegs left |
| 6 | 6.1 | AutomatedGame; PegSolitaire | `choose_move`, `make_automated_move`; `automated_step` | Complete | Computer picks a random legal jump every 0.5 s |
|  | 6.2 | PegSolitaire; PegSolitaireGame | `cell_clicked`, `refresh`, `undo_move`; `PLAYER_CONTROLLED` | Complete | Board clicks, Undo and Randomize are disabled while the computer plays |
| 7 | 7.1 | AutomatedGame; PegSolitaire | `make_automated_move`, `play_to_end`; `automated_step`, `finish_game` | Complete | Stops when no legal moves remain and shows the result |
| 8 | 8.1 | ManualGame; PegSolitaire | `randomize`, `set_pegs`; `randomize_board` | Complete | Same peg count, pegs only on playable holes, tries up to 200 layouts to leave a legal jump |
|  | 8.2 | ManualGame; PegSolitaireGame | `randomize`, `set_pegs`, `undo` | Complete | Randomize is not counted as a move and can be undone |
| Extra | Record / replay | GameRecorder, GameReplayer (`recorder.py`); PegSolitaire | `save`, `load`, `step`; `finish_game`, `replay_game`, `replay_step` | Complete | Record game checkbox saves to `recordings/*.txt`; Replay plays a file back |

## 4. Tests vs User Stories / Acceptance Criteria

### 4.1 Automated tests directly corresponding to acceptance criteria

All 31 unit tests pass (`./.venv/bin/python test_unittest.py`).

| User Story ID | AC ID | Test Class | Test Method(s) | Status |
| ---: | --- | --- | --- | --- |
| 1 | 1.1 | TestBoardSetup | `test_supported_sizes_are_odd`, `test_rejects_even_sizes_and_unknown_board_types` | Pass |
|  | 1.2 | TestBoardSetup | `test_board_shapes_are_centered_and_symmetric`, `test_hexagon_rows_shrink_symmetrically_at_the_edges` | Pass |
| 2 | 2.1 | TestGameModes | `test_create_game_returns_the_chosen_mode`, `test_both_modes_share_the_base_rules` | Pass |
|  | 2.2 | TestGameModes | `test_create_game_returns_the_chosen_mode`, `test_rejects_unknown_mode` | Pass |
| 3 | 3.1 | TestBoardSetup | `test_new_game_starts_with_only_the_center_empty` | Pass |
|  | 3.2 | TestPegSolitaireGame | `test_new_game_resets_board_and_move_count` | Pass |
| 4 | 4.1 | TestManualGame; TestPegSolitaireGame | `test_player_move_updates_board_and_counter`; `test_legal_move_changes_board_and_counts_move` | Pass |
|  | 4.2 | TestManualGame; TestPegSolitaireGame | `test_illegal_player_move_is_rejected`; `test_invalid_move_does_not_change_game_state` | Pass |
| 5 | 5.1 | TestManualGame | `test_manual_game_over_with_win` | Pass |
|  | 5.2 | TestManualGame | `test_manual_game_over_with_loss` | Pass |
| 6 | 6.1 | TestAutomatedGame | `test_automated_move_is_legal_and_updates_board` | Pass |
|  | 6.2 | TestGameModes | `test_both_modes_share_the_base_rules` (`PLAYER_CONTROLLED` flag) | Pass |
| 7 | 7.1 | TestAutomatedGame | `test_automated_game_plays_until_over`, `test_no_automated_move_once_game_is_over`, `test_automated_game_works_on_every_board_type` | Pass |
| 8 | 8.1 | TestManualGame | `test_randomize_keeps_peg_count_and_stays_on_board`, `test_randomize_leaves_a_playable_board` | Pass |
|  | 8.2 | TestManualGame | `test_randomize_does_not_count_as_a_move_and_can_be_undone` | Pass |

### 4.2 Manual tests directly corresponding to acceptance criteria

| User Story ID | AC ID | Test Case Input | Test Oracle (Expected Output) | Notes |
| ---: | --- | --- | --- | --- |
| 1 | 1.1 | Pick size 9 in the Board size menu | Board redraws at 9 x 9 with the center hole empty | GUI layout |
|  | 1.2 | Pick Hexagon in the Board type menu | Hexagon board is drawn with offset rows | GUI layout |
| 2 | 2.1 | Select Manual, click Start Game | Pegs are clickable and Randomize is enabled; Undo is enabled after a move or randomize |  |
|  | 2.2 | Select Automated, click Start Game | Computer starts moving; pegs, Undo and Randomize are disabled |  |
| 3 | 3.2 | Click New Game in the middle of an automated game | Automated moves stop and a fresh board appears |  |
| 4 | 4.1 | Manual English 7: click peg (3,1), then hole (3,3) | Pegs: 31, Moves: 1, middle peg removed |  |
| 5 | 5.1 / 5.2 | Play a manual game until no jumps remain | Status shows win (1 peg) or game over with the peg count | Shown in video for English and Hexagon |
| 6 | 6.2 | Click pegs while the computer is playing | Nothing happens |  |
| 7 | 7.1 | Let an automated game run to the end | Status shows game over and the final peg count | Shown in video |
| 8 | 8.1 | Click Randomize during a manual game | Pegs move to random holes, peg count unchanged | Shown in video |
| Extra | Record / replay | Tick Record game, finish a game, then click Replay and choose the saved file | Game plays back move by move and ends on the same board |  |

### 4.3 Other tests not corresponding to acceptance criteria

| # | Test Input | Expected Result | Test Class | Test Method |
| ---: | --- | --- | --- | --- |
| 1 | Undo after one move | Previous board and move count restored; second undo returns False | TestPegSolitaireGame | `test_undo_restores_previous_board_and_move_count` |
| 2 | Hexagon diagonal jump (1,5) to (3,3) | Move allowed, middle peg removed | TestPegSolitaireGame | `test_hexagon_allows_diagonal_axial_jump` |
| 3 | Fresh English board | Legal moves exist, game not over, not won | TestPegSolitaireGame | `test_reports_available_moves_and_game_not_over` |
| 4 | Manual game with a move, a randomize and another move saved to a file | Replay ends on the same pegs and move count | TestRecordAndReplay | `test_recorded_manual_game_replays_to_same_board` |
| 5 | Automated 9 Hexagon game saved to a file | File header has mode/size/type; replay ends on the same board | TestRecordAndReplay | `test_recorded_automated_game_replays_to_same_board` |
| 6 | Recording file with an illegal move | Replay raises ValueError | TestRecordAndReplay | `test_replay_rejects_illegal_recorded_move` |
| 7 | Try to assign pegs or `moves_made` from outside, or add to pegs | AttributeError each time; `peg_count` and `is_occupied` report the board | TestPegSolitaireGame | `test_game_state_is_read_only_from_outside` |

## 5. Design

### Part 1: How the class hierarchy handles Manual vs Automated games

The design puts the behavior shared by both modes in the `PegSolitaireGame` base class in `game.py`. It owns the board, move rules, undo history, game-over checks, and event log. `ManualGame` adds board randomization, while `AutomatedGame` adds move selection and methods for playing automatically. Both modes use the same underlying rules.

The `create_game(mode, size, board_type)` factory returns the appropriate game subclass. The GUI displays and controls the game, while `recorder.py` handles saving and replaying events through game methods.

```text
PegSolitaireGame  (board, rules, undo, event log)
├── ManualGame      (+ randomize, PLAYER_CONTROLLED = True)
└── AutomatedGame   (+ choose_move, make_automated_move, play_to_end, PLAYER_CONTROLLED = False)

create_game(mode, size, type)  ->  ManualGame | AutomatedGame
GameRecorder / GameReplayer    ->  use PegSolitaireGame methods only
```

### Part 2: Using an LLM to check design principles

**Prompt used:**

> Here are three Python files for a peg solitaire game: `game.py`, `GUI.py` and `recorder.py`. Using these definitions from my software engineering class, rate how well the code follows each principle and point to specific classes and methods:
> - Modularity: the degree to which the components of a system are separate
> - Cohesion: the degree to which the elements inside a module belong together
> - Coupling: degree of interdependence between modules
> - Encapsulation: bundling of data with the methods that operate on that data in one module

The LLM feedback screenshots are included below.

<img width="785" height="465" alt="ss1" src="https://github.com/user-attachments/assets/63fa1a73-9a83-443e-a521-26dedafcef6c" />

<img width="691" height="244" alt="ss2" src="https://github.com/user-attachments/assets/809f0b51-8ac3-4596-a7a4-9862f455d5f2" />

<img width="769" height="369" alt="ss3" src="https://github.com/user-attachments/assets/00be7123-4ba2-47f7-a965-3d8f42052308" />

<img width="780" height="496" alt="ss 4" src="https://github.com/user-attachments/assets/0d70bbdc-56c2-401a-b98b-d2f6736a80ed" />

<img width="785" height="668" alt="ss5" src="https://github.com/user-attachments/assets/b5ce5ec9-fb83-4f50-9e75-8cde d22734bd" />

<img width="783" height="386" alt="ss6" src="https://github.com/user-attachments/assets/fd34c102-774b-46a3-83b2-936da8cb1c2c" />

<img width="802" height="600" alt="ss7" src="https://github.com/user-attachments/assets/e885939c-0556-4d5c-b918-f2b4a3975f4a" />

<img width="789" height="572" alt="ss8" src="https://github.com/user-attachments/assets/611cdea8-c4bd-4606-8042-41f21873c138" />

<img width="789" height="434" alt="ss9" src="https://github.com/user-attachments/assets/40686ee8-a220-4228-b712-b2f7bbfa3cac" />

### Interpreting the feedback

I gave the LLM the three source files and the class definitions of modularity, cohesion, coupling, and encapsulation, and asked it to rate each principle and identify specific classes and methods. It rated the project about 8 out of 10 overall: modularity 9, cohesion 8, coupling 7, and encapsulation 7.

Modularity scored highest because the program is split into three files with separate responsibilities: `game.py` holds the rules, `GUI.py` handles the window and interactions, and `recorder.py` saves and replays games. Cohesion was also strong in the game module. The main criticism was that the `PegSolitaire` GUI class handles several responsibilities, including drawing, clicks, automated timers, recording, and replay.

The lower coupling and encapsulation scores were related. The GUI directly accessed game state, and the original randomization code bypassed the normal state-management methods. The feedback also noted that `PLAYER_CONTROLLED` is a class-level constant, which is appropriate because it identifies the game mode rather than changing game state.

### Changes made based on the analysis

I added read-only properties to `PegSolitaireGame`. Board data is stored in `_pegs` and `_moves_made`; outside code reads it through properties such as `pegs`, `moves_made`, and `peg_count`, and through `is_occupied(position)`. The board can be changed through game methods, preserving undo history and the event log.

I also rewrote `randomize()` to use a private `_legal_moves_for(layout)` helper rather than creating a temporary game and assigning its pegs directly. The GUI uses `is_occupied()` and `peg_count` rather than reading the peg set itself. The unit tests that previously assigned `game.pegs` now use `set_pegs()`, and an additional test verifies that game state cannot be modified from outside. All 31 tests pass.

These changes improve encapsulation because the game class controls changes to its own data. They also reduce coupling: the GUI relies on the game's public methods instead of its internal representation. Splitting the GUI class into separate controllers for automated play and replay remains a possible larger refactor.
