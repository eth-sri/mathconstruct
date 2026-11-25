from math_construct.problems.templates import TEMPLATES
PROBLEM_TEMPLATE = TEMPLATES["tot/problem_2005_1.py"]

import random
from fractions import Fraction
from math_construct.problems.problem import Problem, ProblemConfig, Tag, CheckerTag
from math_construct.templates import get_list_template


def get_solution(n: int):
    if n == 1:
        return [1]
    return [(n-1)**(i-1) for i in range(1,n+1)]

class Problem21(Problem):
    config = ProblemConfig(
        name=Problem.get_name(__file__),
        statement=PROBLEM_TEMPLATE,
        formatting_instructions=get_list_template(),
        parameters=["n"],
        source="Tournament of Towns 2005",
        original_parameters={"n": 15},
        original_solution=get_solution(15),
        problem_url="https://www.math.toronto.edu/oz/turgor/archives/TT2005F_SAsolutions.pdf#page=1",
        solution_url="https://www.math.toronto.edu/oz/turgor/archives/TT2005F_SAsolutions.pdf#page=2",
        tags=[Tag.NUMBER_THEORY, Tag.FIND_ANY, Tag.IS_SIMPLIFIED],
    )
    n: int

    def __init__(self, n: int):
        self.n = n

    def get_problem(self):
        return PROBLEM_TEMPLATE.format(n=self.n)

    def check(self, a: list[int]) -> tuple[bool, str]:
        if len(a) != self.n:
            return False, f"List of size {len(a)}, should be {self.n}", CheckerTag.INCORRECT_LENGTH
        if not all(isinstance(x, int) for x in a):
            return False, "All elements should be integers", CheckerTag.INCORRECT_FORMAT
        if any(x <= 0 for x in a) or len(set(a)) != self.n:
            return False, "Integers must be distinct and positive", CheckerTag.INCORRECT_SOLUTION
        sum = 0
        for i in range(self.n):
            sum += Fraction(a[i], a[(i+1)%self.n])
        if sum.denominator != 1:
            return False, f"Sum {sum} is not an integer", CheckerTag.INCORRECT_SOLUTION
        return True, "OK", CheckerTag.CORRECT

    @staticmethod
    def generate() -> "Problem21":
        n = random.randint(15, 25)
        return Problem21(n)

    def get_solution(self):
        return get_solution(self.n)
