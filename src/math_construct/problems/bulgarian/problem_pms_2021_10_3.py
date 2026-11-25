from math_construct.problems.templates import TEMPLATES
PROBLEM_TEMPLATE = TEMPLATES["bulgarian/problem_pms_2021_10_3.py"]

import random
from math_construct.problems.problem import Problem, ProblemConfig, Tag, CheckerTag
from math_construct.templates import get_matrix_template
import numpy as np



def get_solution(N:int) -> list[str]:
    grid = [[N*((i+j) % N) + (i-j+N) % N for i in range(N)] for j in range(N)]
    return grid

class ProblemBulPMS2021P10_3(Problem):
    config = ProblemConfig(
        name=Problem.get_name(__file__),
        statement=PROBLEM_TEMPLATE,
        formatting_instructions=get_matrix_template(),
        parameters=["N"],
        source="Bulgarian Spring National Competition 2021 10th Grade P3",
        original_parameters={"N": 15},
        original_solution=get_solution(15),
        problem_url="https://klasirane.com/competitions/PMS/All",
        solution_url="https://klasirane.com/competitions/PMS/All",
        tags = [Tag.NUMBER_THEORY, Tag.FIND_ANY, Tag.IS_ORIGINAL, Tag.IS_TRANSLATED]
    )
    N: int

    def __init__(self, N: int):
        self.N = N

    def get_problem(self):
        return PROBLEM_TEMPLATE.format(N=self.N)

    def check(self, x: list[list[str]]) -> bool:
        if len(x) != self.N:
            return False, f"Example should contain {self.N} rows", CheckerTag.INCORRECT_LENGTH

        for row in x:
            if len(row) != self.N:
                return False, f"Each row should be of length {self.N}", CheckerTag.INCORRECT_FORMAT
        x_fl = [v for row in x for v in row]
        if any(type(v) != int for v in x_fl):
            return False, "All entries must be integers", CheckerTag.INCORRECT_FORMAT
        if min(x_fl) < 0 or max(x_fl) > self.N**2 - 1 or len(np.unique(x)) != self.N**2:
            return False, f"The example should contain the numbers between 0 and {self.N**2 - 1} exactly once", CheckerTag.INCORRECT_FORMAT
        
        quotients = np.array(x)//self.N
        remainders = np.array(x) % self.N

        for i in range(self.N):
            if len(np.unique(quotients[i])) != self.N:
                return False, f"The cells modulo {self.N} should have distinct quotients at each column and row", CheckerTag.INCORRECT_SOLUTION
            if len(np.unique(quotients[:, i])) != self.N:
                return False, f"The cells modulo {self.N} should have distinct quotients at each column and row", CheckerTag.INCORRECT_SOLUTION
            if len(np.unique(remainders[i])) != self.N:
                return False, f"The cells modulo {self.N} should have distinct remainders at each column and row", CheckerTag.INCORRECT_SOLUTION
            if len(np.unique(remainders[:, i])) != self.N:
                return False, f"The cells modulo {self.N} should have distinct remainders at each column and row", CheckerTag.INCORRECT_SOLUTION
        return True, "OK", CheckerTag.CORRECT

    @staticmethod
    def generate() -> "ProblemBulPMS2021P10_3":
        N = random.randint(3, 7)
        return ProblemBulPMS2021P10_3(2*N+1)

    def get_solution(self):
        return get_solution(self.N)
