from math_construct.problems.templates import TEMPLATES
PROBLEM_TEMPLATE = TEMPLATES["usamts/problem_1999_1_2.py"]

import random
from math_construct.problems.problem import Problem, ProblemConfig, Tag, CheckerTag
from math_construct.templates import get_list_template


def get_solution(k: int) -> list[int]:
    return [2, 3, (10**k-1)//9, (5*10**(k-1)+1)//3]

class Problem7(Problem):
    config = ProblemConfig(
        name=Problem.get_name(__file__),
        statement=PROBLEM_TEMPLATE,
        formatting_instructions=get_list_template(),
        parameters=["k"],
        source="USAMTS 99/00 Round 1",
        original_parameters={"k": 1999},
        original_solution=[2, 3, (10**1999-1)//9, (5*10**1998+1)//3],
        problem_url="https://files.usamts.org/Problems_11_1.pdf",
        solution_url="https://files.usamts.org/Solutions_11_1.pdf",
        tags=[Tag.NUMBER_THEORY, Tag.IS_ORIGINAL, Tag.IS_GENERALIZED, Tag.FIND_ANY]
    )
    k: int

    def __init__(self, k: int):
        self.k = k

    def get_problem(self):
        return PROBLEM_TEMPLATE.format(k=self.k)

    def check(self, x: list[int]):
        if not all(isinstance(y, int) for y in x):
            return False, "All elements should be integers", CheckerTag.INCORRECT_FORMAT
        if len(x) != 4 or any(y <= 1 for y in x):
            return False, "Need four integers greater than 1", CheckerTag.INCORRECT_SOLUTION
        a, b, c, d = x
        if a*b*c*d != int("1"*self.k + "2"*self.k):
            return False, f"{a}*{b}*{c}*{d} does not equal {self.k} digits of 1 followed by {self.k} digits of 2", CheckerTag.INCORRECT_SOLUTION            
        return True, "OK", CheckerTag.CORRECT

    @staticmethod
    def generate() -> "Problem7":
        k = random.randint(50, 1000)
        return Problem7(k)

    def get_solution(self) -> list[int]:
        return get_solution(self.k)
