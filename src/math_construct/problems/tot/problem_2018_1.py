from math_construct.problems.templates import TEMPLATES
PROBLEM_TEMPLATE = TEMPLATES["tot/problem_2018_1.py"]

import math
import random
from fractions import Fraction

from math_construct.problems.problem import Problem, ProblemConfig, Tag, CheckerTag


FORMATTING_INSTRUCTIONS = r"""Output the fractions as a comma-separated list inside of \boxed, e.g. \boxed{\frac{1}{2}, \frac{1}{3}, \frac{2}{3}}."""

def get_solution(n: int) -> list[list[int]]:
    # set x to n! + 1
    x = math.factorial(n) + 1
    # set i-th fraction to (i+x)/(ix)
    return [Fraction(i+x, i*x) for i in range(1, n+1)]

class Problem16(Problem):
    config = ProblemConfig(
        name=Problem.get_name(__file__),
        statement=PROBLEM_TEMPLATE,
        formatting_instructions=FORMATTING_INSTRUCTIONS,
        parameters=["n"],
        source="Tournament of Towns Spring 2018",
        original_parameters={"n": 10},
        original_solution=get_solution(10),
        problem_url="https://www.maths.usyd.edu.au/u/dzmitry/TT_problems/TT2018JASolutions.pdf#page=1",
        solution_url="https://www.maths.usyd.edu.au/u/dzmitry/TT_problems/TT2018JASolutions.pdf#page=4",
        tags=[Tag.NUMBER_THEORY, Tag.FIND_ANY, Tag.IS_GENERALIZED],
    )
    n: int

    def __init__(self, n: int):
        self.n = n

    def get_problem(self):
        return PROBLEM_TEMPLATE.format(n=self.n)

    def check(self, x: list[Fraction]) -> bool:
        if len(x) != self.n:
            return False, f"List of size {len(x)}, should be {self.n}", CheckerTag.INCORRECT_LENGTH
        for i in range(self.n):
            for j in range(i+1, self.n):
                if x[i].denominator == x[j].denominator:
                    return False, f"Fractions {x[i]} and {x[j]} have the same denominator", CheckerTag.INCORRECT_SOLUTION
        for i in range(self.n):
            if math.gcd(x[i].numerator, x[i].denominator) != 1:
                return False, f"Fraction {x[i]} is not irreducible", CheckerTag.INCORRECT_FORMAT

        if any(f <= 0 for f in x):
            return False, "Fractions must be positive", CheckerTag.INCORRECT_SOLUTION
        min_denom = min(f.denominator for f in x)
        for i in range(self.n):
            for j in range(i+1, self.n):
                if abs((x[i] - x[j]).denominator) >= min_denom:
                    return False, f"Denominator of difference between fractions {i} and {j} is not less than {min_denom}", CheckerTag.INCORRECT_SOLUTION
        return True, "OK", CheckerTag.CORRECT

    @staticmethod
    def generate() -> "Problem16":
        n = random.randint(5, 25)
        return Problem16(n)

    def get_solution(self):
        return get_solution(self.n)
