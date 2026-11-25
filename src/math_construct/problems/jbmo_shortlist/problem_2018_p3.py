from math_construct.problems.templates import TEMPLATES
PROBLEM_TEMPLATE = TEMPLATES["jbmo_shortlist/problem_2018_p3.py"]

import random
from math_construct.problems.problem import Problem, ProblemConfig, Tag, CheckerTag
import numpy as np
from math_construct.templates import get_list_template


def get_solution(n: int) -> list[int]:
    return np.concatenate([[2, -1, -4] for _ in range(n//3)]).tolist()

class ProblemJBMO2018A3(Problem):
    config = ProblemConfig(
        name=Problem.get_name(__file__),
        statement=PROBLEM_TEMPLATE,
        formatting_instructions=get_list_template(),
        parameters=['n'],
        source="2018 JBMO Shortlist A4",
        original_parameters={'n':120},
        original_solution=get_solution(120),
        problem_url="https://artofproblemsolving.com/community/c6h1879852p12786500",
        solution_url="https://artofproblemsolving.com/community/c6h1879852p12786500",
        tags=[Tag.ALGEBRA, Tag.FIND_ANY, Tag.IS_GENERALIZED]
    )
    n: int

    def __init__(self, n:int):
        self.n = n

    def get_problem(self):
        return PROBLEM_TEMPLATE.format(n=self.n)

    def check(self, x: list[int]) -> bool:
        if len(x) != self.n:
            return False, f"Sequence should be of length {self.n}", CheckerTag.INCORRECT_LENGTH
        if 0 in x:
            return False, "Numbers should be non-zero", CheckerTag.INCORRECT_FORMAT
        if len(set(x)) == 1:
            return False, "Numbers should not all be equal", CheckerTag.INCORRECT_SOLUTION
        arr = np.array(x)
        # k = 2/self.n*np.sum(np.log(abs(arr)))
        # if abs(k-4) < 1e-5:
        #     return False, "Resulting value of $k$ is incorrect"
        
        sums = arr + 4/np.roll(arr,-1)
        if max(sums) - min(sums) > 1e-5:
            return False, "The conditions are not satisfied", CheckerTag.INCORRECT_SOLUTION

        return True, "OK", CheckerTag.CORRECT

    @staticmethod
    def generate() -> "ProblemJBMO2018A3":
        n = random.randint(20, 80)
        return ProblemJBMO2018A3(n*3)

    def get_solution(self):
        return get_solution(self.n)
