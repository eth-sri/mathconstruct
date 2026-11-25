from math_construct.problems.templates import TEMPLATES
PROBLEM_TEMPLATE = TEMPLATES["dutch/problem_2010_4.py"]

import math
import random
import sympy
from fractions import Fraction
from math_construct.problems.problem import Problem, ProblemConfig, Tag, CheckerTag

import numpy as np  

FORMATTING = r"""Give your solution as a list of fraction pairs within a single $\boxed{}$ environment. For instance, $\boxed{(\frac{1}{2},\frac{3}{4}),(\frac{1}{3},\frac{2}{4})}$"""


def get_solution(m: int, k: int):
    sols = []
    for a in range(1, m + 1):
        for b in range(1, m + 1):
            if not (a == 1 and b == m) and not (a == m and b == 1):
                sols.append((Fraction(m * a - b, m ** 2 - 1), Fraction(m * b - a, m ** 2 - 1)))
                if len(sols) == k:
                    return sols
    return sols

class ProblemDutch20104(Problem):
    config = ProblemConfig(
        name=Problem.get_name(__file__),
        statement=PROBLEM_TEMPLATE,
        formatting_instructions=FORMATTING,
        parameters=["k", "m"],
        source="Dutch Math Olympiad Finals 2010 P4",
        problem_url="https://wiskundeolympiade.nl/files/opgaven/finale/2010/opgaven_en.pdf",
        solution_url="https://wiskundeolympiade.nl/files/opgaven/finale/2010/uitwerkingen_en.pdf",
        original_parameters={"m": 1000, "k": 10},
        original_solution=get_solution(1000, 10),
        tags=[Tag.IS_GENERALIZED, Tag.NUMBER_THEORY, Tag.FIND_ALL]
    )
    k: int
    m: int

    def __init__(self, k: int, m: int):
        self.k = k
        self.m = m

    def get_problem(self):
        return PROBLEM_TEMPLATE.format(k=self.k, m=self.m)
    
    def is_almost_int(self, x):
        return abs(x - round(x)) < 1e-8

    def check(self, a: list[list[Fraction]]) -> bool:
        checker_format = self.check_format(a, expected_length=self.k, is_unique=True, min_val_exclusive=0, max_val_exclusive=1)
        if not checker_format[0]:
            return checker_format
        solutions = list(set([tuple(x) for x in a]))
        for solution in solutions:
            # with 0 < x, y < 1 both sums are positive, so the integers must be at least 1
            if round(solution[0] + self.m * solution[1]) < 1 or round(self.m * solution[0] + solution[1]) < 1:
                return False, f"The pair {solution} does not give positive integers.", CheckerTag.INCORRECT_SOLUTION
            if not self.is_almost_int(solution[0] + self.m * solution[1]):
                return False, f"The pair {solution} does not satisfy the first condition.", CheckerTag.INCORRECT_SOLUTION
            if not self.is_almost_int(self.m * solution[0] + solution[1]):
                return False, f"The pair {solution} does not satisfy the second condition.", CheckerTag.INCORRECT_SOLUTION
        return True, "OK", CheckerTag.CORRECT

    @classmethod
    def generate_multiple_explicit(cls, n_problems: int = None) -> list["Problem"]:
        # not used in avg plot
        small = np.linspace(1, 10, 5).astype(int).tolist()
        mid = np.linspace(12, 30, 10).astype(int).tolist()
        big = np.linspace(35, 120, 9).astype(int).tolist() 
        m = 1000
        return [cls(k, m) for k in small + mid + big]

    @staticmethod
    def generate() -> "ProblemDutch20104":
        m = random.randint(1000, 30000)
        k = random.randint(10, 30)
        return ProblemDutch20104(k, m)
    
    def get_solution(self):
        return get_solution(self.m, self.k)
