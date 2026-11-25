from math_construct.problems.templates import TEMPLATES
PROBLEM_TEMPLATE = TEMPLATES["imo_shortlist/problem_2000_c4.py"]

from math_construct.problems.problem import Problem, ProblemConfig, Tag, CheckerTag
from math_construct.templates import get_matrix_template
import random


MATRIX_FORMATTING_TEMPLATE = r"""Output the answer as $n \times n$ matrix consisting of 0s (no pawn) and 1s (pawn) formatted using \verb|\begin{array}{...}| and \verb|\end{array}| inside of $\boxed{...}$. For example, $\boxed{\begin{array}{ccc}0 & 0 & 1 \\ 1 & 0 & 0 \\ 1 & 0 & 0\end{array}}$."""

def get_solution(n: int, k: int) -> list[list[int]]:
    a = []
    for i in range(n):
        row = [0]*n
        for j in range(n):
            if i+j in [k-1, 2*k-1, 3*k-1]:
                row[j] = 1
        a.append(row)
    return a

class Problem2000C4(Problem):
    config = ProblemConfig(
        name=Problem.get_name(__file__),
        statement=PROBLEM_TEMPLATE,
        formatting_instructions=MATRIX_FORMATTING_TEMPLATE,
        parameters=["n", "k"],
        source="IMO 2000 Shortlist C4",
        original_parameters={"n": 10, "k": 5},
        original_solution=get_solution(10, 5),
        tags=[Tag.COMBINATORICS, Tag.FIND_MAX_MIN, Tag.IS_SIMPLIFIED],
        problem_url="https://prase.cz/kalva/short/soln/sh00c4.html",
        solution_url="https://prase.cz/kalva/short/soln/sh00c4.html",
    )
    n: int
    k: int

    def __init__(self, n: int, k: int):
        self.n = n
        self.k = k

    def get_problem(self):
        return PROBLEM_TEMPLATE.format(n=self.n, k=self.k, m=4*(self.n-self.k))

    def check(self, x: list[list[int]]) -> bool:
        if len(x) != self.n:
            return False, f"List of size {len(x)}, should be {self.n}", CheckerTag.INCORRECT_LENGTH
        for row in x:
            if len(row) != self.n:
                return False, f"Row of size {len(row)}, should be {self.n}", CheckerTag.INCORRECT_LENGTH
        if any(y not in (0, 1) for row in x for y in row):
            return False, "Entries must be 0 or 1", CheckerTag.INCORRECT_FORMAT
        cnt_1 = sum(row.count(1) for row in x)
        if cnt_1 != 4*(self.n-self.k):
            return False, f"Number of 1s is {cnt_1}, should be {4*(self.n-self.k)}", CheckerTag.INCORRECT_SOLUTION
        for i in range(self.n):
            row = x[i]
            s = "".join(str(y) for y in row)
            max_group = max(len(g) for g in s.split("1"))
            if max_group >= self.k:
                return False, f"Row {row} has a group of length {max_group}, should be less than {self.k}", CheckerTag.INCORRECT_SOLUTION
        for j in range(self.n):
            s = "".join(str(x[i][j]) for i in range(self.n))
            max_group = max(len(g) for g in s.split("1"))
            if max_group >= self.k:
                return False, f"Column {j} has a group of length {max_group}, should be less than {self.k}", CheckerTag.INCORRECT_SOLUTION
        return True, "OK", CheckerTag.CORRECT

    @staticmethod
    def generate() -> "Problem2000C4":
        n = random.randint(9, 25)
        k = random.randint(n//2+1, 2*n//3)
        return Problem2000C4(n, k)

    def get_solution(self):
        return get_solution(self.n, self.k)
