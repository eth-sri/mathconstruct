from math_construct.problems.templates import TEMPLATES
PROBLEM_TEMPLATE = TEMPLATES["swiss/problem_2024_3.py"]

import math
import random
import sympy
from fractions import Fraction
from math_construct.problems.problem import Problem, ProblemConfig, Tag, CheckerTag
from math_construct.templates import get_list_template
import itertools


class ProblemSwiss20243(Problem):
    config = ProblemConfig(
        name=Problem.get_name(__file__),
        statement=PROBLEM_TEMPLATE,
        formatting_instructions=get_list_template("The numbers should be in the order $a,b,c,d$."),
        parameters=["k", "min_val"],
        source="Swiss Math Olympiad Finals 2024",
        problem_url="https://mathematical.olympiad.ch/fileadmin/user_upload/Archiv/Intranet/Olympiads/Mathematics/deploy/exams/2024/FinalRound/MasterSolution/finalRoundSolution2024.pdf#page=7",
        solution_url="https://mathematical.olympiad.ch/fileadmin/user_upload/Archiv/Intranet/Olympiads/Mathematics/deploy/exams/2024/FinalRound/MasterSolution/finalRoundSolution2024.pdf#page=7",
        original_parameters={"min_val": 24, "k": 5},
        original_solution=[math.sqrt(6), math.sqrt(3), math.sqrt(2), 1],
        tags=[Tag.IS_ORIGINAL, Tag.ALGEBRA, Tag.FIND_ANY, Tag.IS_GENERALIZED]
    )
    k: int
    min_val: int

    def __init__(self, k: int, min_val: int):
        self.k = k
        self.min_val = min_val

    def get_problem(self):
        return PROBLEM_TEMPLATE.format(k=self.k, min_val=self.min_val)
        
    def check(self, a: list[float]) -> bool:
        checker_format = self.check_format(a, expected_length=4, min_val_exclusive=0)
        if not checker_format[0]:
            return checker_format
        a, b, c, d = a
        if a * b ** 2 + a * c ** 2 < self.k * b * c * d - 1e-8 * min(1, self.k * b * c * d):
            return False, f"{a} * {b}^2 + {a} * {c}^2 < {self.k} * {b} * {c} * {d}", CheckerTag.INCORRECT_SOLUTION
        val = (a ** 2 + b ** 2 + c ** 2 + d ** 2) * (1 / a ** 2 + 1 / b ** 2 + 1 / c ** 2 + 1 / d ** 2) 
        if abs(val - self.min_val) > 1e-8:
            return False, f"({a}^2 + {b}^2 + {c}^2 + {d}^2) * (1/{a}^2 + 1/{b}^2 + 1/{c}^2 + 1/{d}^2) != {self.min_val}", CheckerTag.INCORRECT_SOLUTION
        return True, "OK", CheckerTag.CORRECT

    @staticmethod
    def generate() -> "ProblemSwiss20243":
        k = random.randint(5,20)
        min_val = 4 * (k + 1)
        return ProblemSwiss20243(k, min_val)
    
    def get_solution(self):
        D = self.k ** 2 - 4 * (self.k + 1)
        sqrt_D = math.sqrt(D)
        b = math.sqrt((self.k + sqrt_D) / 2)
        return [
            math.sqrt(self.k + 1),
            b,
            math.sqrt(self.k + 1) / b,
            1
        ]
