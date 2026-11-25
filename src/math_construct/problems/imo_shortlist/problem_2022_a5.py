from math_construct.problems.templates import TEMPLATES
PROBLEM_TEMPLATE = TEMPLATES["imo_shortlist/problem_2022_a5.py"]

import math
import random
from math_construct.problems.problem import Problem, ProblemConfig, Tag, CheckerTag


FORMATTING_INSTRUCTIONS = r"""Output the sequence $(r, a_1, a_2, \ldots, a_n)$ as a comma-separated list of numbers inside of inside of $\boxed{...}$. For example $\boxed{1.5, 1, 2, 3}$."""

def get_solution(n: int):
    if n == 2:
        return [2, 1, 3]
    if n == 3:
        r = (1 + math.sqrt(5)) / 2
        return [r, 0, r, r+r*r]
    elif n == 4:
        # find roots of x^3 - x - 1 = 0 with sympy
        # x = sympy.symbols('x')
        # roots = sympy.solve(x**3 - x - 1, x)
        r = 1.32471795724475
        return [r, 0, r, r + r*r, r + r*r + r*r*r]


class Problem22(Problem):
    config = ProblemConfig(
        name=Problem.get_name(__file__),
        statement=PROBLEM_TEMPLATE,
        formatting_instructions=FORMATTING_INSTRUCTIONS,
        parameters=["n"],
        source="IMO Shortlist 2022 A5",
        original_parameters={"n": 4},
        original_solution=get_solution(4),
        problem_url="https://www.imo-official.org/problems/IMO2022SL.pdf#page=18",
        solution_url="https://www.imo-official.org/problems/IMO2022SL.pdf#page=18",
        tags=[Tag.ALGEBRA, Tag.IS_SIMPLIFIED, Tag.FIND_ALL] 
    )
    n: int

    def __init__(self, n: int):
        self.n = n

    def get_problem(self):
        return PROBLEM_TEMPLATE.format(n=self.n)

    def check(self, a: list[float]) -> bool:
        if len(a) != self.n + 1:
            return False, f"List of size {len(a)}, should be {self.n+1}", CheckerTag.INCORRECT_LENGTH
        r, a = a[0], a[1:]
        if r <= 0:
            return False, f"r={r} is not positive", CheckerTag.INCORRECT_FORMAT
        if any(a[i] >= a[i+1] for i in range(self.n-1)):
            return False, "a must be strictly increasing", CheckerTag.INCORRECT_SOLUTION
        target_diffs = [r**i for i in range(1, self.n*(self.n-1)//2+1)]
        diffs = [a[j] - a[i] for i in range(self.n) for j in range(i+1, self.n)]
        diffs.sort()
        for i in range(len(diffs)):
            if abs(diffs[i] - target_diffs[i]) > 1e-3 * min(1, target_diffs[i]):
                return False, f"The arrays of differences are not equal at index {i}", CheckerTag.INCORRECT_SOLUTION
        return True, "OK", CheckerTag.CORRECT

    @staticmethod
    def generate() -> "Problem22":
        n = random.randint(3, 4) # 2 trivial
        return Problem22(n)

    def get_solution(self):
        return get_solution(self.n)
