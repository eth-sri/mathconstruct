from math_construct.problems.templates import TEMPLATES
PROBLEM_TEMPLATE = TEMPLATES["imo_shortlist/problem_2016_a5.py"]

from fractions import Fraction
from math_construct.problems.problem import Problem, ProblemConfig, Tag, CheckerTag
from math_construct.templates import get_fraction_template
import math
import random


def get_solution(n: int) -> Fraction:
    r = int(math.sqrt(n))
    while (r+1)*(r+1) <= n:
        r += 1
    s = n - r*r
    if s%2 == 0:
        return r + Fraction(s, 2*r)
    else:
        return (r+1) - Fraction(2*r+1-s, 2*(r+1))

class Problem2016A5(Problem):
    config = ProblemConfig(
        name=Problem.get_name(__file__),
        statement=PROBLEM_TEMPLATE,
        formatting_instructions=get_fraction_template(),
        parameters=["n"],
        source="IMO 2016 Shortlist A5",
        original_parameters={"n": 10 ** 19},
        original_solution=get_solution(10 ** 19),
        tags=[Tag.ALGEBRA, Tag.IS_SIMPLIFIED, Tag.FIND_ANY],
        problem_url="https://www.imo-official.org/problems/IMO2016SL.pdf#page=22",
        solution_url="https://www.imo-official.org/problems/IMO2016SL.pdf#page=22",
    )
    n: int

    def __init__(self, n: int):
        self.n = n 

    def get_problem(self):
        return PROBLEM_TEMPLATE.format(n=self.n)
    
    def check(self, f: Fraction) -> tuple[bool, str, CheckerTag]:
        if f.denominator <= 0 or (f.denominator-1)**2 > self.n:
            return False, f"Denominator {f.denominator} is not in the range [1, {math.sqrt(self.n)+1}]", CheckerTag.INCORRECT_SOLUTION
        if f < 0:
            return False, "Fraction must be >= sqrt(n) (non-negative)", CheckerTag.INCORRECT_SOLUTION
        if f**2 < self.n or f**2 > self.n + 1:
            return False, f"Fraction {f} is not in range [{math.sqrt(self.n)}, {math.sqrt(self.n+1)}]", CheckerTag.INCORRECT_SOLUTION
        return True, "OK", CheckerTag.CORRECT

    @staticmethod
    def generate() -> "Problem2016A5":
        n = random.randint(10**19, 10**20)
        return Problem2016A5(n)

    def get_solution(self):
        return get_solution(self.n)
