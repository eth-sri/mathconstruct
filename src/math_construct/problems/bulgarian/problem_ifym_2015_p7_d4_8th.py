from math_construct.problems.templates import TEMPLATES
PROBLEM_TEMPLATE = TEMPLATES["bulgarian/problem_ifym_2015_p7_d4_8th.py"]

from math_construct.problems.problem import Problem, ProblemConfig, Tag, CheckerTag
from math_construct.templates import get_list_template
import numpy as np
import random
import math


def get_solution(n: int) -> list[int]:
    n = 2*n
    a = -n
    b = (n + 1)
    c = n*(n+1) + 1
    d = (c-1)*c + 1
    return (a, b, c, d)

class ProblemIFYM_2015_P7_4_8(Problem):
    config = ProblemConfig(
        name=Problem.get_name(__file__),
        statement=PROBLEM_TEMPLATE,
        formatting_instructions=get_list_template(),
        parameters=["n"],
        source="IFYM 2015 P7 Day 4",
        original_parameters={"n": 10000001},
        original_solution=get_solution(10000001),
        problem_url="https://klasirane.com/competitions/IFYM/2-8-9%20%D0%BA%D0%BB%D0%B0%D1%81",
        solution_url="https://klasirane.com/competitions/IFYM/2-8-9%20%D0%BA%D0%BB%D0%B0%D1%81",
        tags=[Tag.ALGEBRA, Tag.FIND_ANY, Tag.IS_TRANSLATED, Tag.IS_ORIGINAL]
    )
    n: int

    def __init__(self, n: int):
        self.n = n

    def get_problem(self):
        return PROBLEM_TEMPLATE.format(n=self.n)

    def check(self, x: int) -> bool:
        
        if len(x) != 4:
            return False, f"Example contains {(len(x))} numbers instead of 4", CheckerTag.INCORRECT_LENGTH
        
        for i in x:
            if abs(i) <= self.n:
                return False, f"Each number should have an absolute value higher than {self.n}", CheckerTag.INCORRECT_SOLUTION

        if x[0]*x[1]*x[2] + x[0]*x[2]*x[3] + x[0]*x[1]*x[3] + x[1]*x[2]*x[3] != 1:
            return False, f"The required condition isn't satisfied for this example", CheckerTag.INCORRECT_SOLUTION

        return True, "OK", CheckerTag.CORRECT
        
    @staticmethod
    def generate() -> "ProblemIFYM_2015_P7_4_8":
        n = random.randint(5, 30)
        n = int(2**n)
        return ProblemIFYM_2015_P7_4_8(n)

    def get_solution(self):
        return get_solution(self.n)
