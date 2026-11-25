from math_construct.problems.templates import TEMPLATES
PROBLEM_TEMPLATE = TEMPLATES["dutch/problem_2019_2.py"]

import math
import random
import sympy
from fractions import Fraction
from math_construct.problems.problem import Problem, ProblemConfig, Tag, CheckerTag

MATRIX_FORMATTING_TEMPLATE = r"""Output each configuration between \verb|\begin{array}{...}| and \verb|\end{array}|. All configurations should appear inside of a single $\boxed{...}$. For example, $\boxed{\begin{array}{ccc}0 & 1 & 0 \\ 1 & 0 & 0 \\ 0 & 0 & 0\end{array},\begin{array}{cc}0 & 1 \\ 1 & 0\end{array}}$."""


def get_solution(n: int):
    solutions = []
    first_solution = [[1 if (i < n and j >= n) or (i >= n and j < n) else 0 for j in range(2 * n)] for i in range(2 * n)]
    solutions.append(first_solution)
    second_solution = [[0 if i == j else 1 for j in range(n+1)] for i in range(n+1)]
    solutions.append(second_solution)
    if n % 2 == 0:
        third_solution = [[0 if (abs(i - j) == 1 and ((i + j) % 4 == 1)) or i == j  else 1 for j in range(n + 2)] for i in range(n + 2)]
        solutions.append(third_solution)
    return solutions

class ProblemDutch20192(Problem):
    config = ProblemConfig(
        name=Problem.get_name(__file__),
        statement=PROBLEM_TEMPLATE,
        formatting_instructions=MATRIX_FORMATTING_TEMPLATE + "\nThe element in the $i$-th row and $j$-th column should be 1 if guest $i$ is friends with guest $j$, and 0 otherwise. Elements on the diagonal should be 0.",
        parameters=["k", "n"],
        source="Dutch Math Olympiad Finals 2019 P2",
        original_parameters={"k": 4, "n": 3},
        problem_url="https://wiskundeolympiade.nl/phocadownload/opgaven/finale/2019/ProblemsKlas6.pdf",
        solution_url="https://wiskundeolympiade.nl/phocadownload/opgaven/finale/2019/Solutions.pdf",
        original_solution=get_solution(4),
        tags=[Tag.IS_ORIGINAL, Tag.IS_GENERALIZED, Tag.COMBINATORICS, Tag.FIND_ALL]
    )
    k: int
    n: int

    def __init__(self, k: int, n: int):
        self.k = k
        self.n = n

    def get_problem(self):
        return PROBLEM_TEMPLATE.format(k=self.k, n=self.n)
    
    def check_single(self, matrix: list[int]) ->bool:
        for i in range(len(matrix)):
            for j in range(i):
                if matrix[i][j] != matrix[j][i]:
                    return False, f"The friendship between guest {i} and guest {j} in {matrix} should be mutual."
            if matrix[i][i] != 0:
                return False, f"A guest cannot be friends with themselves, but guest {i} in {matrix} is."
        n_friends = [sum(row) for row in matrix]
        if not all([x == self.k for x in n_friends]):
            return False, f"Each guest should have exactly {self.k} friends."
        for i in range(len(matrix)):
            for j in range(len(matrix)):
                for k in range(len(matrix)):
                    if matrix[i][j] == 0 and matrix[i][k] == 0 and matrix[j][k] == 1:
                        return False, f"If guest {i} is not friends with guest {j} and guest {k} is friends with guest {j}, then guest {k} should not be friends with guest {i}, but this is the case in {matrix}."
        return True, "OK"

    def check(self, a: list[list[int]]) -> bool:
        lengths = [len(x) for x in a]
        if len(a) != self.n or len(set(lengths)) != self.n:
            return False, f"There should be {self.n} different configurations.", CheckerTag.INCORRECT_LENGTH
        checker_format = [self.check_format(sol, is_integer=True, is_square_matrix=True, min_val_inclusive=0, max_val_inclusive=1) for sol in a]
        for is_valid, reason, tag in checker_format:
            if not is_valid:
                return is_valid, reason, tag
        
        for x in a:
            is_valid, reason = self.check_single(x)
            if not is_valid:
                return False, reason, CheckerTag.INCORRECT_SOLUTION
        return True, "OK", CheckerTag.CORRECT

    @staticmethod
    def generate() -> "ProblemDutch20192":
        k = random.randint(4, 8)
        if k % 2 == 0 and k > 2:
            n = 3
        else:
            n = 2
        return ProblemDutch20192(k, n)
    
    def get_solution(self) -> list[list[int]]:
        return get_solution(self.k)[:self.n]
