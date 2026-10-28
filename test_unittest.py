import unittest

from game import PegSolitaireGame


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
        self.game.pegs = {(3, 3)}

        self.assertFalse(self.game.has_legal_moves())
        self.assertTrue(self.game.is_game_over())
        self.assertTrue(self.game.has_won())

    def test_reports_loss_when_multiple_pegs_remain_without_moves(self):
        self.game.pegs = {(0, 0), (6, 6)}

        self.assertTrue(self.game.is_game_over())
        self.assertFalse(self.game.has_won())

    def test_new_game_resets_board_and_move_count(self):
        self.game.make_move((3, 1), (3, 3))

        self.game.new_game(5, "Diamond")

        self.assertEqual(self.game.size, 5)
        self.assertEqual(self.game.board_type, "Diamond")
        self.assertEqual(len(self.game.cells), 13)
        self.assertEqual(len(self.game.pegs), 12)
        self.assertEqual(self.game.moves_made, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
