from math_construct.problems.templates import TEMPLATES
PROBLEM_TEMPLATE = TEMPLATES["imo_shortlist/problem_2011_a1.py"]

# NOTE: added a bound on a1 to force both classes

from math_construct.problems.problem import Problem, ProblemConfig, Tag, CheckerTag
import itertools
import math
import random
from fractions import Fraction


FORMATTING_INSTRUCTIONS = r"""Output a comma-separated list of 4-tuples of integers inside of \boxed, for example \boxed{((2,3,4,5), (4,5,6,7))}."""

def get_solution(n: int) -> list[list[int]]:
    ret = [] 
    i = 1 
    while len(ret) < n:
        ret.append([i, 5*i, 7*i, 11*i])
        ret.append([i, 11*i, 19*i, 29*i])
        i += 1
    ret = ret[:n]
    return ret

class Problem2011A1(Problem):
    config = ProblemConfig(
        name=Problem.get_name(__file__),
        statement=PROBLEM_TEMPLATE,
        formatting_instructions=FORMATTING_INSTRUCTIONS,
        parameters=["n"],
        source="IMO 2011 Shortlist A1",
        original_parameters={"n": 21},
        original_solution=get_solution(21),
        problem_url="https://www.imo-official.org/problems/IMO2011SL.pdf#page=13",
        solution_url="https://www.imo-official.org/problems/IMO2011SL.pdf#page=13",
        tags=[Tag.ALGEBRA, Tag.FIND_MAX_MIN, Tag.IS_SIMPLIFIED]
    )
    n: int

    def __init__(self, n: int):
        self.n = n 
        self.bound = math.ceil(n/2)

    def get_problem(self):
        return PROBLEM_TEMPLATE.format(n=self.n, bound=self.bound)
    
    def check(self, solution: list[list[int]]) -> tuple[bool, str, CheckerTag]:
        # format 
        if len(solution) != self.n:
            return False, f"List of size {len(solution)}, should be {self.n}", CheckerTag.INCORRECT_LENGTH
        if any(len(a) != 4 for a in solution):
            return False, f"Some list element is not a 4-tuple", CheckerTag.INCORRECT_FORMAT

        # assert uniqueness
        if not all(isinstance(ai, int) for a in solution for ai in a):
            return False, "All elements should be integers", CheckerTag.INCORRECT_FORMAT
        if len(set(frozenset(a) for a in solution)) != len(solution):
            return False, "All elements should be unique", CheckerTag.INCORRECT_FORMAT
        # conditions 
        for a in solution: 
            if any(ai <= 0 for ai in a):
                return False, f"Nonpositive element found in set {a}", CheckerTag.INCORRECT_FORMAT
            if len(set(a)) != 4:
                return False, f"Duplicate element found in set {a}", CheckerTag.INCORRECT_FORMAT
            if a[0] > self.bound:
                return False, f"First element {a[0]} of {a} exceeds bound {self.bound}", CheckerTag.INCORRECT_SOLUTION
            sa = sum(a)
            pa = 0 
            for i in range(4):
                for j in range(i+1, 4):
                    if sa % (a[i] + a[j]) == 0:
                        pa += 1
            if pa != 4:
                return False, f"Set {a} has {pa} pairs dividing {sa} (expected 4)", CheckerTag.INCORRECT_SOLUTION
        
        return True, "OK", CheckerTag.CORRECT

    @staticmethod
    def generate() -> "Problem2011A1":
        n = random.randint(10, 31)
        return Problem2011A1(n)

    def get_solution(self):
        return get_solution(self.n)
