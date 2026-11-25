from math_construct.problems.templates import TEMPLATES
PROBLEM_TEMPLATE = TEMPLATES["dutch/problem_2018_2.py"]

import math
import random
import sympy
from fractions import Fraction
from math_construct.problems.problem import Problem, ProblemConfig, Tag, CheckerTag
from math_construct.templates import get_list_template
import itertools


def get_solution(n: int) -> list[list[int]]:
    solutions = []
    for i in range(1, n + 1):
        if n % i == 0:
            solutions.append([l for l in range(1, n + 1) if l % i == 0])
    return solutions

class ProblemDutch20182(Problem):
    config = ProblemConfig(
        name=Problem.get_name(__file__),
        statement=PROBLEM_TEMPLATE,
        formatting_instructions=r"Output a list of comma separated lists inside of $\boxed{...}$. Each list indicates the numbers that are coloured red for that option, all other numbers are coloured blue. For example, $\boxed{(1,2,3),(1,5,7)}$ indicates two solutions where in the first only the numbers 1, 2, and 3 are coloured red. ",
        parameters=["n", "k"],
        source="Dutch Math Olympiad Finals 2018 P2",
        problem_url="https://wiskundeolympiade.nl/phocadownload/opgaven/finale/2018/ProblemsKlas6.pdf",
        solution_url="https://wiskundeolympiade.nl/phocadownload/opgaven/finale/2018/Solutions.pdf",
        original_parameters={"n": 15, "k": 4},
        original_solution=get_solution(15),
        tags=[Tag.IS_ORIGINAL, Tag.IS_GENERALIZED, Tag.FIND_ALL, Tag.NUMBER_THEORY] 
    )
    n: int
    k: int

    def __init__(self, n: int, k: int):
        self.n = n
        self.k = k

    def get_problem(self):
        return PROBLEM_TEMPLATE.format(n=self.n, k=self.k)

    def check(self, a: list[list[int]]) -> bool:
        solutions = [tuple(i) for i in a]
        check_format = self.check_format(solutions, is_integer=True, expected_length=self.k, is_unique=True, min_val_inclusive=1, max_val_inclusive=self.n)
        if not check_format[0]:
            return check_format
        
        if len(set(frozenset(s) for s in solutions)) != len(solutions):
            return False, "Colourings are not distinct", CheckerTag.INCORRECT_FORMAT
        for solution in solutions:
            if self.n not in solution:
                return False, f"{self.n} should be red.", CheckerTag.INCORRECT_SOLUTION
            for x in range(1, self.n + 1):
                for y in range(1, self.n + 1):
                    if x + y <= self.n and x in solution and y not in solution:
                        if x + y in solution:
                            return False, f"{x} and {y} have different colours, but {x + y} is red.", CheckerTag.INCORRECT_SOLUTION
                    if x * y <= self.n and x in solution and y not in solution:
                        if x * y not in solution:
                            return False, f"{x} and {y} have different colours, but {x * y} is blue.", CheckerTag.INCORRECT_SOLUTION
        return True, "OK", CheckerTag.CORRECT

    @staticmethod
    def generate() -> "ProblemDutch20182":
        n = random.randint(20,40)
        max_len = len([i for i in range(1,n+1) if n % i == 0])
        k = random.randint(min(5, max_len), max_len)
        return ProblemDutch20182(n, k)
    
    def get_solution(self) -> list[list[int]]:
        return get_solution(self.n)[:self.k]
