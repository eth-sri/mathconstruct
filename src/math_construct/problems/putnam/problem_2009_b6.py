from math_construct.problems.templates import TEMPLATES
PROBLEM_TEMPLATE = TEMPLATES["putnam/problem_2009_b6.py"]

import math
import random
from fractions import Fraction

from math_construct.problems.problem import Problem, ProblemConfig, Tag, CheckerTag
from math_construct.templates import get_list_template


def get_solution(m: int, n: int) -> list[int]:
    p2 = 1
    while n%2 == 0:
        n //= 2
        p2 *= 2
    x = 1
    while x < n:
        x *= 2
    a = [0, 1, 2*x+1, (x+1)**2, x**n+1, n*(x+1), x, n]
    while len(a) < m + 1:
        a.append(n)
    a = [x*p2 for x in a]
    return a

class Problem_Putnam2009B6(Problem):
    config = ProblemConfig(
        name=Problem.get_name(__file__),
        statement=PROBLEM_TEMPLATE,
        formatting_instructions=get_list_template(),
        parameters=["m", "n"],
        source="Putnam 2009 B6",
        original_parameters={"m": 10, "n": 7},
        original_solution=get_solution(10, 7),
        tags=[Tag.NUMBER_THEORY, Tag.FIND_ANY],
        problem_url="https://kskedlaya.org/putnam-archive/2009.pdf",
        solution_url="https://kskedlaya.org/putnam-archive/2009s.pdf",
    )
    m: int

    def __init__(self, m: int, n: int):
        self.m = m
        self.n = n

    def get_problem(self):
        return PROBLEM_TEMPLATE.format(m=self.m, n=self.n)

    def check(self, x: list[int]) -> tuple[bool, str]:
        def is_power_of_2(n: int) -> bool:
            return n & (n-1) == 0
        if len(x) != self.m + 1:
            return False, f"List of size {len(x)}, should be {self.m + 1}", CheckerTag.INCORRECT_LENGTH
        if not all(isinstance(y, int) for y in x):
            return False, "All elements should be integers", CheckerTag.INCORRECT_FORMAT
        if x[0] != 0 or x[-1] != self.n:
            return False, "a_0 != 0 or a_m != n", CheckerTag.INCORRECT_FORMAT
        for i in range(1, len(x)):
            ok = False
            for j in range(i):
                if is_power_of_2(x[i] - x[j]):
                    ok = True
                    break
            if not ok:
                for b in x[:i]:
                    for c in x[:i]:
                        if b>0 and c>0 and b%c == x[i]:
                            ok = True
                            break
                    if ok:
                        break
            if not ok:
                return False, f"x[i] not of the form b mod c or b+2^k", CheckerTag.INCORRECT_SOLUTION
        return True, "OK", CheckerTag.CORRECT

    @staticmethod
    def generate() -> "Problem_Putnam2009B6":
        m = random.randint(8, 50)
        n = random.randint(3, 20)
        return Problem_Putnam2009B6(m, n)

    def get_solution(self):
        return get_solution(self.m, self.n)
