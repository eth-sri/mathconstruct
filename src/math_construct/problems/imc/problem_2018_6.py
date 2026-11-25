from math_construct.problems.templates import TEMPLATES
PROBLEM_TEMPLATE = TEMPLATES["imc/problem_2018_6.py"]

import random
import numpy as np
from math_construct.problems.problem import Problem, ProblemConfig, Tag, CheckerTag
from math_construct.templates import get_matrix_template


def get_solution(n: int, k: int):
    A = [[0]*k for _ in range(n)]
    for col_idx in range(k):
        row_idx = col_idx//2
        A[row_idx][col_idx] = 1
    return A


class Problem_IMC_2018_6(Problem):
    config = ProblemConfig(
        name=Problem.get_name(__file__),
        statement=PROBLEM_TEMPLATE,
        formatting_instructions=get_matrix_template(),
        parameters=["n", "k"],
        source="IMC 2018 P6",
        original_parameters={"n": 6, "k": 10},
        original_solution=get_solution(6, 10),
        problem_url="https://www.imc-math.org.uk/imc2018/imc2018-day2-solutions.pdf#page=1",
        solution_url="https://www.imc-math.org.uk/imc2018/imc2018-day2-solutions.pdf#page=1",
        tags=[Tag.ALGEBRA, Tag.FIND_MAX_MIN, Tag.IS_SIMPLIFIED],
    )
    n: int
    k: int

    def __init__(self, n: int, k: int):
        self.n = n
        self.k = k

    def get_problem(self):
        return PROBLEM_TEMPLATE.format(n=self.n, k=self.k)

    def check(self, x: list[list[float]]):
        if len(x) != self.n:
            return False, f"The number of rows is not equal to n ({self.n}).", CheckerTag.INCORRECT_FORMAT
        if any(len(row) != self.k for row in x):
            return False, f"The number of columns is not equal to k ({self.k}).", CheckerTag.INCORRECT_FORMAT
        x = np.array(x)
        for i in range(self.k):
            if np.linalg.norm(x[:, i]) < 1e-3:
                return False, f"Column {i} is zero.", CheckerTag.INCORRECT_SOLUTION
        for i in range(self.k):
            for j in range(self.k):
                if abs(i-j) <= 1:
                    continue
                if abs(np.dot(x[:, i], x[:, j])) > 1e-3 * min(1, np.linalg.norm(x[:, i]) * np.linalg.norm(x[:, j])):
                    return False, f"Columns {i} and {j} are not orthogonal.", CheckerTag.INCORRECT_SOLUTION
        return True, "OK", CheckerTag.CORRECT

    @staticmethod
    def generate() -> "Problem_IMC_2018_6":
        k = random.randint(8,20)
        n = random.randint((k+1)//2, (k+1)//2+4)
        return Problem_IMC_2018_6(n, k)

    def get_solution(self):
        return get_solution(self.n, self.k)
