from math_construct.problems.templates import TEMPLATES
PROBLEM_TEMPLATE = TEMPLATES["imo_shortlist/problem_2020_a3.py"]

# TODO: Don't have a variation here
import math
import random
from fractions import Fraction
from math_construct.problems.problem import Problem, ProblemConfig, Tag, CheckerTag
from math_construct.templates import get_list_template


def get_solution():
    return [1, 2 + math.sqrt(3), 1, 2 + math.sqrt(3)]

class Problem23(Problem):
    config = ProblemConfig(
        name=Problem.get_name(__file__),
        statement=PROBLEM_TEMPLATE,
        formatting_instructions=get_list_template(),
        parameters=[],
        source="IMO Shortlist 2020 A3",
        original_parameters={},
        original_solution=get_solution(),
        problem_url="https://www.imo-official.org/problems/IMO2020SL.pdf#page=20",
        solution_url="https://www.imo-official.org/problems/IMO2020SL.pdf#page=20",
        tags=[Tag.ALGEBRA, Tag.FIND_MAX_MIN, Tag.IS_SIMPLIFIED]
    )

    def __init__(self):
        pass

    def get_problem(self):
        return PROBLEM_TEMPLATE

    def check(self, solution: list[float]) -> bool:
        a, b, c, d = solution
        if min(a, b, c, d) <= 0:
            return False, "a, b, c, d must be positive", CheckerTag.INCORRECT_SOLUTION
        if abs((a + c) * (b + d) - a * c - b * d) > 1e-3 * min(1, a * c + b * d):
            return False, f"Equation (a+c)(b+d) = ac + bd is not satisfied", CheckerTag.INCORRECT_SOLUTION
        if abs(a / b + b / c + c / d + d / a - 8) > 1e-3:
            return False, f"Equation a/b + b/c + c/d + d/a = 8 is not satisfied", CheckerTag.INCORRECT_SOLUTION
        return True, "OK", CheckerTag.CORRECT

    @staticmethod
    def generate() -> "Problem23":
        return Problem23()

    def get_solution(self):
        return get_solution()
