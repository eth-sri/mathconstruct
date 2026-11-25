from math_construct.problems.templates import TEMPLATES
PROBLEM_TEMPLATE = TEMPLATES["swiss/problem_2021_r2_z1.py"]

import random
from math_construct.problems.problem import Problem, ProblemConfig, Tag, CheckerTag
import numpy as np


EXTRA_FORMATTING_INSTRUCTIONS = r"""Output the sequence as a list of integers inside $\boxed{...}$. For example, $\boxed{[1,2,3,4]}$."""

def get_solution(n:int) -> list[int]:
    return [1,2] + [3*2**i for i in range(n-2)]

class ProblemSwiss2021R2Z1(Problem):
    config = ProblemConfig(
        name=Problem.get_name(__file__),
        statement=PROBLEM_TEMPLATE,
        formatting_instructions=EXTRA_FORMATTING_INSTRUCTIONS,
        parameters=["n"],
        source="Swiss MO 2021 Round 2 Z1",
        original_parameters={"n": 25},
        original_solution=get_solution(25),
        problem_url="https://mathematical.olympiad.ch/fileadmin/user_upload/Archiv/Intranet/Olympiads/Mathematics/deploy/exams/2021/SecondRound/MasterSolution/secondRoundSolution2021.pdf",
        solution_url="https://mathematical.olympiad.ch/fileadmin/user_upload/Archiv/Intranet/Olympiads/Mathematics/deploy/exams/2021/SecondRound/MasterSolution/secondRoundSolution2021.pdf",
        tags=[Tag.NUMBER_THEORY, Tag.IS_SIMPLIFIED, Tag.IS_TRANSLATED, Tag.FIND_ANY]
    )

    n: int

    def __init__(self, n):
        self.n = n

    def get_problem(self):
        return PROBLEM_TEMPLATE.format(n=self.n)

    def check(self, x: list[int]) -> bool:
        if len(x) != self.n:
            return False, f"Example should contain {self.n} entries", CheckerTag.INCORRECT_LENGTH
        
        if len(set(x)) != len(x):
            return False, f"Example numbers should be distinct", CheckerTag.INCORRECT_FORMAT
        
        if not all(isinstance(v, int) and v > 0 for v in x):
            return False, "Example numbers should be positive integers", CheckerTag.INCORRECT_FORMAT
        total_sum = sum(x)

        for entry in x:
            if total_sum % entry != 0:
                return False, f"The sum {total_sum} is not divisible by {entry}", CheckerTag.INCORRECT_SOLUTION
        
        return True, "OK", CheckerTag.CORRECT

    @staticmethod
    def generate() -> "ProblemSwiss2021R2Z1":
        N = random.randint(13, 35)
        return ProblemSwiss2021R2Z1(N)

    def get_solution(self):
        return get_solution(self.n)
