from math_construct.problems.templates import TEMPLATES
PROBLEM_TEMPLATE = TEMPLATES["imo_shortlist/problem_2003_n3.py"]

# NOTE: added extra constraint to force the hardest solution class 

from math_construct.problems.problem import Problem, ProblemConfig, Tag, CheckerTag
import itertools
import math
import random


FORMATTING_INSTRUCTIONS = r"""Output the sequence of pairs $(a,b)$ as a comma-separated list inside of \boxed, e.g. \boxed{(10, 5), (20, 10)}."""

def get_solution(k: int) -> list[int]:
    ret = [] 
    for l in range(1, k+1): 
        ret.append([8*l*l*l*l-l, 2*l])
    return ret 

class Problem2003N3(Problem):
    config = ProblemConfig(
        name=Problem.get_name(__file__),
        statement=PROBLEM_TEMPLATE,
        formatting_instructions=FORMATTING_INSTRUCTIONS,
        parameters=["k"],
        source="IMO 2003 Shortlist N3",
        problem_url="https://anhngq.wordpress.com/wp-content/uploads/2010/07/imo-2003-shortlist.pdf#page=62",
        solution_url="https://anhngq.wordpress.com/wp-content/uploads/2010/07/imo-2003-shortlist.pdf#page=62",
        original_parameters={"k": 10},
        original_solution=get_solution(10),
        tags=[Tag.NUMBER_THEORY, Tag.FIND_ALL, Tag.IS_SIMPLIFIED] 
    )
    k: int

    def __init__(self, k: int):
        self.k = k

    def get_problem(self):
        return PROBLEM_TEMPLATE.format(k=self.k)

    def check(self, solution: list[list[int]]) -> tuple[bool, str, CheckerTag]:
        if len(solution) != self.k:
            return False, f"List of size {len(solution)}, should be {self.k}", CheckerTag.INCORRECT_LENGTH
        solution_str = [str(x) for x in solution]
        if len(set(solution_str)) < len(solution_str):
            return False, "List contains duplicates", CheckerTag.INCORRECT_FORMAT
        for x in solution: 
            if len(x) != 2:
                return False, f"List element {x} is not a pair", CheckerTag.INCORRECT_FORMAT
            a, b = x
            if not all(isinstance(v, int) and not isinstance(v, bool) for v in x):
                return False, f"Pair {x} is not a pair of integers", CheckerTag.INCORRECT_FORMAT
            if a <= b or b <= 1:
                return False, f"Pair {x} does not satisfy a>b>1", CheckerTag.INCORRECT_SOLUTION
            top = a*a 
            bot = 2*a*b*b - b*b*b + 1
            if bot <= 0 or top % bot != 0:
                return False, f"For pair {x} the expression is {top}/{bot} which is not a positive integer", CheckerTag.INCORRECT_SOLUTION
        return True, "OK", CheckerTag.CORRECT

    @staticmethod
    def generate() -> "Problem2003N3":
        k = random.randint(10, 30)
        return Problem2003N3(k)

    def get_solution(self):
        return get_solution(self.k)
