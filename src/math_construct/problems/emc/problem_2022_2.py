from math_construct.problems.templates import TEMPLATES
PROBLEM_TEMPLATE = TEMPLATES["emc/problem_2022_2.py"]


from math_construct.problems.problem import Problem, ProblemConfig, Tag, CheckerTag
import random
import math
from typing import List, Tuple
from scipy.spatial import ConvexHull


FORMATTING_INSTRUCTIONS = r"""Output the sequences as comma-separated tuples inside of \boxed, e.g. \boxed{(3, 3, 1), (4, 2, 2)}. The first integer in a tuple is the lovely number and the rest are the divisors $d_1, ..., d_k$."""

def get_solution(n: int) -> List:
    lovely_numbers = [[1, 1]]
    for i in range(2, n+1):
        neww_lovely_number = lovely_numbers[-1][0] * (lovely_numbers[-1][0] + 1)
        divisors = lovely_numbers[-1][1:] + [lovely_numbers[-1][0] + 1]
        lovely_numbers.append([neww_lovely_number] + divisors)
    return lovely_numbers

class ProblemEMC20222(Problem):
    config = ProblemConfig(
        name=Problem.get_name(__file__),
        statement=PROBLEM_TEMPLATE,
        formatting_instructions=FORMATTING_INSTRUCTIONS,
        parameters=["n"],
        source="EMC 2022 Seniors P2",
        original_parameters={"n": 10},
        original_solution=get_solution(10),
        problem_url="https://emc.mnm.hr/wp-content/uploads/2022/12/EMC_2022_Seniors_ENG_Solutions.pdf",
        solution_url="https://emc.mnm.hr/wp-content/uploads/2022/12/EMC_2022_Seniors_ENG_Solutions.pdf",
        tags=[Tag.IS_SIMPLIFIED, Tag.NUMBER_THEORY, Tag.FIND_INF] 
    )
    n: int

    def __init__(self, n: int):
        self.n = n

    def get_problem(self):
        return PROBLEM_TEMPLATE.format(n=self.n)

    def check(self, x: list[list[int]]) -> bool:
        checker_format = self.check_format(x, expected_length=self.n, is_unique=True, is_integer=True, min_val_exclusive=0)
        if not checker_format[0]:
            return checker_format
        if len(set(seq[0] for seq in x)) != len(x):
            return False, "Lovely numbers are not distinct", CheckerTag.INCORRECT_SOLUTION
        for seq in x:
            if len(seq) < 2:
                return False, f"At least one divisor is required: {seq}", CheckerTag.INCORRECT_SOLUTION
            product = math.prod(seq[1:])
            if product != seq[0]:
                return False, f"Product of divisors is not equal to the lovely number: {seq}", CheckerTag.INCORRECT_SOLUTION
            if not all((seq[0] + seq[i]) % seq[i]**2  == 0 for i in range(1, len(seq))):
                return False, f"Condition not satisfied for all divisors: {seq}", CheckerTag.INCORRECT_SOLUTION
        return True, "OK", CheckerTag.CORRECT

    @staticmethod
    def generate() -> "ProblemEMC20222":
        n = random.randint(5, 12)
        return ProblemEMC20222(n)

    def get_solution(self):
        return get_solution(self.n)
