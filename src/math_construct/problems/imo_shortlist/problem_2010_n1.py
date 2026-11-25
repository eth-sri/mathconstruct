from math_construct.problems.templates import TEMPLATES
PROBLEM_TEMPLATE = TEMPLATES["imo_shortlist/problem_2010_n1.py"]

# NOTE: the original shortlist had 2 variants, hard to find more 

from math_construct.problems.problem import Problem, ProblemConfig, Tag, CheckerTag
import itertools
import math
import random
from fractions import Fraction


FORMATTING_INSTRUCTIONS = r"""Output a comma-separated list of integers within a \boxed environment, for example: \boxed{1, 2, 3, 4}."""

def get_solution(k: int) -> list[list[float]]:
    if k == 51:
        n = 39 
        return list(range(2, 34)) + list(range(35, 41)) + [67]
    elif k == 42:
        n = 48 
        return list(range(2, 34)) + list(range(36, 51)) + [67]
    else:
        raise ValueError(f"Invalid variant k = {k}")

class Problem2010N1(Problem):
    config = ProblemConfig(
        name=Problem.get_name(__file__),
        statement=PROBLEM_TEMPLATE,
        formatting_instructions=FORMATTING_INSTRUCTIONS,
        parameters=["k"],
        source="IMO 2010 Shortlist N1",
        problem_url="https://www.imo-official.org/problems/IMO2010SL.pdf#page=65",
        solution_url="https://www.imo-official.org/problems/IMO2010SL.pdf#page=65",
        original_parameters={"k": 42},
        original_solution=get_solution(42),
        tags=[Tag.NUMBER_THEORY, Tag.FIND_ANY, Tag.IS_ORIGINAL]
    )
    k: int

    def __init__(self, k: int):
        self.k = k
        if self.k == 51:
            self.n = 39
        elif self.k == 42:
            self.n = 48
        else:
            raise ValueError(f"Invalid variant k = {k}")

    def get_problem(self):
        return PROBLEM_TEMPLATE.format(k=self.k)
    
    def check(self, solution: list[int]) -> tuple[bool, str, CheckerTag]:
        # format 
        if len(solution) != self.n:
            return False, f"List of size {len(solution)}, should be {self.n}", CheckerTag.INCORRECT_LENGTH

        if not all(isinstance(s, int) and s > 0 for s in solution) or len(set(solution)) != len(solution):
            return False, "Elements must be distinct positive integers", CheckerTag.INCORRECT_FORMAT
        # equality
        ret = Fraction(1)
        for s in solution:
            ret *= Fraction(s-1, s)
        if ret != Fraction(self.k, 2010):
            return False, f"Product is {ret}, should be {Fraction(self.k, 2010)}", CheckerTag.INCORRECT_SOLUTION
        return True, "OK", CheckerTag.CORRECT

    @staticmethod
    def generate() -> "Problem2010N1":
        # random choice of two (one of which is original, 42)
        k = random.choice([42, 51])
        return Problem2010N1(k)

    def get_solution(self):
        return get_solution(self.k)
