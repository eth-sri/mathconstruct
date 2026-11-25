from math_construct.problems.templates import TEMPLATES
PROBLEM_TEMPLATE = TEMPLATES["bulgarian/problem_pms_2022_10_p3.py"]

from math_construct.problems.problem import Problem, ProblemConfig, Tag, CheckerTag
import numpy as np
import random


FORMATTING_INSTRUCTIONS = r"""Output the sequences as a list of comma-separated tuples inside of \boxed, e.g. \boxed{[(2, 19), (3, 123)]}."""


def get_solution(N: int) -> list[int]:
    ex = []
    for i in range(1, N+1):
        q = 12*i**2+3*i
        p = (6*q+3+(24*i+3))//2
        ex.append((p, q))
    return ex

class ProblemBulPMS2022P10_3(Problem):
    config = ProblemConfig(
        name=Problem.get_name(__file__),
        statement=PROBLEM_TEMPLATE,
        formatting_instructions=FORMATTING_INSTRUCTIONS,
        parameters=["N"],
        source="Bulgarian Spring National Competition 2022 10-12th Grade P3",
        original_parameters={"N": 20},
        original_solution=get_solution(20),
        problem_url="https://klasirane.com/competitions/PMS/All",
        solution_url="https://klasirane.com/competitions/PMS/All",
        tags=[Tag.NUMBER_THEORY, Tag.FIND_INF, Tag.IS_SIMPLIFIED, Tag.IS_TRANSLATED]
    )
    N: int

    def __init__(self, N: int):
        self.N = N

    def get_problem(self):
        return PROBLEM_TEMPLATE.format(N=self.N)

    def check(self, x: list[tuple[int]]) -> bool:

        if len(x) != self.N:
            return False, f"{self.N} examples expected, received {len(x)}", CheckerTag.INCORRECT_LENGTH
        
        # assert that all pairs are unique
        if len(set([tuple(el) for el in x])) != len(x):
            return False, "All examples should be unique", CheckerTag.INCORRECT_FORMAT
        
        for _, entry in enumerate(x):
            if len(entry) != 2:
                return False, f"Each element of the sequence should be a pair", CheckerTag.INCORRECT_FORMAT
            if any(type(v) != int or v <= 0 for v in entry):
                return False, "p and q must be natural numbers", CheckerTag.INCORRECT_FORMAT
            a1 = entry[0]-3*entry[1]
            a2 = entry[0]*(entry[0] - 1)//2 + 9*entry[1]*(entry[1] - 1)//2 - 3*entry[0]*entry[1]

            if a1 != a2:
                return False, f"Example does not result in $a_1 = a_2$", CheckerTag.INCORRECT_SOLUTION
        return True, "OK", CheckerTag.CORRECT

    @staticmethod
    def generate() -> "ProblemBulPMS2022P10_3":
        N = random.randint(10, 100)
        return ProblemBulPMS2022P10_3(N)

    def get_solution(self):
        return get_solution(self.N)
