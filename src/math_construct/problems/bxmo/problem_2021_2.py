from math_construct.problems.templates import TEMPLATES
PROBLEM_TEMPLATE = TEMPLATES["bxmo/problem_2021_2.py"]

import math
import random
import sympy
from fractions import Fraction
from math_construct.problems.problem import Problem, ProblemConfig, Tag, CheckerTag
from math_construct.templates import get_matrix_template
import itertools


def get_solution(n):
    a = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        a[i][i] = 1
    for j in range(n // 2):
        a[j][n - 1 - j] = 1
    return a

class ProblemBxMO20212(Problem):
    config = ProblemConfig(
        name=Problem.get_name(__file__),
        statement=PROBLEM_TEMPLATE,
        formatting_instructions=get_matrix_template("If a square contains a pebble, write 1, otherwise write 0."),
        parameters=["threen_1", "n"],
        source="BxMO 2021 P2",
        problem_url="http://bxmo.org/problems/bxmo-problems-2021-zz.pdf",
        solution_url="http://bxmo.org/problems/bxmo-problems-2021-zz.pdf",
        original_parameters={"n": 7, "threen_1": 10},
        original_solution=get_solution(7),
        tags=[Tag.IS_SIMPLIFIED, Tag.FIND_ANY, Tag.COMBINATORICS, Tag.IS_GENERALIZED]
    )
    threen_1: int
    n: int

    def __init__(self, threen_1: int, n: int):
        self.threen_1 = threen_1
        self.n = n

    def get_problem(self):
        return PROBLEM_TEMPLATE.format(threen_1=self.threen_1, n=self.n)
        
    def check(self, a: list[list[int]]) -> bool:
        # check matrix is correct
        checker_format = self.check_format(a, is_integer=True, is_square_matrix=True, expected_length=self.n, min_val_inclusive=0, max_val_inclusive=1)
        if not checker_format[0]:
            return checker_format
        sum_pebbles = sum([sum(row) for row in a])
        if sum_pebbles != self.threen_1:
            return False, f"There should be {self.threen_1} pebbles.", CheckerTag.INCORRECT_SOLUTION
        pebble_sets = []
        for i in range(self.n):
            for j in range(self.n):
                pebble_set = [
                    (k,i) for k in range(self.n) if a[k][i] == 1
                ] + [
                    (j,k) for k in range(self.n) if a[j][k] == 1
                ]
                if set(pebble_set) in pebble_sets:
                    return False, f"Square {(i,j)} has the same pebble set as another: {pebble_set}", CheckerTag.INCORRECT_SOLUTION
                pebble_sets.append(set(pebble_set))
        return True, "OK", CheckerTag.CORRECT

    @staticmethod
    def generate() -> "ProblemBxMO20212":
        N = random.randint(3, 6)
        n = 2 * N + 1
        threen_1 = 3 * N + 1
        return ProblemBxMO20212(threen_1, n)
    
    def get_solution(self):
        return get_solution(self.n)
