from math_construct.problems.templates import TEMPLATES
PROBLEM_TEMPLATE = TEMPLATES["dutch/problem_2014_3.py"]

import math
import random
import sympy
from fractions import Fraction
from math_construct.problems.problem import Problem, ProblemConfig, Tag, CheckerTag
from math_construct.templates import get_matrix_template
import itertools


# Valid tournaments for n = 8..12 (the inductive extension below breaks "exactly one" for n >= 8).
LARGER_SOLUTIONS = {
    8: [[0, 0, 0, 0, 1, 0, 1, 1], [1, 0, 1, 0, 0, 1, 1, 0], [1, 0, 0, 1, 0, 1, 1, 0], [1, 1, 0, 0, 1, 1, 1, 1], [0, 1, 1, 0, 0, 1, 1, 1], [1, 0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 1, 0, 0], [0, 1, 1, 0, 0, 0, 1, 0]],
    9: [[0, 0, 1, 1, 1, 0, 0, 1, 1], [1, 0, 0, 0, 1, 0, 0, 0, 1], [0, 1, 0, 1, 1, 1, 0, 0, 1], [0, 1, 0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 1, 0, 0, 0, 0, 0], [1, 1, 0, 1, 1, 0, 1, 1, 1], [1, 1, 1, 1, 1, 0, 0, 1, 0], [0, 1, 1, 0, 1, 0, 0, 0, 0], [0, 0, 0, 1, 1, 0, 1, 1, 0]],
    10: [[0, 0, 0, 0, 1, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 1, 0, 0, 0, 1], [1, 1, 0, 1, 1, 0, 0, 1, 1, 1], [1, 1, 0, 0, 1, 0, 1, 1, 1, 0], [0, 1, 0, 0, 0, 0, 0, 1, 0, 0], [1, 0, 1, 1, 1, 0, 1, 1, 1, 1], [1, 1, 1, 0, 1, 0, 0, 1, 0, 0], [1, 1, 0, 0, 0, 0, 0, 0, 1, 1], [1, 1, 0, 0, 1, 0, 1, 0, 0, 1], [1, 0, 0, 1, 1, 0, 1, 0, 0, 0]],
    11: [[0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1], [1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1], [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1], [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1], [1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1], [1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1], [1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1], [0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1], [0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1], [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]],
    12: [[0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1], [1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1], [1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1], [1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1], [0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0], [1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1], [0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0], [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1], [1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0], [0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0]],
}


def get_solution(n):
    if n in LARGER_SOLUTIONS:
        return [row[:] for row in LARGER_SOLUTIONS[n]]
    seven_solution = [
            [0, 1, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, 0, 0, 0],
            [1, 0, 0, 0, 1, 0, 1],
            [1, 0, 1, 0, 0, 1, 0],
            [1, 1, 0, 1, 0, 1, 0],
            [1, 1, 1, 0, 0, 0, 1],
            [1, 1, 0, 1, 1, 0, 0],
        ]
    for i in range(8, n + 1):
        wins = [1] * i
        wins[i - 1] = 0
        wins[i - 3] = 0
        for index, row in enumerate(seven_solution):
            row.append(int(index==(i - 3)))
        seven_solution.append(wins)
    return seven_solution
class ProblemDutch20143(Problem):
    config = ProblemConfig(
        name=Problem.get_name(__file__),
        statement=PROBLEM_TEMPLATE,
        formatting_instructions=get_matrix_template("The element in the $i$-th row and $j$-th column should be 1 if team $i$ won against team $j$, and 0 otherwise. The diagonal should be 0."),
        parameters=["n"],
        source="Dutch Math Olympiad Finals 2014 P3",
        original_parameters={"n": 7},
        problem_url="https://wiskundeolympiade.nl/phocadownload/opgaven/finale/2014/ProblemsKlas6.pdf",
        solution_url="https://wiskundeolympiade.nl/files/opgaven/finale/2014/uitwerkingen_en.pdf",
        original_solution=[
            [0, 1, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, 0, 0, 0],
            [1, 0, 0, 0, 1, 0, 1],
            [1, 0, 1, 0, 0, 1, 0],
            [1, 1, 0, 1, 0, 1, 0],
            [1, 1, 1, 0, 0, 0, 1],
            [1, 1, 0, 1, 1, 0, 0],
        ],
        tags=[Tag.IS_ORIGINAL, Tag.COMBINATORICS, Tag.FIND_ANY, Tag.IS_GENERALIZED]
    )
    n: int

    def __init__(self, n: int):
        self.n = n
    def get_problem(self):
        return PROBLEM_TEMPLATE.format(n=self.n)

    def check(self, a: list[list[int]]) -> bool:
        # check validity matrix
        if len(a) != self.n:
            return False, f"The matrix should have {self.n} rows.", CheckerTag.INCORRECT_FORMAT
        for row in a:
            if len(row) != self.n:
                return False, f"The matrix should have {self.n} columns.", CheckerTag.INCORRECT_FORMAT
        for i in (range(self.n)):
            for j in range(i):
                if a[i][j] != 1 - a[j][i]:
                    return False, f"Invalid Matrix at {(i,j)} or {(j,i)}: The game between team {i} and team {j} should have a winner, but entries do not sum to 1.", CheckerTag.INCORRECT_SOLUTION
            if any(v not in (0, 1) for v in a[i]):
                return False, "Entries must be 0 or 1", CheckerTag.INCORRECT_FORMAT
            if a[i][i] != 0:
                return False, f"Invalid Matrix at {(i,i)}: The diagonal should be 0.", CheckerTag.INCORRECT_SOLUTION

        all_scores = [sum(row) for row in a]
        # minimum is unique
        min_score = min(all_scores)
        if all_scores.count(min_score) != 1:
            return False, f"The team with the least points should be unique, but found {all_scores.count(min_score)} team with {min_score} points.", CheckerTag.INCORRECT_SOLUTION
        for index, row in enumerate(a):
            # each team lost exactly one game against a team that got less points in the final ranking
            if sum(row) == min_score:
                continue
            n_lost = sum(1 for i, val in enumerate(row) if i != index and val == 0 and all_scores[i] < sum(row))
            if n_lost != 1:
                return False, f"Team {index} should have lost exactly one game against a team that got less points in the final ranking.", CheckerTag.INCORRECT_SOLUTION
        return True, "OK", CheckerTag.CORRECT

    @staticmethod
    def generate() -> "ProblemDutch20143":
        n = random.randint(7,12)
        return ProblemDutch20143(n)

    def get_solution(self):
        return get_solution(self.n)
