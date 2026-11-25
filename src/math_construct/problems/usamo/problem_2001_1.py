from math_construct.problems.templates import TEMPLATES
PROBLEM_TEMPLATE = TEMPLATES["usamo/problem_2001_1.py"]

import random
from math_construct.problems.problem import Problem, ProblemConfig, Tag, CheckerTag
from math_construct.utils import get_latex_array
from math_construct.templates import get_matrix_template


EXTRA_FORMATTING_INSTRUCTIONS = r"""In your solution, each cell should contain a number between 1 and ${n}$ representing the color of the ball.

$${init_grid}$$
"""

ORIGINAL_SOLUTION = [
    [1, 1, 1, 2, 3, 4, 5, 6],
    [2, 7, 12, 7, 8, 9, 10, 11],
    [3, 8, 13, 12, 13, 14, 15, 16],
    [4, 9, 14, 17, 17, 17, 18, 19],
    [5, 10, 15, 18, 20, 22, 20, 21],
    [6, 11, 16, 19, 21, 23, 22, 23]
]    

class Problem15(Problem):
    """2001 USAMO Problem 1"""
    config = ProblemConfig(
        name=Problem.get_name(__file__),
        statement=PROBLEM_TEMPLATE,
        formatting_instructions=get_matrix_template(extra_instructions=EXTRA_FORMATTING_INSTRUCTIONS),
        parameters=["n"],
        source="2001 USAMO Problem 1",
        original_parameters={"n": 23},
        original_solution=ORIGINAL_SOLUTION,
        problem_url="https://artofproblemsolving.com/wiki/index.php/2001_USAMO_Problems/Problem_1",
        solution_url="https://artofproblemsolving.com/wiki/index.php/2001_USAMO_Problems/Problem_1",
        tags=[Tag.COMBINATORICS, Tag.FIND_MAX_MIN, Tag.IS_SIMPLIFIED]
    )
    n: int

    def __init__(self, n: int):
        self.n = n
        self.init_grid = [["o" for _ in range(8)] for _ in range(6)]

    def get_problem(self):
        return PROBLEM_TEMPLATE.format(n=self.n, init_grid=get_latex_array(self.init_grid))
    
    def get_formatting_instructions(self):
        return get_matrix_template(extra_instructions=EXTRA_FORMATTING_INSTRUCTIONS.format(
                                    init_grid=get_latex_array(self.init_grid),
                                    n=self.n
                                    )
                                )

    def check(self, x: list[list[int]]) -> bool:
        if len(x) != 6:
            return False, f"Number of rows is {len(x)}, should be 6", CheckerTag.INCORRECT_LENGTH
        for i in range(6):
            if len(x[i]) != 8:
                return False, f"Row of size {len(x[i])}, should be 8", CheckerTag.INCORRECT_LENGTH
            for j in range(8):
                if not isinstance(x[i][j], int) or x[i][j] < 1 or x[i][j] > self.n:
                    return False, f"Cell ({i}, {j}) has value {x[i][j]}, should be in the range [1, {self.n}]", CheckerTag.INCORRECT_FORMAT
        pairs = set()
        for j in range(8):
            if len(set(x[i][j] for i in range(6))) != 6:
                return False, f"Box {j} has duplicate colors", CheckerTag.INCORRECT_SOLUTION
            for i1 in range(6):
                for i2 in range(i1+1, 6):
                    pairs.add(tuple(sorted((x[i1][j], x[i2][j]))))
        if len(pairs) != 8 * 6 * 5 / 2:
            return False, f"There is a pair of colors that occur together in more than one box", CheckerTag.INCORRECT_SOLUTION
        return True, "OK", CheckerTag.CORRECT
    
    @staticmethod
    def generate() -> "Problem15":
        n = random.randint(23, 27)
        return Problem15(n)

    def get_solution(self):
        return ORIGINAL_SOLUTION
