from math_construct.problems.templates import TEMPLATES
PROBLEM_TEMPLATE = TEMPLATES["emc/problem_2016_3.py"]


from math_construct.problems.problem import Problem, ProblemConfig, Tag, CheckerTag
from math_construct.templates import get_list_template
import random
import math
from fractions import Fraction
from typing import List


LIST_FORMATTING_TEMPLATE = r"""Output the answer as a comma separated list of fractions inside of $\boxed{...}$. For example $\boxed{\frac{1}{2}, \frac{2}{3}, \frac{1}{1}}$."""
def get_solution(number: int) -> List:
    pythegorean_triples = []
    c = 0
    m = 2
    while len(pythegorean_triples) < number:
        for n in range(1, m + 1):
            a=m * m - n * n
            b=2 * m * n
            c=m * m + n * n
            if(a == 0 or b == 0 or c == 0):
                break
            if math.gcd(a, b) == 1:
                pythegorean_triples.append([a, b, c])
        m = m + 1
    number_from_pythogras = number // 2 if number % 2 == 0 else (number - 1) // 2
    fractions = []
    for triple in pythegorean_triples[:number_from_pythogras]:
        fractions.append(Fraction(abs(triple[1] - triple[0]), triple[2]))
        fractions.append(Fraction(triple[1] + triple[0], triple[2]))
    if number % 2 == 1:
        fractions.append(Fraction(1, 1))
    return fractions

class ProblemEMC20163(Problem):
    config = ProblemConfig(
        name=Problem.get_name(__file__),
        statement=PROBLEM_TEMPLATE,
        formatting_instructions=LIST_FORMATTING_TEMPLATE,
        parameters=["n"],
        source="EMC 2016 Juniors P3",
        original_parameters={"n": 20},
        original_solution=get_solution(20),
        problem_url="https://emc.mnm.hr/wp-content/uploads/2016/12/EMC_2016_Juniors_ENG_Solutions.pdf",
        solution_url="https://emc.mnm.hr/wp-content/uploads/2016/12/EMC_2016_Juniors_ENG_Solutions.pdf",
        tags=[Tag.IS_SIMPLIFIED, Tag.NUMBER_THEORY, Tag.FIND_ANY] 
    )
    n: int

    def __init__(self, n: int):
        self.n = n

    def get_problem(self):
        return PROBLEM_TEMPLATE.format(n=self.n)

    def check(self, x: list[Fraction]) -> bool:
        checker_format = self.check_format(x, expected_length=self.n, is_unique=True)
        if not checker_format[0]:
            return checker_format
        if any(f <= 0 for f in x):
            return False, "All numbers must be positive", CheckerTag.INCORRECT_FORMAT
        sum_of_squares = sum(f*f for f in x)
        if abs(sum_of_squares - self.n) > 1e-6:
            return False, f"Sum of squares is {sum_of_squares}, should be {self.n}", CheckerTag.INCORRECT_SOLUTION
        return True, "OK", CheckerTag.CORRECT  

    @staticmethod
    def generate() -> "ProblemEMC20163":
        n = random.randint(10, 50)
        return ProblemEMC20163(n)

    def get_solution(self):
        return get_solution(self.n)
