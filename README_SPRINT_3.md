CS449 Project Sprint 3

GitHub link: https://github.com/zxvang/peg_solitaire

1. Demonstration

The video (5 minutes max) shows:

(a) A manual game on the English board played until it's over
(b) A manual game on the Hexagon board played until it's over
(c) An automated game played until it's over
(d) A manual game where I randomize the board a few times before it ends
(e) Unit tests for the manual game mode
(f) Unit tests for the automated game mode
2. Summary of Source Code
Source code file name	Production code or test code?	# lines of code
game.py	Production code	270
GUI.py	Production code	487
recorder.py	Production code	98
test_unittest.py	Test code	298
	Total	1153
3. Production Code vs User Stories / Acceptance Criteria
User Story ID	User Story Name
1	Choose a board size and type
2	Choose the game mode of a chosen board (manual/automated)
3	Start a new game of the chosen board size and game mode
4	Make a move in a manual game
5	A manual game is over
6	Make a move in an automated game
7	An automated game is over
8	Randomize the state of the board during a manual game
User Story ID	AC ID	Class Name(s)	Method Name(s)	Status	Notes
1	1.1	PegSolitaire (GUI.py); PegSolitaireGame (game.py)	configuration_changed, draw_board; playable_cells, new_game	Complete	Size menu offers 5, 7, 9 and redraws the board on a Tkinter canvas
	1.2	PegSolitaire; PegSolitaireGame	configuration_changed, draw_board; playable_cells, MOVE_DIRECTIONS	Complete	English, Hexagon, Diamond, European shapes
2	2.1	PegSolitaire; ManualGame; create_game (game.py)	configuration_changed, create_game	Complete	Manual radio button builds a ManualGame
	2.2	PegSolitaire; AutomatedGame; create_game	configuration_changed, create_game	Complete	Automated radio button builds an AutomatedGame
3	3.1	PegSolitaire; PegSolitaireGame	start_game, refresh; new_game	Complete	Full board, center empty, counters reset
	3.2	PegSolitaire	start_game, cancel_pending	Complete	New Game restarts and stops any running automated game or replay
4	4.1	PegSolitaire; PegSolitaireGame	cell_clicked, refresh; is_legal_move, make_move	Complete	Board and peg/move counters update
	4.2	PegSolitaire; PegSolitaireGame	cell_clicked; is_legal_move	Complete	Illegal jump shows a message, board unchanged
5	5.1	PegSolitaire; PegSolitaireGame	finish_game; is_game_over, has_won	Complete	Win message when one peg remains
	5.2	PegSolitaire; PegSolitaireGame	finish_game; is_game_over, legal_moves	Complete	Game over message with pegs left
6	6.1	AutomatedGame; PegSolitaire	choose_move, make_automated_move; automated_step	Complete	Computer picks a random legal jump every 0.5 s
	6.2	PegSolitaire; PegSolitaireGame	cell_clicked, refresh, undo_move; PLAYER_CONTROLLED	Complete	Board clicks, Undo and Randomize are disabled while the computer plays
7	7.1	AutomatedGame; PegSolitaire	make_automated_move, play_to_end; automated_step, finish_game	Complete	Stops when no legal moves remain and shows the result
8	8.1	ManualGame; PegSolitaire	randomize, set_pegs; randomize_board	Complete	Same peg count, pegs only on playable holes, tries up to 200 layouts to leave a legal jump
	8.2	ManualGame; PegSolitaireGame	randomize, set_pegs, undo	Complete	Randomize is not counted as a move and can be undone
