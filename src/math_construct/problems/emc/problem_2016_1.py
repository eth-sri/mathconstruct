from math_construct.problems.templates import TEMPLATES
PROBLEM_TEMPLATE = TEMPLATES["emc/problem_2016_1.py"]


from math_construct.problems.problem import Problem, ProblemConfig, Tag, CheckerTag
from math_construct.templates import get_list_template
import random
import math
import sympy
from typing import List


LIST_FORMATTING_TEMPLATE = r"""Output the answer as a comma separated list of integers inside of $\boxed{...}$. For example $\boxed{1,2,3,4}$."""

def get_solution(number: int) -> List:
    factorial = math.factorial(2 * number) + 1
    return [2 * factorial + (2 * i - 1) for i in range(2, number + 2)]

class ProblemEMC20161(Problem):
    config = ProblemConfig(
        name=Problem.get_name(__file__),
        statement=PROBLEM_TEMPLATE,
        formatting_instructions=LIST_FORMATTING_TEMPLATE,
        parameters=["n"],
        source="EMC 2016 Juniors P1",
        original_parameters={"n": 10},
        original_solution=get_solution(10),
        problem_url="https://emc.mnm.hr/wp-content/uploads/2016/12/EMC_2016_Seniors_ENG_Solutions.pdf",
        solution_url="https://emc.mnm.hr/wp-content/uploads/2016/12/EMC_2016_Seniors_ENG_Solutions.pdf",
        tags=[Tag.IS_SIMPLIFIED, Tag.IS_GENERALIZED, Tag.NUMBER_THEORY, Tag.FIND_ANY] 
    )
    n: int

    def __init__(self, n: int):
        self.n = n

    def get_problem(self):
        return PROBLEM_TEMPLATE.format(n=self.n, nminusone=self.n-1, nminustwo=self.n-2)

    def check(self, x: list[int]) -> bool:
        checker_format = self.check_format(x, is_integer=True, expected_length=self.n, min_val_inclusive=1)
        if not checker_format[0]:
            return checker_format
        for i in range(self.n):
            if i < self.n - 1 and math.gcd(x[i], x[i + 1]) != 1:
                return False, f"Elements {i} and {i + 1} are not coprime", CheckerTag.INCORRECT_SOLUTION
            if i < self.n - 2 and math.gcd(x[i], x[i + 2]) != 1:
                return False, f"Elements {i} and {i + 2} are not coprime", CheckerTag.INCORRECT_SOLUTION
        for r in range(self.n):
            for s in range(r, self.n):
                if sum(x[r:s+1]) < 4 or sympy.isprime(sum(x[r:s+1])):
                    return False, f"Sum from {r} to {s} is not composite", CheckerTag.INCORRECT_SOLUTION
        return True, "OK", CheckerTag.CORRECT

    @staticmethod
    def generate() -> "ProblemEMC20161":
        n = random.randint(8, 20)
        return ProblemEMC20161(n)

    def get_solution(self):
        return get_solution(self.n)
