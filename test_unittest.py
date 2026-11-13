import os
import random
import tempfile
import unittest

from game import AutomatedGame, ManualGame, PegSolitaireGame, create_game
from recorder import GameRecorder, GameReplayer


class TestBoardSetup(unittest.TestCase):
    def test_supported_sizes_are_odd(self):
        self.assertEqual(PegSolitaireGame.BOARD_SIZES, (5, 7, 9))

    def test_board_shapes_are_centered_and_symmetric(self):
        expected_counts = {
            "English": {5: 21, 7: 33, 9: 45},
            "Hexagon": {5: 19, 7: 37, 9: 61},
            "Diamond": {5: 13, 7: 25, 9: 41},
            "European": {5: 21, 7: 37, 9: 57},
        }

        for board_type, sizes in expected_counts.items():
            for size, expected_count in sizes.items():
                with self.subTest(board_type=board_type, size=size):
                    cells = PegSolitaireGame.playable_cells(size, board_type)
                    center = (size // 2, size // 2)

                    self.assertEqual(len(cells), expected_count)
                    self.assertIn(center, cells)
                    self.assertEqual(
                        {(size - 1 - row, size - 1 - column) for row, column in cells},
                        cells,
                    )

    def test_hexagon_rows_shrink_symmetrically_at_the_edges(self):
        expected_row_counts = {
            5: [3, 4, 5, 4, 3],
            7: [4, 5, 6, 7, 6, 5, 4],
            9: [5, 6, 7, 8, 9, 8, 7, 6, 5],
        }

        for size, expected_counts in expected_row_counts.items():
            with self.subTest(size=size):
                cells = PegSolitaireGame.playable_cells(size, "Hexagon")
                row_counts = [
                    sum(row == current_row for row, _ in cells)
                    for current_row in range(size)
                ]
                self.assertEqual(row_counts, expected_counts)

    def test_rejects_even_sizes_and_unknown_board_types(self):
        with self.assertRaises(ValueError):
            PegSolitaireGame(6, "English")
        with self.assertRaises(ValueError):
            PegSolitaireGame(7, "Unknown")

    def test_new_game_starts_with_only_the_center_empty(self):
        for board_type in PegSolitaireGame.BOARD_TYPES:
            with self.subTest(board_type=board_type):
                game = PegSolitaireGame(7, board_type)

                self.assertEqual(len(game.pegs), len(game.cells) - 1)
                self.assertNotIn((3, 3), game.pegs)
                self.assertTrue(game.pegs.issubset(game.cells))


class TestPegSolitaireGame(unittest.TestCase):
    def setUp(self):
        self.game = PegSolitaireGame(7, "English")

    def test_legal_move_changes_board_and_counts_move(self):
        self.assertTrue(self.game.make_move((3, 1), (3, 3)))

        self.assertNotIn((3, 1), self.game.pegs)
        self.assertNotIn((3, 2), self.game.pegs)
        self.assertIn((3, 3), self.game.pegs)
        self.assertEqual(self.game.moves_made, 1)

    def test_invalid_move_does_not_change_game_state(self):
        original_pegs = set(self.game.pegs)

        self.assertFalse(self.game.make_move((3, 1), (3, 5)))

        self.assertEqual(self.game.pegs, original_pegs)
        self.assertEqual(self.game.moves_made, 0)

    def test_undo_restores_previous_board_and_move_count(self):
        self.game.make_move((3, 1), (3, 3))

        self.assertTrue(self.game.undo())

        self.assertEqual(len(self.game.pegs), len(self.game.cells) - 1)
        self.assertNotIn((3, 3), self.game.pegs)
        self.assertEqual(self.game.moves_made, 0)
        self.assertFalse(self.game.undo())

    def test_hexagon_allows_diagonal_axial_jump(self):
        game = PegSolitaireGame(7, "Hexagon")

        self.assertTrue(game.make_move((1, 5), (3, 3)))
        self.assertNotIn((2, 4), game.pegs)
        self.assertIn((3, 3), game.pegs)

    def test_reports_available_moves_and_game_not_over(self):
        self.assertTrue(self.game.has_legal_moves())
        self.assertFalse(self.game.is_game_over())
        self.assertFalse(self.game.has_won())

    def test_reports_win_when_one_peg_remains(self):
        self.game.set_pegs({(3, 3)})

        self.assertFalse(self.game.has_legal_moves())
        self.assertTrue(self.game.is_game_over())
        self.assertTrue(self.game.has_won())

    def test_reports_loss_when_multiple_pegs_remain_without_moves(self):
        self.game.set_pegs({(0, 2), (6, 4)})

        self.assertTrue(self.game.is_game_over())
        self.assertFalse(self.game.has_won())

    def test_game_state_is_read_only_from_outside(self):
        with self.assertRaises(AttributeError):
            self.game.pegs = set()
        with self.assertRaises(AttributeError):
            self.game.moves_made = 5
        with self.assertRaises(AttributeError):
            self.game.pegs.add((0, 0))

        self.assertEqual(self.game.peg_count, 32)
        self.assertTrue(self.game.is_occupied((3, 1)))
        self.assertFalse(self.game.is_occupied((3, 3)))

    def test_new_game_resets_board_and_move_count(self):
        self.game.make_move((3, 1), (3, 3))

        self.game.new_game(5, "Diamond")

        self.assertEqual(self.game.size, 5)
        self.assertEqual(self.game.board_type, "Diamond")
        self.assertEqual(len(self.game.cells), 13)
        self.assertEqual(len(self.game.pegs), 12)
        self.assertEqual(self.game.moves_made, 0)


class TestGameModes(unittest.TestCase):
    def test_create_game_returns_the_chosen_mode(self):
        manual = create_game("Manual", 7, "English")
        automated = create_game("Automated", 9, "Hexagon")

        self.assertIsInstance(manual, ManualGame)
        self.assertIsInstance(automated, AutomatedGame)
        self.assertEqual((automated.size, automated.board_type), (9, "Hexagon"))

    def test_both_modes_share_the_base_rules(self):
        self.assertTrue(issubclass(ManualGame, PegSolitaireGame))
        self.assertTrue(issubclass(AutomatedGame, PegSolitaireGame))
        self.assertTrue(ManualGame.PLAYER_CONTROLLED)
        self.assertFalse(AutomatedGame.PLAYER_CONTROLLED)

    def test_rejects_unknown_mode(self):
        with self.assertRaises(ValueError):
            create_game("Online", 7, "English")


class TestManualGame(unittest.TestCase):
    def setUp(self):
        self.game = ManualGame(7, "English", rng=random.Random(1))

    def test_player_move_updates_board_and_counter(self):
        self.assertTrue(self.game.make_move((3, 1), (3, 3)))

        self.assertEqual(self.game.moves_made, 1)
        self.assertEqual(len(self.game.pegs), 31)

    def test_illegal_player_move_is_rejected(self):
        self.assertFalse(self.game.make_move((0, 2), (0, 3)))
        self.assertEqual(self.game.moves_made, 0)

    def test_manual_game_over_with_win(self):
        self.game.set_pegs({(3, 1), (3, 2)})

        self.assertTrue(self.game.make_move((3, 1), (3, 3)))
        self.assertTrue(self.game.is_game_over())
        self.assertTrue(self.game.has_won())

    def test_manual_game_over_with_loss(self):
        self.game.set_pegs({(0, 2), (6, 4)})

        self.assertTrue(self.game.is_game_over())
        self.assertFalse(self.game.has_won())

    def test_randomize_keeps_peg_count_and_stays_on_board(self):
        self.game.make_move((3, 1), (3, 3))
        before = set(self.game.pegs)

        self.assertTrue(self.game.randomize())

        self.assertEqual(len(self.game.pegs), len(before))
        self.assertTrue(self.game.pegs.issubset(self.game.cells))
        self.assertNotEqual(self.game.pegs, before)

    def test_randomize_leaves_a_playable_board(self):
        for _ in range(20):
            self.game.randomize()
            self.assertTrue(self.game.has_legal_moves())

    def test_randomize_does_not_count_as_a_move_and_can_be_undone(self):
        before = set(self.game.pegs)

        self.game.randomize()
        self.assertEqual(self.game.moves_made, 0)
        self.assertTrue(self.game.undo())
        self.assertEqual(self.game.pegs, before)


class TestAutomatedGame(unittest.TestCase):
    def setUp(self):
        self.game = AutomatedGame(7, "English", rng=random.Random(7))

    def test_automated_move_is_legal_and_updates_board(self):
        legal = self.game.legal_moves()

        move = self.game.make_automated_move()

        self.assertIn(move, legal)
        self.assertEqual(self.game.moves_made, 1)
        self.assertEqual(len(self.game.pegs), 31)

    def test_automated_game_plays_until_over(self):
        moves = self.game.play_to_end()

        self.assertTrue(self.game.is_game_over())
        self.assertEqual(moves, self.game.moves_made)
        self.assertEqual(len(self.game.pegs), 32 - moves)

    def test_no_automated_move_once_game_is_over(self):
        self.game.play_to_end()

        self.assertIsNone(self.game.make_automated_move())

    def test_automated_game_works_on_every_board_type(self):
        for board_type in PegSolitaireGame.BOARD_TYPES:
            with self.subTest(board_type=board_type):
                game = AutomatedGame(7, board_type, rng=random.Random(3))
                game.play_to_end()
                self.assertTrue(game.is_game_over())


class TestRecordAndReplay(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.folder.name, "game.txt")

    def tearDown(self):
        self.folder.cleanup()

    def test_recorded_manual_game_replays_to_same_board(self):
        game = ManualGame(7, "English", rng=random.Random(2))
        game.make_move((3, 1), (3, 3))
        game.randomize()
        game.make_move(*game.legal_moves()[0])
        GameRecorder.save(game, self.path)

        replayer = GameReplayer(self.path)
        while replayer.step() is not None:
            pass

        self.assertIsInstance(replayer.game, ManualGame)
        self.assertEqual(replayer.game.pegs, game.pegs)
        self.assertEqual(replayer.game.moves_made, game.moves_made)

    def test_recorded_automated_game_replays_to_same_board(self):
        game = AutomatedGame(9, "Hexagon", rng=random.Random(5))
        game.play_to_end()
        GameRecorder.save(game, self.path)

        mode, size, board_type, events = GameRecorder.load(self.path)
        self.assertEqual((mode, size, board_type), ("Automated", 9, "Hexagon"))
        self.assertEqual(len(events), game.moves_made)

        replayer = GameReplayer(self.path)
        while replayer.step() is not None:
            pass
        self.assertEqual(replayer.game.pegs, game.pegs)
        self.assertTrue(replayer.game.is_game_over())

    def test_replay_rejects_illegal_recorded_move(self):
        with open(self.path, "w") as handle:
            handle.write("MODE Manual\nSIZE 7\nTYPE English\nMOVE 0,0 0,2\n")

        replayer = GameReplayer(self.path)
        with self.assertRaises(ValueError):
            replayer.step()


if __name__ == "__main__":
    unittest.main(verbosity=2)
