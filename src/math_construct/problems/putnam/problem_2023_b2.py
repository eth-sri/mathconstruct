from math_construct.problems.templates import TEMPLATES
PROBLEM_TEMPLATE = TEMPLATES["putnam/problem_2023_b2.py"]

import math
import random
from fractions import Fraction

from math_construct.problems.problem import Problem, ProblemConfig, Tag, CheckerTag
from math_construct.templates import get_list_template


def count_ones(n: int) -> int:
    """Counts ones in binary representation of n."""
    return bin(n).count("1")

def get_solution(k: int) -> list[int]:
    res = []
    for a in range(1, 300):
        for b in range(1, a):
            s = 2**a + 2**b + 1
            if s%2023 == 0:
                res.append(s//2023)
    return res[:k]

class Problem_Putnam2023B2(Problem):
    config = ProblemConfig(
        name=Problem.get_name(__file__),
        statement=PROBLEM_TEMPLATE,
        formatting_instructions=get_list_template(),
        parameters=["m"],
        source="Putnam 2023 B2",
        original_parameters={"m": 1},
        original_solution=get_solution(1),
        tags=[Tag.NUMBER_THEORY, Tag.FIND_MAX_MIN, Tag.IS_GENERALIZED],
        problem_url="https://kskedlaya.org/putnam-archive/2023.pdf",
        solution_url="https://kskedlaya.org/putnam-archive/2023s.pdf",
    )
    m: int

    def __init__(self, m: int):
        self.m = m

    def get_problem(self):
        return PROBLEM_TEMPLATE.format(m=self.m)

    def check(self, x: list[int]) -> tuple[bool, str]:
        if len(x) != self.m:
            return False, f"List of size {len(x)}, should be {self.m}", CheckerTag.INCORRECT_LENGTH
        # uniqueness
        if len(set(x)) != len(x):
            return False, "All elements should be unique", CheckerTag.INCORRECT_FORMAT
        if not all(isinstance(y, int) for y in x):
            return False, "All elements should be integers", CheckerTag.INCORRECT_FORMAT
        if not all(y > 0 for y in x):
            return False, "All elements should be positive", CheckerTag.INCORRECT_FORMAT
        for n in x:
            if count_ones(2023*n) != 3:
                return False, "Not 3 ones in binary representation", CheckerTag.INCORRECT_SOLUTION
        return True, "OK", CheckerTag.CORRECT

    @staticmethod
    def generate() -> "Problem_Putnam2023B2":
        m = random.randint(3, 25)
        return Problem_Putnam2023B2(m)

    def get_solution(self):
        return get_solution(self.m)
