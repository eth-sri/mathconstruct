from math_construct.problems.templates import TEMPLATES
PROBLEM_TEMPLATE = TEMPLATES["croatian/problem_2020_4.py"]

import random
import math
from sympy import divisors, divisor_sigma
from fractions import Fraction
from math_construct.problems.problem import Problem, ProblemConfig, Tag, CheckerTag
from math_construct.utils import get_latex_array
from math_construct.templates import get_list_template


FORMATTING_TEMPLATE = r"""Output the answer as a comma separated list inside of $\boxed{...}$. For example $\boxed{(1, 2), (3, 4), (5, 6)}$."""

def get_solution(n: int):
    sol = [(6, 28)]
    p = 7
    while len(sol) < n:
        # 6p >= 10^(i-1)
        i = len(sol)+1
        p = max(p, 10**(i-1)//6+1)
        assert len(str(6*p)) >= i, f"6*p = {6*p} does not have at least {i} digits"
        if math.gcd(p, 6) == 1 and math.gcd(p, 28) == 1:
            sol.append((6*p, 28*p))
        p += 1
    return sol


class Problem_HMO_2020_4(Problem):
    config = ProblemConfig(
        name=Problem.get_name(__file__),
        statement=PROBLEM_TEMPLATE,
        formatting_instructions=FORMATTING_TEMPLATE,
        parameters=["n"],
        source="HMO 2020 4",
        original_parameters={"n": 8},
        original_solution=get_solution(8),
        problem_url="https://natjecanja.math.hr/wp-content/uploads/2021/01/HMO2020-rje.pdf#page=3", # page 3
        solution_url="https://natjecanja.math.hr/wp-content/uploads/2021/01/HMO2020-rje.pdf#page=3", # page 3
        tags=[Tag.NUMBER_THEORY, Tag.FIND_INF, Tag.IS_SIMPLIFIED],
    )
    n: int

    def __init__(self, n: int):
        self.n = n

    def get_problem(self):
        return PROBLEM_TEMPLATE.format(n=self.n)

    def check(self, x: list[list[int]]):
        def get_sum(m: int):
            d = divisors(m)
            res = 0
            for i in d:
                res += 1.0/i
            return res
        if len(x) != self.n:
            return False, f"List does not have exactly {self.n} elements", CheckerTag.INCORRECT_LENGTH
        for i in range(self.n):
            if len(x[i]) != 2:
                return False, f"Tuple {x[i]} does not have exactly 2 elements", CheckerTag.INCORRECT_FORMAT
            if not all(isinstance(v, int) and v > 0 for v in x[i]):
                return False, f"Tuple {x[i]} must contain positive integers", CheckerTag.INCORRECT_FORMAT
            if len(str(x[i][0])) < i+1 or len(str(x[i][1])) < i+1:
                return False, f"Elements of tuple {x[i]} do not have at least {i+1} digits", CheckerTag.INCORRECT_FORMAT
            if Fraction(divisor_sigma(x[i][0]), x[i][0]) != Fraction(divisor_sigma(x[i][1]), x[i][1]):
                return False, f"Sum of reciprocals of divisors of {x[i][0]} and {x[i][1]} are not the same", CheckerTag.INCORRECT_SOLUTION
        if len(set(tuple(t) for t in x)) != self.n:
            return False, "Tuples are not distinct", CheckerTag.INCORRECT_SOLUTION
        return True, "OK", CheckerTag.CORRECT

    @staticmethod
    def generate() -> "Problem_HMO_2020_4":
        n = random.randint(8,20)
        return Problem_HMO_2020_4(n)

    def get_solution(self):
        return get_solution(self.n)
