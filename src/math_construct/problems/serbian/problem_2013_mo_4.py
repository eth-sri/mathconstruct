from math_construct.problems.templates import TEMPLATES
PROBLEM_TEMPLATE = TEMPLATES["serbian/problem_2013_mo_4.py"]

import random

from math_construct.problems.problem import Problem, ProblemConfig, Tag, CheckerTag
from math_construct.templates import get_list_template
from fractions import Fraction


FORMATTING_INSTRUCTIONS = r"""Output a comma-separated list of triples inside of \boxed. For example: \boxed{(1,2,3), (4,5,6)}."""

def get_solution(n: int) -> list[list[Fraction]]:
    ret = [] 
    m = n//2 
    for i in range(1, m+1):
        ret.append([2*i-1, 2*i+n, 2*i+2*n-1])
        ret.append([2*i, 2*i+n-1, 2*i+2*n])
    return ret 

class ProblemSMO2013_4(Problem):
    # aka: Day 2 Problem 1
    config = ProblemConfig(
        name=Problem.get_name(__file__),
        statement=PROBLEM_TEMPLATE,
        formatting_instructions=FORMATTING_INSTRUCTIONS,
        parameters=["n"],
        source="Serbian MO 2013 Problem 4 (D2 P1)",
        problem_url="https://imomath.com/srb/zadaci/2013_smo.pdf#page=2",
        solution_url="https://imomath.com/srb/zadaci/2013_smo_resenja.pdf#page=5",
        original_parameters={"n": 16},
        original_solution=get_solution(16),
        tags=[Tag.NUMBER_THEORY, Tag.FIND_ALL, Tag.IS_SIMPLIFIED, Tag.IS_TRANSLATED]
    )
    n: int 

    def __init__(self, n: int):
        self.n = n

    def get_problem(self):
        return PROBLEM_TEMPLATE.format(n=self.n)
    
    def check(self, solution: list[list[int]]) -> tuple[bool, str, CheckerTag]:
        # length  
        if len(solution) != self.n:
            return False, f"List of size {len(solution)}, should be {self.n}", CheckerTag.INCORRECT_LENGTH

        # format 
        uniques = set()
        for sol in solution:
            if len(sol) != 3:
                return False, f"Element {sol} is not a triple", CheckerTag.INCORRECT_FORMAT
            for x in sol:
                if x <= 0 or x > 3*self.n:
                    return False, f"{sol} has an element which is not in the set", CheckerTag.INCORRECT_FORMAT
                uniques.add(x) 
        if len(uniques) != 3*self.n or uniques != set(range(1, 3*self.n + 1)):
            return False, f"Triples are not disjoint", CheckerTag.INCORRECT_FORMAT
        
        # constraints
        for sol in solution: 
            ba = sol[1] - sol[0]
            cb = sol[2] - sol[1]
            if ba == cb:
                return False, f"Triple {sol} has equal differences", CheckerTag.INCORRECT_SOLUTION 
            if ba not in [self.n-1, self.n, self.n+1] or cb not in [self.n-1, self.n, self.n+1]:
                return False, f"Triple {sol} has invalid differences", CheckerTag.INCORRECT_SOLUTION

        return True, "OK", CheckerTag.CORRECT

    @staticmethod
    def generate() -> "ProblemSMO2013_4":
        m = random.choice(range(10, 20, 2))
        return ProblemSMO2013_4(m)

    def get_solution(self):
        return get_solution(self.n)
