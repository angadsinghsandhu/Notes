"""Bind wine parity to the unfinished question; complete TODOs in test memory only."""
import ast
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_exercise_answer as answer
from check_polars import cell_source, read_source


class WineQuestionTest(answer.WineAnswerTest):
    PATH = answer.BASE + 'exercise-question.ipynb'
    HASH = 'c7a0678291954ef19b53699d3ab5e863b09f2c949b8d655f40acba6fe33ced8b'

    def codes(self, source, converted):
        # This question's exact cell list and completions; never modify archive TODOs.
        cells = {i: cell_source(source, i) for i in (6, 7, 8, 9, 11, 12, 15, 17, 18, 20,
                                                    22, 23, 25, 29, 30, 32, 33)}
        completions = {
            6: ['0'], 8: ['1'], 17: ['4', '8'],
            22: (['range(df.height), test_size=0.2', 'range(train.height), test_size=0.2'] if converted
                 else ['df, test_size=0.2', 'train, test_size=0.2']),
            30: ['train', 'val', 'test'], 33: ['train', 'val', 'test'],
        }
        for i, values in completions.items():
            self.assertEqual(cells[i].count('# YOUR CODE HERE'), len(values), f'question TODO cell {i}')
            for value in values:
                cells[i] = cells[i].replace('# YOUR CODE HERE', value, 1)
            self.assertNotIn('# YOUR CODE HERE', cells[i])
            ast.parse(cells[i])
        return cells

    def test_question_original_and_converted_completion_remains_test_memory_only(self):
        source, old = read_source(self.PATH), read_source(self.PATH, original=True)
        for i, count in ((6, 1), (8, 1), (17, 2), (22, 2), (30, 3), (33, 3),
                         (35, 2), (37, 3), (39, 4), (41, 4)):
            self.assertEqual(cell_source(source, i).count('# YOUR CODE HERE'), count)
            self.assertEqual(cell_source(old, i).count('# YOUR CODE HERE'), count)
        before = source
        self.codes(old, False)
        self.codes(source, True)
        self.assertEqual(read_source(self.PATH), before)
        # These invalid teaching cells remain intentionally incomplete, including models.
        for i in (6, 8, 17, 22, 30, 33, 35, 37, 39, 41):
            with self.assertRaises(SyntaxError): ast.parse(cell_source(source, i))


if __name__ == '__main__':
    unittest.main()
