from math_construct.problems.templates import TEMPLATES
PROBLEM_TEMPLATE = TEMPLATES["imo_shortlist/problem_2012_c2.py"]


from math_construct.problems.problem import Problem, ProblemConfig, Tag, CheckerTag
import itertools
import math
import random
from fractions import Fraction
import numpy as np

FORMATTING_INSTRUCTIONS = r"""Output a comma-separated list of pairs inside of \boxed, for example \boxed{((2,3), (4,5), (1, 6))}."""

def get_solution(n: int, m: int) -> list[list[int]]:
    if n % 5 in [3, 4, 0]:
        k = (m-1) // 2 
    else: 
        k = m // 2
    a = list(reversed(range(2*k+2, 3*k+2))) + list(reversed(range(3*k+2, 4*k+3)))
    b = list(range(2, 2*k+2, 2)) + list(range(1, 2*k+2, 2))
    
    if n % 5 == 2: 
        a = a[:-1]
        b = b[:-1]
    elif n % 5 == 1: 
        a = a[:-1]
        b = b[:-1]
        a = [x-1 for x in a]
    return [[a[i], b[i]] for i in range(m)]

class Problem2012C2(Problem):
    config = ProblemConfig(
        name=Problem.get_name(__file__),
        statement=PROBLEM_TEMPLATE,
        formatting_instructions=FORMATTING_INSTRUCTIONS,
        parameters=["n", "m"],
        source="IMO 2012 Shortlist C2",
        original_parameters={"n": 70, "m": 27},
        original_solution=get_solution(70, 27),
        problem_url="https://www.imo-official.org/problems/IMO2012SL.pdf#page=20",
        solution_url="https://www.imo-official.org/problems/IMO2012SL.pdf#page=20",
        tags=[Tag.COMBINATORICS, Tag.FIND_MAX_MIN, Tag.IS_SIMPLIFIED]
    )
    n: int

    def __init__(self, n: int, m: int):
        self.n = n 
        assert m == int((2*n-1)/5), f"Invalid params: {n} and {m}"
        self.m = m 

    def get_problem(self):
        return PROBLEM_TEMPLATE.format(n=self.n, m=self.m)
    
    def check(self, solution: list[list[int]]) -> tuple[bool, str, CheckerTag]:
        # format 
        if len(solution) != self.m:
            return False, f"List of size {len(solution)}, should be {self.m}", CheckerTag.INCORRECT_LENGTH
        if any(len(a) != 2 for a in solution):
            return False, f"Some list element is not a pair", CheckerTag.INCORRECT_FORMAT

        # conditions
        elems = set()
        sums = set() 
        for a, b in solution: 
            if not (isinstance(a, int) and isinstance(b, int)) or a < 1 or a > self.n or b < 1 or b > self.n:
                return False, f"Pair {[a, b]} must consist of integers in [1, n]", CheckerTag.INCORRECT_FORMAT
            elems.add(a)
            elems.add(b)
            s = a+b 
            if s > self.n:
                return False, f"Sum {s} of {a} and {b} exceeds n={self.n}", CheckerTag.INCORRECT_SOLUTION
            sums.add(s)
        if len(elems) != 2*self.m:
            return False, f"Pairs are not disjoint", CheckerTag.INCORRECT_SOLUTION
        if len(sums) != self.m:
            return False, f"Sums are not distinct", CheckerTag.INCORRECT_SOLUTION
        
        return True, "OK", CheckerTag.CORRECT

    @classmethod
    def generate_multiple_explicit(cls, n_problems: int = None) -> list["Problem"]:
        # not used in avg plot
        small = np.linspace(3, 23, 5).astype(int).tolist()
        mid = np.linspace(23, 100, 10).astype(int).tolist()
        big = np.linspace(100, 1200, 5).astype(int).tolist() 
        return [cls(n, int((2*n-1)/5)) for n in small + mid + big]

    @staticmethod
    def generate() -> "Problem2012C2":
        n = random.randint(23, 100)
        m = int((2*n-1)/5)
        return Problem2012C2(n, m)

    def get_solution(self):
        return get_solution(self.n, self.m)