Extra	Record / replay	GameRecorder, GameReplayer (recorder.py); PegSolitaire	save, load, step; finish_game, replay_game, replay_step	Complete	Record game checkbox saves to recordings/*.txt; Replay plays a file back
4. Tests vs User Stories / Acceptance Criteria
4.1 Automated tests directly corresponding to acceptance criteria

All 31 unit tests pass (./.venv/bin/python test_unittest.py).

User Story ID	AC ID	Test Class	Test Method(s)	Status
1	1.1	TestBoardSetup	test_supported_sizes_are_odd, test_rejects_even_sizes_and_unknown_board_types	Pass
	1.2	TestBoardSetup	test_board_shapes_are_centered_and_symmetric, test_hexagon_rows_shrink_symmetrically_at_the_edges	Pass
2	2.1	TestGameModes	test_create_game_returns_the_chosen_mode, test_both_modes_share_the_base_rules	Pass
	2.2	TestGameModes	test_create_game_returns_the_chosen_mode, test_rejects_unknown_mode	Pass
3	3.1	TestBoardSetup	test_new_game_starts_with_only_the_center_empty	Pass
	3.2	TestPegSolitaireGame	test_new_game_resets_board_and_move_count	Pass
4	4.1	TestManualGame; TestPegSolitaireGame	test_player_move_updates_board_and_counter; test_legal_move_changes_board_and_counts_move	Pass
	4.2	TestManualGame; TestPegSolitaireGame	test_illegal_player_move_is_rejected; test_invalid_move_does_not_change_game_state	Pass
5	5.1	TestManualGame	test_manual_game_over_with_win	Pass
	5.2	TestManualGame	test_manual_game_over_with_loss	Pass
6	6.1	TestAutomatedGame	test_automated_move_is_legal_and_updates_board	Pass
	6.2	TestGameModes	test_both_modes_share_the_base_rules (PLAYER_CONTROLLED flag)	Pass
7	7.1	TestAutomatedGame	test_automated_game_plays_until_over, test_no_automated_move_once_game_is_over, test_automated_game_works_on_every_board_type	Pass
8	8.1	TestManualGame	test_randomize_keeps_peg_count_and_stays_on_board, test_randomize_leaves_a_playable_board	Pass
	8.2	TestManualGame	test_randomize_does_not_count_as_a_move_and_can_be_undone	Pass
4.2 Manual tests directly corresponding to acceptance criteria
User Story ID	AC ID	Test Case Input	Test Oracle (Expected Output)	Notes
1	1.1	Pick size 9 in the Board size menu	Board redraws at 9 x 9 with the center hole empty	GUI layout
	1.2	Pick Hexagon in the Board type menu	Hexagon board is drawn with offset rows	GUI layout
2	2.1	Select Manual, click Start Game	Pegs are clickable and Randomize is enabled; Undo is enabled after a move or randomize	
	2.2	Select Automated, click Start Game	Computer starts moving; pegs, Undo and Randomize are disabled	
3	3.2	Click New Game in the middle of an automated game	Automated moves stop and a fresh board appears	
4	4.1	Manual English 7: click peg (3,1), then hole (3,3)	Pegs: 31, Moves: 1, middle peg removed	
5	5.1 / 5.2	Play a manual game until no jumps remain	Status shows win (1 peg) or game over with the peg count	Shown in video for English and Hexagon
6	6.2	Click pegs while the computer is playing	Nothing happens	
7	7.1	Let an automated game run to the end	Status shows game over and the final peg count	Shown in video
8	8.1	Click Randomize during a manual game	Pegs move to random holes, peg count unchanged	Shown in video
Extra	Record / replay	Tick Record game, finish a game, then click Replay and choose the saved file	Game plays back move by move and ends on the same board	
4.3 Other tests not corresponding to acceptance criteria
#	Test Input	Expected Result	Test Class	Test Method
1	Undo after one move	Previous board and move count restored; second undo returns False	TestPegSolitaireGame	test_undo_restores_previous_board_and_move_count
2	Hexagon diagonal jump (1,5) to (3,3)	Move allowed, middle peg removed	TestPegSolitaireGame	test_hexagon_allows_diagonal_axial_jump
3	Fresh English board	Legal moves exist, game not over, not won	TestPegSolitaireGame	test_reports_available_moves_and_game_not_over
4	Manual game with a move, a randomize and another move saved to a file	Replay ends on the same pegs and move count	TestRecordAndReplay	test_recorded_manual_game_replays_to_same_board
5	Automated 9 Hexagon game saved to a file	File header has mode/size/type; replay ends on the same board	TestRecordAndReplay	test_recorded_automated_game_replays_to_same_board
6	Recording file with an illegal move	Replay raises ValueError	TestRecordAndReplay	test_replay_rejects_illegal_recorded_move
7	Try to assign pegs or moves_made from outside, or add to pegs	AttributeError each time; peg_count and is_occupied report the board	TestPegSolitaireGame	test_game_state_is_read_only_from_outside
5. Design
Part 1: How the class hierarchy handles Manual vs Automated games

My design puts everything both modes have in common into one base class, PegSolitaireGame, in game.py. That class owns the board: which holes exist for each size and type (playable_cells), where the pegs are, the move counter, and the undo history. It also owns every rule of the game: is_legal_move, legal_moves, make_move, undo, has_legal_moves, is_game_over and has_won. A jump is a jump no matter who chooses it, so neither mode re-implements any of this. Both modes also share the event log (events) that the recorder writes to a file, which is why recording works the same way for a manual or an automated game.

The two modes only differ in who picks the move, so each subclass adds just that part. ManualGame is the mode where the person clicks. It adds randomize(), because the requirement to scramble the board only applies to a manual game. Randomize keeps the same number of pegs, places them on random playable holes, and tries again if the new layout has no legal jump so the game does not end on the spot. It uses the base class method set_pegs(), which saves the old layout to the undo history, so a randomize can be undone like a move. AutomatedGame is the mode where the computer plays. It adds choose_move() (pick a random legal jump), make_automated_move() (make one jump, or return None when the game is over) and play_to_end(). Both subclasses take an optional random number generator so the unit tests can use a fixed seed and get the same game every run.

Each subclass also sets two class attributes: MODE ("Manual" or "Automated") and PLAYER_CONTROLLED (True or False). A small factory function, create_game(mode, size, board_type), turns the mode chosen in the GUI into the right object. This keeps the GUI from needing if/else branches on mode names. The GUI draws the board on a Tkinter canvas (hexagon tiles for the Hexagon board, squares for the others) and only reads the game's state to draw it. It asks the game object PLAYER_CONTROLLED to decide whether board clicks, Undo and Randomize are allowed, and for an automated game it calls make_automated_move() on a timer until it returns None. When the game ends, both modes go through the same finish_game() method, which shows win or loss and saves the recording.

Recording and replay live in their own module, recorder.py. GameRecorder turns a game's event log into a plain text file and reads it back, and GameReplayer rebuilds the right game type with create_game() and applies one event per step. Because the replayer only calls base class methods (make_move, set_pegs, undo), it does not care which mode produced the file. If a new mode were added later, such as a smarter computer player, it would only need a new subclass that overrides choose_move(); the rules, the GUI's end-of-game handling and record/replay would all keep working without changes.

PegSolitaireGame  (board, rules, undo, event log)
├── ManualGame      (+ randomize, PLAYER_CONTROLLED = True)
└── AutomatedGame   (+ choose_move, make_automated_move, play_to_end, PLAYER_CONTROLLED = False)

create_game(mode, size, type)  ->  ManualGame | AutomatedGame
GameRecorder / GameReplayer    ->  use PegSolitaireGame methods only
Part 2: Using an LLM to check design principles

Prompt used:

Here are three Python files for a peg solitaire game: game.py, GUI.py and recorder.py. Using these definitions from my software engineering class, rate how well the code follows each principle and point to specific classes or methods:
- Modularity: the degree to which the components of a system are separate
- Cohesion: the degree to which the elements inside a module belong together
- Coupling: degree of interdependence between modules
- Encapsulation: bundling of data with the methods that operate on that data in one module

[Insert screenshots of the prompt and response here]

Interpreting the feedback

I gave the LLM all three source files along with the definitions of modularity, cohesion, coupling and encapsulation from class, and asked it to rate each one and point to specific classes and methods. It rated the project about 8 out of 10 overall: modularity 9, cohesion 8, coupling 7 and encapsulation 7.

Modularity scored highest because the program is split into three files with separate jobs. game.py holds the rules, GUI.py handles the window and clicks, and recorder.py saves and replays games. The LLM pointed out that PegSolitaireGame.make_move() works without Tkinter, and the GUI's cell_clicked() just calls it. Cohesion was also strong in game.py, since is_legal_move(), make_move(), undo() and has_won() all deal with the rules and the board. Its main criticism was the PegSolitaire class in GUI.py, which draws the board, handles clicks, runs the automated timer, saves recordings and controls replay. I agree with this. All of those are tied to running the interface, but it is the biggest class in the project and the one that would be hardest to change.

The two lower scores were connected. For coupling, the LLM noted that the dependencies only go one way (GUI.py and recorder.py import game.py, but game.py imports neither), which is good. The problem was that PegSolitaire.refresh() read self.game.pegs and self.game.moves_made directly, so the GUI depended on how the game stores its data. For encapsulation, it said that pegs and moves_made were public and could be changed from outside the class. Its example was ManualGame.randomize(), which built a temporary game object and assigned trial.pegs = candidate, skipping the checks in set_pegs(). That was a fair catch that I had missed. It also mentioned PLAYER_CONTROLLED, but that is a constant set by each subclass rather than game state, so I left it as is.

Changes made based on the analysis

I followed its suggestion to add read-only properties. In PegSolitaireGame the board data is now stored in the private attributes _pegs and _moves_made. Outside code reads it through a pegs property that returns a frozenset, a moves_made property, a new peg_count property and a new is_occupied(position) method. Trying to assign pegs or moves_made, or to add to the set that pegs returns, now raises an error. The only way to change the board is through make_move(), undo() or set_pegs(), which also keep the undo history and recording log correct.

I rewrote randomize() so it no longer creates a temporary game and overwrites its pegs. Instead it calls a private helper, _legal_moves_for(layout), which checks whether a possible layout has a legal jump without changing any game object. The GUI now uses is_occupied() and peg_count instead of reading the set itself. The unit tests that used to assign game.pegs directly now use set_pegs(), and I added test_game_state_is_read_only_from_outside to check that the data cannot be changed from outside. All 31 tests pass.

These changes improve encapsulation because the game class now controls every change to its own data. They also lower coupling, since the GUI depends on a few small methods instead of on the internal set. If I change how the board is stored later, only game.py needs to change. The one point I did not change is splitting the GUI class, because that would be a bigger refactor. If I did, I would move the automated timer and replay control into a separate controller class.