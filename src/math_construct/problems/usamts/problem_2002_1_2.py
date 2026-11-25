from math_construct.problems.templates import TEMPLATES
PROBLEM_TEMPLATE = TEMPLATES["usamts/problem_2002_1_2.py"]

import math
import random

from math_construct.problems.problem import Problem, ProblemConfig, Tag, CheckerTag
from math_construct.templates import get_list_template


def get_solution(k: int) -> list[list[int]]:
    ret = []
    x = 10
    while len(ret) < k:
        i = len(ret) + 1
        # enforce b >= 10^i
        x = max(7 + i, math.ceil(math.sqrt((10**i-6)/3.0)))  # x>=8 keeps a>0, strictly increasing
        a = 3*x**2 - 18*x - 39
        b = 3*x**2 + 6
        c = 3*x**2 + 18*x + 33
        d = 3*x**2 + 36*x + 42
        ret += [[a, b, c, d]]
    return ret

class Problem12(Problem):
    config = ProblemConfig(
        name=Problem.get_name(__file__),
        statement=PROBLEM_TEMPLATE,
        formatting_instructions=get_list_template(extra_instructions="Each element of the list should be a quadruple of integers, e.g. (1, 2, 3, 4)."),
        parameters=["k"],
        source="USAMTS 02/03 Round 1",
        original_parameters={"k": 10},
        original_solution=get_solution(10),
        problem_url="https://files.usamts.org/Problems_14_1.pdf",
        solution_url="https://files.usamts.org/Solutions_14_1.pdf",
        tags=[Tag.NUMBER_THEORY, Tag.IS_ORIGINAL, Tag.FIND_INF]
    )
    k: int

    def __init__(self, k: int):
        self.k = k

    def get_problem(self):
        return PROBLEM_TEMPLATE.format(k=self.k)

    def check(self, x: list[list[int]]) -> bool:
        def is_square(n: int) -> bool:
            return int(math.sqrt(n))**2 == n
        if len(x) != self.k or any(not isinstance(v, int) or v <= 0 for q in x for v in q):
            return False, "Need exactly k quadruples of positive integers", CheckerTag.INCORRECT_SOLUTION
        if len(set(tuple(a) for a in x)) != self.k:
            return False, f"Number of unique quadruples is {len(set(tuple(a) for a in x))}, should be {self.k}", CheckerTag.INCORRECT_SOLUTION
        for i, (a, b, c, d) in enumerate(x):
            if len(set([a, b, c, d])) != 4:
                return False, f"Not all elements of quadruple are distinct", CheckerTag.INCORRECT_SOLUTION
            if len(str(a)) < i+1 and len(str(b)) < i+1 and len(str(c)) < i+1 and len(str(d)) < i+1:
                return False, f"All numbers in the quadruple does not have at least {i+1} digits", CheckerTag.INCORRECT_SOLUTION
            if not is_square(a+b+c) or not is_square(a+b+d) or not is_square(a+c+d) or not is_square(b+c+d):
                return False, f"Not all sums are squares", CheckerTag.INCORRECT_SOLUTION
        return True, "OK", CheckerTag.CORRECT

    @staticmethod
    def generate() -> "Problem12":
        k = random.randint(5, 15)
        return Problem12(k)

    def get_solution(self):
        return get_solution(self.k)
