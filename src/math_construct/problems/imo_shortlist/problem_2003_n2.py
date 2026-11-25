from math_construct.problems.templates import TEMPLATES
PROBLEM_TEMPLATE = TEMPLATES["imo_shortlist/problem_2003_n2.py"]

from math_construct.problems.problem import Problem, ProblemConfig, Tag, CheckerTag
import itertools
import math
import random


FORMATTING_INSTRUCTIONS = r"""Output the sequence of numbers $a$ as a comma-separated list inside of \boxed, e.g. \boxed{256, 512, 1024}."""

def get_solution(k: int) -> list[int]:
    ret = [3,2,1][:k]
    while len(ret) < k:
        ret += [int("2" + str(ret[-1]))]
    return ret 

class Problem2003N2(Problem):
    config = ProblemConfig(
        name=Problem.get_name(__file__),
        statement=PROBLEM_TEMPLATE,
        formatting_instructions=FORMATTING_INSTRUCTIONS,
        parameters=["k"],
        source="IMO 2003 Shortlist N2",
        original_parameters={"k": 15},
        original_solution=get_solution(15),
        problem_url="https://anhngq.wordpress.com/wp-content/uploads/2010/07/imo-2003-shortlist.pdf#page=60",
        solution_url="https://anhngq.wordpress.com/wp-content/uploads/2010/07/imo-2003-shortlist.pdf#page=60",
        tags=[Tag.NUMBER_THEORY, Tag.FIND_ALL, Tag.IS_SIMPLIFIED]
    )
    k: int

    def __init__(self, k: int):
        self.k = k

    def get_problem(self):
        return PROBLEM_TEMPLATE.format(k=self.k)

    def is_good(self, a: int) -> bool:
        b = int(str(a)[-1] + str(a)[:-1])
        c = b**2
        d = int(str(c)[1:] + str(c)[0])
        return d == a**2

    def check(self, solution: list[int]) -> tuple[bool, str, CheckerTag]:
        if len(solution) != self.k:
            return False, f"List of size {len(solution)}, should be {self.k}", CheckerTag.INCORRECT_LENGTH
        if len(set(solution)) < len(solution):
            return False, "List contains duplicates", CheckerTag.INCORRECT_FORMAT
        for a in solution: 
            if not isinstance(a, int) or a <= 0:
                return False, f"Number {a} is not a positive integer", CheckerTag.INCORRECT_FORMAT
            if not self.is_good(a):
                return False, f"Number {a} is not good", CheckerTag.INCORRECT_SOLUTION
        return True, "OK", CheckerTag.CORRECT

    @staticmethod
    def generate() -> "Problem2003N2":
        k = random.randint(15, 30)
        return Problem2003N2(k)

    def get_solution(self):
        return get_solution(self.k)
