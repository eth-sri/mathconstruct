from math_construct.problems.templates import TEMPLATES
PROBLEM_TEMPLATE = TEMPLATES["jbmo_shortlist/problem_2018_n4.py"]

from math_construct.problems.problem import Problem, ProblemConfig, Tag, CheckerTag
from math_construct.templates import LIST_FORMATTING_TEMPLATE
import random
import numpy as np


def mod_exp(a: int, y: int, p: int) -> int:
    """Computes (a^y) % p using modular exponentiation."""
    result = 1  # Initialize result
    a = a % p   # Reduce a modulo p initially

    while y > 0:
        # If y is odd, multiply the current base with the result
        if y % 2 == 1:
            result = (result * a) % p

        # Square the base and halve the exponent
        a = (a * a) % p
        y //= 2

    return result

def get_solution(N: int) -> list[int]:
    res = []
    for n in range(1, N+1):
        res.append(2**(2**n))
    return res

class ProblemJBMO2018N4(Problem):
    config = ProblemConfig(
        name=Problem.get_name(__file__),
        statement=PROBLEM_TEMPLATE,
        formatting_instructions=LIST_FORMATTING_TEMPLATE,
        parameters=["N"],
        source="JBMO 2018 Shortlist N4",
        original_parameters={"N": 7},
        original_solution=get_solution(7),
        problem_url="https://artofproblemsolving.com/community/c6h1870447p12685788",
        solution_url="https://artofproblemsolving.com/community/c6h1870447p12685788",
        tags=[Tag.FIND_INF, Tag.IS_SIMPLIFIED, Tag.NUMBER_THEORY]
    )
    N: int

    def __init__(self, N: int):
        self.N = N

    def get_problem(self):
        return PROBLEM_TEMPLATE.format(N=self.N)

    def check(self, x: list[int]) -> bool:
        if len(x) != self.N:
            return False, f"Expected {self.N} examples, received {len(x)}", CheckerTag.INCORRECT_LENGTH
        if len(set(x)) != len(x):
            return False, f"Elements of {x} are non-distinct", CheckerTag.INCORRECT_FORMAT
        for n in x:
            if not isinstance(n, int) or n < 1:
                return False, f"{n} is not a positive integer", CheckerTag.INCORRECT_FORMAT
            if (mod_exp(4, n, n**2+n+1) + mod_exp(2, n, n**2+n+1) + 1) % (n**2+n+1) != 0:
                return False, f"Number {n} does not satisfy the property", CheckerTag.INCORRECT_SOLUTION
        return True, "OK", CheckerTag.CORRECT

    @staticmethod
    def generate() -> "ProblemJBMO2018N4":
        k = random.randint(7, 10)
        return ProblemJBMO2018N4(k)

    def get_solution(self):
        return get_solution(self.N)
