from math_construct.problems.templates import TEMPLATES
PROBLEM_TEMPLATE = TEMPLATES["imo_shortlist/problem_2008_a2.py"]

from math_construct.problems.problem import Problem, ProblemConfig, Tag, CheckerTag
import itertools
import math
import random
from fractions import Fraction
import numpy as np  



FORMATTING_INSTRUCTIONS = r"""Output a comma-separated list of triples of fractions (or integers), within a single \boxed environment, for example for n=2: \boxed{(\frac{1}{2},\frac{3}{4},-1),(\frac{1}{3},3,\frac{-4}{6})}."""

def get_solution(n: int) -> list[list[float]]:
    ret = []
    for k in range(2, n+2):
        x = Fraction(-k, (k - 1)**2)
        y = Fraction(k - k**2, 1)
        z = Fraction(k-1, k**2)
        ret.append([x, y, z])
    return ret 

class Problem2008A2(Problem):
    config = ProblemConfig(
        name=Problem.get_name(__file__),
        statement=PROBLEM_TEMPLATE,
        formatting_instructions=FORMATTING_INSTRUCTIONS,
        parameters=["n"],
        source="IMO 2008 Shortlist A2",
        original_parameters={"n": 20},
        original_solution=get_solution(20),
        problem_url="https://www.imo-official.org/problems/IMO2008SL.pdf#page=10",
        solution_url="https://www.imo-official.org/problems/IMO2008SL.pdf#page=10",
        tags=[Tag.ALGEBRA, Tag.FIND_INF, Tag.IS_SIMPLIFIED] 
    )
    n: int

    def __init__(self, n: int):
        self.n = n

    def get_problem(self):
        return PROBLEM_TEMPLATE.format(n=self.n)
    
    def check(self, solution: list[list[list[int]]]) -> tuple[bool, str, CheckerTag]:
        # format 
        if len(solution) != self.n: 
            return False, f"List of size {len(solution)}, should be {self.n}", CheckerTag.INCORRECT_LENGTH
        if any(len(triple) != 3 for triple in solution):
            return False, f"Some list element is not a triple", CheckerTag.INCORRECT_FORMAT

        # check uniqueness
        if len(set(tuple(triple) for triple in solution)) != len(solution):
            return False, "All elements should be unique", CheckerTag.INCORRECT_FORMAT
        # equality 
        for triple in solution:
            triple = [Fraction(x) for x in triple] # as types may not be unified
            x, y, z = triple
            if x * y * z != 1:
                return False, f"Triple {triple} does not satisfy xyz = 1", CheckerTag.INCORRECT_SOLUTION
            try:
                lhs = x**2 / (x-1)**2 + y**2 / (y-1)**2 + z**2 / (z-1)**2 
            except ZeroDivisionError:
                return False, f"Division by zero when computing LHS", CheckerTag.INCORRECT_SOLUTION
            if lhs != 1:
                return False, f"Triple {triple} does not satisfy the equality", CheckerTag.INCORRECT_SOLUTION

        return True, "OK", CheckerTag.CORRECT
        
    @classmethod
    def generate_multiple_explicit(cls, n_problems: int = None) -> list["Problem"]:
        # not used in avg plot
        small = np.linspace(1, 10, 5).astype(int).tolist()
        mid = np.linspace(11, 30, 10).astype(int).tolist()
        big = np.linspace(35, 90, 9).astype(int).tolist() 
        return [cls(k) for k in small + mid + big]

    @staticmethod
    def generate() -> "Problem2008A2":
        n = random.randint(10, 30)
        return Problem2008A2(n)

    def get_solution(self):
        return get_solution(self.n)
