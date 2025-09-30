from math_construct.problems.templates import TEMPLATES
PROBLEM_TEMPLATE = TEMPLATES["swiss/problem_2020_1_selection.py"]

import random
from math_construct.problems.problem import Problem, ProblemConfig, Tag, CheckerTag

LIST_FORMATTING_TEMPLATE = r"""Output the answer as a comma separated list of coordinates inside of $\boxed{...}$. The $i$-th element indicates the coordinates of the square on which the $i$-th move is executed. The squares are labled from $(0,0)$ to $(n-1,n-1)$ and $(0,0)$ is a white square. For instance, $\boxed{(1,0),(0,1)}$ would execute the first 2 moves on the squares $(1,0)$ and $(0,1)$."""


def get_solution(n):
    moves = []
    for i in range(1, n, 2):
        moves += [[j, j + i] for j in range(n) if max(j, j + i) < n]
    for i in range(n - 1, 0, -2):
        moves += [[j + i, j] for j in range(n) if max(j, j + i) < n]
    return moves

class ProblemSwissSelection20201(Problem):
    config = ProblemConfig(
        name=Problem.get_name(__file__),
        statement=PROBLEM_TEMPLATE,
        formatting_instructions=LIST_FORMATTING_TEMPLATE,
        parameters=["n"],
        problem_url="https://mathematical.olympiad.ch/fileadmin/user_upload/Archiv/Intranet/Olympiads/Mathematics/deploy/exams/2020/Selection/MasterSolution/selectionSolution2020.pdf#page=1",
        solution_url="https://mathematical.olympiad.ch/fileadmin/user_upload/Archiv/Intranet/Olympiads/Mathematics/deploy/exams/2020/Selection/MasterSolution/selectionSolution2020.pdf#page=1",
        source="Swiss Math Olympiad IMO Selection 2020",
        original_parameters={"n": 6},
        original_solution=get_solution(6),
        tags=[Tag.IS_SIMPLIFIED, Tag.FIND_ANY, Tag.COMBINATORICS] 
    )
    n: int

    def __init__(self, n: int):
        self.n = n

    def get_problem(self):
        return PROBLEM_TEMPLATE.format(n=self.n)
        
    def check(self, a: list[int]) -> bool:
        checker = self.check_format(a, is_integer=True, is_matrix=True, 
                                    expected_size_all_axes=[None, 2])
        if not checker[0]:
            return checker
        if any(x < 0 or x >= self.n for y in a for x in y):
            return False, "The coordinates must be inside the board.", CheckerTag.INCORRECT_FORMAT
        
        board = [[(i + j) % 2 for i in range(self.n)] for j in range(self.n)]

        for x, y in a:
            for i in range(self.n):
                board[x][i] = 1 - board[x][i]
                board[i][y] = 1 - board[i][y]
            board[x][y] = 1 - board[x][y]
        
        if any(1 in x for x in board) and any(0 in x for x in board):
            return False, "The board is not monochrome.", CheckerTag.INCORRECT_SOLUTION
        return True, "OK", CheckerTag.CORRECT

    @staticmethod
    def generate() -> "ProblemSwissSelection20201":
        n = 2 * random.randint(2, 5)
        return ProblemSwissSelection20201(n)
    
    def get_solution(self) -> list[list[int]]:
        return get_solution(self.n)
    
