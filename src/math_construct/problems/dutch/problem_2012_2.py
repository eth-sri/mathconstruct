from math_construct.problems.templates import TEMPLATES
PROBLEM_TEMPLATE = TEMPLATES["dutch/problem_2012_2.py"]

import math
import random
import sympy
from fractions import Fraction
from math_construct.problems.problem import Problem, ProblemConfig, Tag, CheckerTag
from math_construct.templates import get_matrix_template
import itertools


def get_solution(n: int):
    matrix = []
    for i in range(n):
        ints = [k for k in range(1, n + 1)]
        matrix.append(ints[:i][::-1] + ints[::-1][:n - i])
    return matrix

class ProblemDutch20122(Problem):
    config = ProblemConfig(
        name=Problem.get_name(__file__),
        statement=PROBLEM_TEMPLATE,
        formatting_instructions=get_matrix_template(),
        parameters=["n"],
        source="Dutch Math Olympiad Finals 2012 P2",
        problem_url="https://wiskundeolympiade.nl/files/opgaven/finale/2012/opgaven_en.pdf",
        solution_url="https://wiskundeolympiade.nl/files/opgaven/finale/2012/uitwerkingen_en.pdf",
        original_parameters={"n": 5},
        original_solution=get_solution(5),
        tags=[Tag.IS_ORIGINAL, Tag.COMBINATORICS, Tag.FIND_ANY, Tag.IS_GENERALIZED]
    )
    n: int

    def __init__(self, n: int):
        self.n = n

    def get_problem(self):
        return PROBLEM_TEMPLATE.format(n=self.n)

    def check(self, a: list[list[int]]) -> bool:
        check_format = self.check_format(a, is_integer=True, expected_length=self.n, is_square_matrix=True, min_val_inclusive=1, max_val_inclusive=self.n)
        if not check_format[0]:
            return check_format
        # check validity matrix
        for row in a:
            if len(set(row)) != self.n:
                return False, f"The row should contain the numbers 1 to {self.n}, but is not the case for {row}.", CheckerTag.INCORRECT_SOLUTION
        for i in range(self.n):
            column = [a[j][i] for j in range(self.n)]
            if len(set(column)) != self.n:
                return False, f"The column should contain the numbers 1 to {self.n}, but is not the case for {column}.", CheckerTag.INCORRECT_SOLUTION
        blue_cells = [[0 for _ in range(self.n)] for _ in range(self.n)]
        for i in range(self.n):
            for j in range(self.n):
                if a[i][j] > j + 1:
                    blue_cells[i][j] = 1
        row_blue_counts = [sum(row) for row in blue_cells]
        if len(set(row_blue_counts)) != 1:
            return False, f"Each row should contain the same number of blue cells, but found {row_blue_counts}.", CheckerTag.INCORRECT_SOLUTION
        return True, "OK", CheckerTag.CORRECT

    @staticmethod
    def generate() -> "ProblemDutch20122":
        n = 2 * random.randint(2,6) + 1
        return ProblemDutch20122(n)
    
    def get_solution(self):
        return get_solution(self.n)
