from math_construct.problems.templates import TEMPLATES
PROBLEM_TEMPLATE = TEMPLATES["usamo/problem_2006_4.py"]

import math
import random
from sympy import isprime, primefactors
from fractions import Fraction
from math_construct.problems.problem import Problem, ProblemConfig, Tag, CheckerTag
from math_construct.templates import get_list_template


def get_solution(n: int) -> list[Fraction]:
    if n == 4:
        return [Fraction(2,1), Fraction(2,1)]
    if n == 7:
        return [Fraction(9, 2), Fraction(4, 3), Fraction(7, 6)]
    if isprime(n):
        a = [Fraction(n, 2), 4, Fraction(1, 2)]
        k = n - ((n+1)//2+4)
        return a + [Fraction(1,1)] * k
    ps = primefactors(n)
    p1, p2 = ps[0], n//ps[0]
    return [Fraction(p1,1), Fraction(p2,1)] + [Fraction(1,1)] * (n - p1 - p2)

class Problem_USAMO_2006_4(Problem):
    """2006 USAMO Problem 4"""
    config = ProblemConfig(
        name=Problem.get_name(__file__),
        statement=PROBLEM_TEMPLATE,
        formatting_instructions=get_list_template(),
        parameters=["n"],
        source="2006 USAMO Problem 4",
        original_parameters={"n": 51},
        original_solution=get_solution(51),
        tags=[Tag.NUMBER_THEORY, Tag.FIND_ANY, Tag.IS_SIMPLIFIED],
        problem_url="https://artofproblemsolving.com/wiki/index.php/2006_USAMO_Problems/Problem_4",
        solution_url="https://artofproblemsolving.com/wiki/index.php/2006_USAMO_Problems/Problem_4",
    )
    n: int

    def __init__(self, n: int):
        self.n = n

    def get_problem(self):
        return PROBLEM_TEMPLATE.format(n=self.n)

    def check(self, a: list[int | Fraction]) -> tuple[bool, str, CheckerTag]:
        if not all(isinstance(y, int) or isinstance(y, Fraction) for y in a):
            return False, "All elements should be integers or fractions", CheckerTag.INCORRECT_FORMAT
        if sum(a) != math.prod(a):
            return False, f"Sum of the list is {sum(a)}, should be equal to the product {math.prod(a)}", CheckerTag.INCORRECT_SOLUTION
        return True, "OK", CheckerTag.CORRECT

    @staticmethod
    def generate() -> "Problem_USAMO_2006_4":
        n = random.randint(50, 100)
        if n == 5:
            n += 1
        return Problem_USAMO_2006_4(n)

    def get_solution(self):
        return get_solution(self.n)
