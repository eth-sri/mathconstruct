from math_construct.problems.templates import TEMPLATES
PROBLEM_TEMPLATE = TEMPLATES["usamts/problem_1998_1_4.py"]

from math_construct.problems.problem import Problem, ProblemConfig, Tag, CheckerTag
from math import sqrt
import random



LIST_FORMATTING_TEMPLATE = r"""Output the answer as a comma separated list of 7 coordinates inside of $\boxed{...}$. For example $\boxed{(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7)}$."""

class Problem_USAMTS_1998_1_4(Problem):
    config = ProblemConfig(
        name=Problem.get_name(__file__),
        statement=PROBLEM_TEMPLATE,
        formatting_instructions=LIST_FORMATTING_TEMPLATE,
        parameters=["d"],
        source="USAMTS 98/99 Round 4",
        original_parameters={"d": 1},
        original_solution=[
            [0,0],
            [1,0],
            [0.5,sqrt(3)/2],
            [1.5,sqrt(3)/2],
            [0.771286, 1.550844],
            [-0.062046, 0.998073],
            [0.833333, 0.552770],
        ],
        problem_url="https://files.usamts.org/Problems_10_1.pdf",
        solution_url="https://files.usamts.org/Solutions_10_1.pdf",
        tags=[Tag.GEOMETRY, Tag.FIND_ANY, Tag.IS_GENERALIZED],
    )

    def __init__(self, d: int):
        self.d = d

    def get_problem(self):
        return PROBLEM_TEMPLATE.format(d=self.d)

    def check(self, solution: list[float]) -> bool:
        if len(solution) != 7:
            return False, f"List of size {len(solution)}, should be 7", CheckerTag.INCORRECT_LENGTH
        assert all(len(p) == 2 for p in solution)
        for i in range(7):
            for j in range(i + 1, 7):
                for k in range(j + 1, 7):
                    d1 = (solution[i][0] - solution[j][0]) ** 2 + (solution[i][1] - solution[j][1]) ** 2
                    d2 = (solution[i][0] - solution[k][0]) ** 2 + (solution[i][1] - solution[k][1]) ** 2
                    d3 = (solution[j][0] - solution[k][0]) ** 2 + (solution[j][1] - solution[k][1]) ** 2
                    if abs(d1-self.d**2) > 1e-3 and abs(d2-self.d**2) > 1e-3 and abs(d3-self.d**2) > 1e-3:
                        return False, f"Distance between points {i}, {j}, {k} is not {self.d}", CheckerTag.INCORRECT_SOLUTION
        return True, "OK", CheckerTag.CORRECT

    @staticmethod
    def generate() -> "Problem_USAMTS_1998_1_4":
        d = random.randint(2, 10)
        return Problem_USAMTS_1998_1_4(d)

    def get_solution(self):
        solution = self.config.original_solution
        return [[p[0]*self.d, p[1]*self.d] for p in solution]
