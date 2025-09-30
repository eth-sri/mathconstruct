from math_construct.problems.templates import TEMPLATES
PROBLEM_TEMPLATE = TEMPLATES["imo_shortlist/problem_2016_c4.py"]

from fractions import Fraction
from math_construct.problems.problem import Problem, ProblemConfig, Tag, CheckerTag
from math_construct.templates import get_matrix_template
import math
import random


def get_solution(n: int) -> list[str]:
    a = []
    for i in range(n):
        row = ""
        for j in range(n):
            idx = (i + (j//3))%3
            row += "IMO"[idx]
        a.append(row)
    return a

class Problem2016C4(Problem):
    config = ProblemConfig(
        name=Problem.get_name(__file__),
        statement=PROBLEM_TEMPLATE,
        formatting_instructions=get_matrix_template(),
        parameters=["n"],
        source="IMO 2016 Shortlist C4",
        original_parameters={"n": 9},
        original_solution=get_solution(9),
        problem_url="https://www.imo-official.org/problems/IMO2016SL.pdf#page=37",
        solution_url="https://www.imo-official.org/problems/IMO2016SL.pdf#page=37",
        tags=[Tag.COMBINATORICS, Tag.IS_SIMPLIFIED, Tag.FIND_ANY],
    )
    n: int

    def __init__(self, n: int):
        self.n = n 

    def get_problem(self):
        return PROBLEM_TEMPLATE.format(n=self.n)
    
    def check(self, a: list[str]) -> tuple[bool, str]:
        def get_diagonal(i: int, j: int, di: int, dj: int) -> str:
            res = ""
            while 0 <= i < self.n and 0 <= j < self.n:
                res += a[i][j]
                i += di
                j += dj
            return res
        if len(a) != self.n:
            return False, f"Number of rows {len(a)} is not equal to {self.n}", CheckerTag.INCORRECT_LENGTH
        for row in a:
            if len(row) != self.n:
                return False, f"Number of columns {len(row)} is not equal to {self.n}", CheckerTag.INCORRECT_LENGTH
            for c in row:
                if c not in "IMO":
                    return False, f"Cell {c} is not in the set {'IMO'}", CheckerTag.INCORRECT_FORMAT
            for i in range(self.n):
                if a[i].count("I") != self.n//3 or a[i].count("M") != self.n//3 or a[i].count("O") != self.n//3:
                    return False, f"Row {a[i]} does not have equal number of I, M and O", CheckerTag.INCORRECT_SOLUTION
            for j in range(self.n):
                col = "".join(a[i][j] for i in range(self.n))
                if col.count("I") != self.n//3 or col.count("M") != self.n//3 or col.count("O") != self.n//3:
                    return False, f"Column {col} does not have equal number of I, M and O", CheckerTag.INCORRECT_SOLUTION

            for di, dj in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
                for i in range(self.n):
                    for start in [(i, 0), (0, i)]:
                        if start[0]+di < 0 or start[1]+dj < 0:
                            continue
                        diag = get_diagonal(start[0], start[1], di, dj)
                        if len(diag)%3 == 0:
                            if diag.count("I") != len(diag)//3 or diag.count("M") != len(diag)//3 or diag.count("O") != len(diag)//3:
                                return False, f"Diagonal starting at ({start[0]}, {start[1]}) with ({di}, {dj}) direction does not have equal number of I, M and O", CheckerTag.INCORRECT_SOLUTION
        return True, "OK", CheckerTag.CORRECT

    @staticmethod
    def generate() -> "Problem2016C4":
        n = 9*random.randint(1, 6)
        return Problem2016C4(n)

    def get_solution(self):
        return get_solution(self.n)
