from math_construct.problems.templates import TEMPLATES
PROBLEM_TEMPLATE = TEMPLATES["croatian/problem_2014_2.py"]

import random
import math
from math_construct.problems.problem import Problem, ProblemConfig, Tag, CheckerTag
from math_construct.templates import get_matrix_template


FORMATTING_TEMPLATE = r"""You should output your answer as a ${N} \times {N}$ matrix, where the entry in row $i$ and column $j$ is an integer between $1$ and $M$ representing the color of the side/diagonal connecting vertex $i$ and vertex $j$.
 
Output the answer between \verb|\begin{array}{...}| and \verb|\end{array}| inside of $\boxed{...}$. 

For example, $\boxed{\begin{array}{ccc}1 & 1 & 3 \\ 2 & 1 & 1 \\ 2 & 2 & 3\end{array}}$."""

def get_solution(M: int, N: int) -> list[int, int]:
    p = M - 1
    assert p**2 == N
    a = []
    for i in range(N):
        i1, j1 = i//p, i%p
        row = []
        for j in range(N):
            i2, j2 = j//p, j%p
            if i1 == i2:
                row.append(p+1)
                continue
            col = -1
            for k in range(p):
                if ((j1-j2)%p+p)%p == ((i1-i2)*k%p+p)%p:
                    col = k
                    break
            assert col != -1, f"No solution for {i1}, {i2}, {j1}, {j2}"
            row.append(col+1)
        a.append(row)
    return a
    

class Problem_HMO_2014_2(Problem):
    config = ProblemConfig(
        name=Problem.get_name(__file__),
        statement=PROBLEM_TEMPLATE,
        formatting_instructions=FORMATTING_TEMPLATE,
        parameters=["M", "N"],
        source="HMO 2014 2",
        original_parameters={"M": 4, "N": 9},
        original_solution=get_solution(4, 9),
        problem_url="https://natjecanja.math.hr/wp-content/uploads/2015/02/HMO2014_rjesenja.pdf#page=2", # page 2
        solution_url="https://natjecanja.math.hr/wp-content/uploads/2015/02/HMO2014_rjesenja.pdf#page=2", # page 2
        tags=[Tag.COMBINATORICS, Tag.FIND_MAX_MIN, Tag.IS_SIMPLIFIED],
    )
    M: int
    N: int

    def __init__(self, M: int, N: int):
        self.M = M
        self.N = N

    def get_problem(self):
        return PROBLEM_TEMPLATE.format(M=self.M, N=self.N)

    def check(self, a: list[list[int]]):
        if len(a) != self.N or any(len(row) != self.N for row in a):
            return False, f"Matrix is not {self.N}x{self.N}", CheckerTag.INCORRECT_FORMAT
        if any(a[i][j] != a[j][i] for i in range(self.N) for j in range(self.N)):
            return False, "Matrix must be symmetric (one color per side/diagonal)", CheckerTag.INCORRECT_FORMAT
        all_colors = set([a[i][j] for i in range(self.N) for j in range(self.N) if i != j])
        if len(all_colors) != self.M:
            return False, f"Matrix has {len(all_colors)} different colors, but needs exactly {self.M} colors", CheckerTag.INCORRECT_SOLUTION
        for i in range(self.N):
            for j in range(self.N):
                if a[i][j] < 1 or a[i][j] > self.M:
                    return False, f"Entry {i},{j} is not between 1 and {self.M}", CheckerTag.INCORRECT_SOLUTION
        for i in range(self.N):
            for j in range(self.N):
                for k in range(self.N):
                    if i == j or i == k or j == k:
                        continue
                    if len(set([a[i][j], a[j][k], a[k][i]])) == 2:
                        return False, f"Three vertices {i}, {j}, {k} determine a triangle with exactly two colors", CheckerTag.INCORRECT_SOLUTION   
        return True, "OK", CheckerTag.CORRECT

    @staticmethod
    def generate() -> "Problem_HMO_2014_2":
        primes = [2, 3, 5]
        M = random.choice(primes)+1
        N = (M-1)**2
        return Problem_HMO_2014_2(M, N)

    def get_solution(self):
        return get_solution(self.M, self.N)
