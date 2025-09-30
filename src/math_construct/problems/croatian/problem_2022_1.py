from math_construct.problems.templates import TEMPLATES
PROBLEM_TEMPLATE = TEMPLATES["croatian/problem_2022_1.py"]

import random
from math_construct.problems.problem import Problem, ProblemConfig, Tag, CheckerTag
from math_construct.utils import get_latex_array
from math_construct.templates import get_list_template


def get_solution(n: int):
    res = []
    for i in range(n):
        if i%2 == 0:
            res += [2.0**(-i//2)]
        else:
            res += [3.0**((i-1)//2)]
    return res

class Problem_HMO_2022_1(Problem):
    config = ProblemConfig(
        name=Problem.get_name(__file__),
        statement=PROBLEM_TEMPLATE,
        formatting_instructions=get_list_template(),
        parameters=["n"],
        source="HMO 2022 1",
        original_parameters={"n": 20},
        original_solution=get_solution(20),
        problem_url="https://natjecanja.math.hr/wp-content/uploads/2023/05/2022_HMO.pdf#page=1", # page 1
        solution_url="https://natjecanja.math.hr/wp-content/uploads/2023/05/2022_HMO.pdf#page=1", # page 1
        tags=[Tag.NUMBER_THEORY, Tag.FIND_MAX_MIN, Tag.IS_SIMPLIFIED],
    )
    n: int

    def __init__(self, n: int):
        self.n = n
        self.m = n//2 - 1

    def get_problem(self):
        return PROBLEM_TEMPLATE.format(n=self.n, m=self.m)

    def check(self, a: list[float]):
        if len(a) != self.n:
            return False, f"List does not have exactly {self.n} elements", CheckerTag.INCORRECT_LENGTH
        if not all(x > 0 for x in a):
            return False, f"All elements must be positive", CheckerTag.INCORRECT_FORMAT
        a = a + a
        cnt = 0
        for i in range(self.n):
            if abs(a[i]*a[i+3] - (a[i]*a[i+1] + a[i+1]*a[i+2] + a[i+2]*a[i+3])) < 1e-3:
                cnt += 1
        if cnt < self.m:
            return False, f"The equality holds only for {cnt} indices, but need {self.m}", CheckerTag.INCORRECT_SOLUTION
        return True, "OK", CheckerTag.CORRECT

    @staticmethod
    def generate() -> "Problem_HMO_2022_1":
        n = 2*random.randint(8,20)
        return Problem_HMO_2022_1(n)

    def get_solution(self):
        return get_solution(self.n)
