from math_construct.problems.templates import TEMPLATES
PROBLEM_TEMPLATE = TEMPLATES["imo_shortlist/problem_2005_c8.py"]

from math_construct.problems.problem import Problem, ProblemConfig, Tag, CheckerTag
import itertools
import math
import random


FORMATTING_INSTRUCTIONS = r"""Output the list of green diagonals, followed by the list of red diagonals, separated by a comma, inside of \boxed. Each list of diagonals should contain comma-separated pairs $(a,b)$, referring to the diagonal $(A_a, A_b)$. For example, a well-formatted output is \boxed{((1,3), (2,4)), ((2,5), (3,5))}."""

def get_solution(n: int) -> list[list[list[int]]]:
    green = [] 
    l = n // 2 + 1 
    for i in range(3, l+1):
        green.append([1, i])
    for j in range(l+2, n+1):
        green.append([l, j])
    red = [] 
    for i in range(l+1, n+1):
        red.append([2, i])
    for j in range(3, l):
        red.append([j, l+1])
    return [green, red]

class Problem2005C8(Problem):
    config = ProblemConfig(
        name=Problem.get_name(__file__),
        statement=PROBLEM_TEMPLATE,
        formatting_instructions=FORMATTING_INSTRUCTIONS,
        parameters=["n"],
        source="IMO 2005 Shortlist C8",
        original_parameters={"n": 15},
        original_solution=get_solution(15),
        problem_url="https://www.imomath.com/imocomp/sl05_0707.pdf#page=5",
        solution_url="https://www.imomath.com/imocomp/sl05_0707.pdf#page=13",
        tags=[Tag.COMBINATORICS, Tag.FIND_ALL, Tag.IS_SIMPLIFIED] 
    )
    n: int

    def __init__(self, n: int):
        self.n = n
        self.maxscore = math.ceil(3/4 * (self.n-3)**2)

    def get_problem(self):
        return PROBLEM_TEMPLATE.format(n=self.n, maxscore=self.maxscore)
    
    def intersect_inside(self, d1: list[int], d2: list[int]) -> bool:
        a, b = d1
        c, d = min(d2), max(d2)
        if a == c or a == d or b == c or b == d:
            return False 
        a_there = a > c and a < d 
        b_there = b > c and b < d
        if a_there ^ b_there: 
            return True
        return False 

    def check(self, solution: list[list[list[int]]]) -> tuple[bool, str, CheckerTag]:
        # valid input
        if len(solution) != 2:
            return False, f"Outer list of size {len(solution)}, should be 2", CheckerTag.INCORRECT_LENGTH
        green, red = solution
        if len(green) != self.n-3 or len(red) != self.n-3:
            return False, f"Lists of diagonals of size {len(green)} and {len(red)}, should both be {self.n-3}", CheckerTag.INCORRECT_FORMAT
        all_dias = green+red
        for dia in all_dias:
            if len(dia) != 2:
                return False, f"Diagonal {dia} is not a pair", CheckerTag.INCORRECT_FORMAT
            a, b = dia
            if not (isinstance(a, int) and isinstance(b, int) and 1 <= a <= self.n and 1 <= b <= self.n):
                return False, f"Diagonal {dia} has invalid vertex labels", CheckerTag.INCORRECT_FORMAT
            if (a-b+self.n)%self.n in [0, 1, self.n-1]:
                return False, f"Diagonal {dia} is not a valid diagonal", CheckerTag.INCORRECT_FORMAT
        all_dias_str = [str(sorted(x)) for x in all_dias]
        if len(all_dias_str) != len(set(all_dias_str)):
            return False, f"Some diagonals are repeated", CheckerTag.INCORRECT_FORMAT

        # no same color intersections
        for d1, d2 in itertools.combinations(green, 2):
            if self.intersect_inside(d1, d2):
                return False, 'Green intersect inside', CheckerTag.INCORRECT_SOLUTION
        for d1, d2 in itertools.combinations(red, 2):
            if self.intersect_inside(d1, d2):
                return False, 'Red intersect inside', CheckerTag.INCORRECT_SOLUTION
        
        # count intersections
        nb_intersections = 0 
        for d1 in green:
            for d2 in red:
                if self.intersect_inside(d1, d2):
                    nb_intersections += 1
        
        if nb_intersections != self.maxscore:
            return False, f"Number of intersections {nb_intersections} is not maximal (expected {self.maxscore})", CheckerTag.INCORRECT_SOLUTION
        return True, "OK", CheckerTag.CORRECT

    @staticmethod
    def generate() -> "Problem2005C8":
        n = random.randint(14, 24)
        return Problem2005C8(n)

    def get_solution(self):
        return get_solution(self.n)
