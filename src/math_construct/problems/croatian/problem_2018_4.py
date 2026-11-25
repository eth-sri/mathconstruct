from math_construct.problems.templates import TEMPLATES
PROBLEM_TEMPLATE = TEMPLATES["croatian/problem_2018_4.py"]

import random
import math
from math_construct.problems.problem import Problem, ProblemConfig, Tag, CheckerTag
from math_construct.utils import get_latex_array
from math_construct.templates import get_list_template


def get_solution(n: int):
    a = [1, 2]
    while len(a) < n:
        k = 1
        for x in a:
            k = math.lcm(k, x)
        for i in range(len(a)):
            for j in range(i+1, len(a)):
                k = math.lcm(k, a[j]-a[i])
        a = [k] + [x + k for x in a]
    return a

class Problem_HMO_2018_4(Problem):
    config = ProblemConfig(
        name=Problem.get_name(__file__),
        statement=PROBLEM_TEMPLATE,
        formatting_instructions=get_list_template(),
        parameters=["n"],
        source="HMO 2018 4",
        original_parameters={"n": 6},
        original_solution=get_solution(6),
        problem_url="https://natjecanja.math.hr/wp-content/uploads/2019/03/HMO2018-rje.pdf#page=16", # page 16
        solution_url="https://natjecanja.math.hr/wp-content/uploads/2019/03/HMO2018-rje.pdf#page=16", # page 16
        tags=[Tag.NUMBER_THEORY, Tag.FIND_ANY, Tag.IS_SIMPLIFIED],
    )
    n: int

    def __init__(self, n: int):
        self.n = n

    def get_problem(self):
        return PROBLEM_TEMPLATE.format(n=self.n)

    def check(self, x: list[int]):
        if len(x) != self.n:
            return False, f"List does not have exactly {self.n} elements", CheckerTag.INCORRECT_LENGTH
        if any(not isinstance(v, int) or isinstance(v, bool) for v in x):
            return False, "All elements must be integers", CheckerTag.INCORRECT_FORMAT
        if any(x[i] <= 0 for i in range(self.n)):
            return False, f"All elements must be positive", CheckerTag.INCORRECT_FORMAT
        for i in range(self.n):
            for j in range(i+1, self.n):
                if x[j] <= x[i]:
                    return False, f"{x[j]+x[i]}/{x[j]-x[i]} is not a positive integer", CheckerTag.INCORRECT_SOLUTION
                if (x[j] + x[i]) % (x[j] - x[i]) != 0:
                    return False, f"{(x[j] + x[i]) % (x[j] - x[i])} is not an integer", CheckerTag.INCORRECT_SOLUTION
        return True, "OK", CheckerTag.CORRECT

    @staticmethod
    def generate() -> "Problem_HMO_2018_4":
        n = random.randint(6, 8)
        return Problem_HMO_2018_4(n)

    def get_solution(self):
        return get_solution(self.n)
