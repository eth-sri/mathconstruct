from math_construct.problems.templates import TEMPLATES
PROBLEM_TEMPLATE = TEMPLATES["bxmo/problem_2020_4.py"]

import math
import random
from math_construct.problems.problem import Problem, ProblemConfig, Tag, CheckerTag
from math_construct.templates import get_integer_template
from sympy import divisors
import math


def get_solution(n):
    m = 3 ** (n - 1)
    k = math.ceil(math.log2(m))
    if 2 ** k < m:
        k += 1
    return 2 ** k * m


class ProblemBxMO20204(Problem):
    config = ProblemConfig(
        name=Problem.get_name(__file__),
        statement=PROBLEM_TEMPLATE,
        formatting_instructions=get_integer_template("Your answer can contain mathematical operations using valid LaTeX notation."),
        problem_url="http://bxmo.org/problems/bxmo-problems-2020-zz.pdf",
        solution_url="http://bxmo.org/problems/bxmo-problems-2t020-zz.pdf",
        parameters=["n"],
        source="BxMO 2020 P4",
        original_parameters={"n": 60},
        original_solution=get_solution(60),
        tags=[Tag.NUMBER_THEORY, Tag.FIND_ANY, Tag.IS_GENERALIZED, Tag.IS_SIMPLIFIED] 
    )
    n: int

    def __init__(self, n: int):
        self.n = n

    def get_problem(self):
        return PROBLEM_TEMPLATE.format(n=self.n)
        
    def check(self, a: int) -> bool:
        check_format = self.check_format(a, is_integer=True, min_val_inclusive=1)
        if not check_format[0]:
            return check_format
        divisors_number = divisors(a)
        count = 0
        for divisor in divisors_number:
            if a < divisor * divisor < 4 * a:
                count += 1
        if not count == self.n:
            return False, f"The number should have exactly {self.n} close divisors, but has {count}.", CheckerTag.INCORRECT_SOLUTION
        return True, "OK", CheckerTag.CORRECT

    @staticmethod
    def generate() -> "ProblemBxMO20204":
        N = 2 * random.randint(30,70)
        return ProblemBxMO20204(N)
    
    def get_solution(self):
        return get_solution(self.n)
