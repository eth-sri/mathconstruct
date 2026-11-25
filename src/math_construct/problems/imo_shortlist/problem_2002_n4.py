from math_construct.problems.templates import TEMPLATES
PROBLEM_TEMPLATE = TEMPLATES["imo_shortlist/problem_2002_n4.py"]

import random
from fractions import Fraction
from math_construct.problems.problem import Problem, ProblemConfig, Tag, CheckerTag


FORMATTING_INSTRUCTIONS = r"""Output $k$ comma-separated tuples inside of \boxed{}, e.g. \boxed{(20, 2, 3, 4), (20, 6, 7, 8)}."""

def get_solution(k: int) -> list[int]:
    a = [1, 1, 1]
    for _ in range(k-1):
        a.append((a[-1]*a[-2]+1)//a[-3])
    res = []
    for i in range(k):
        res.append([12, a[i], a[i+1], a[i+2]])
    return res

class Problem19(Problem):
    config = ProblemConfig(
        name=Problem.get_name(__file__),
        statement=PROBLEM_TEMPLATE,
        formatting_instructions=FORMATTING_INSTRUCTIONS,
        parameters=["k"],
        source="IMO 2002 Shortlist N4",
        original_parameters={"k": 15},
        original_solution=get_solution(15),
        tags=[Tag.NUMBER_THEORY, Tag.FIND_INF, Tag.IS_SIMPLIFIED],
        problem_url="https://anhngq.wordpress.com/wp-content/uploads/2010/07/imo-2002-shortlist.pdf#page=6",
        solution_url="https://anhngq.wordpress.com/wp-content/uploads/2010/07/imo-2002-shortlist.pdf#page=6",
    )
    k: int

    def __init__(self, k: int):
        self.k = k

    def get_problem(self):
        return PROBLEM_TEMPLATE.format(k=self.k)

    def check(self, solution: list[list[int]]) -> bool:
        if len(solution) != self.k:
            return False, f"List of size {len(solution)}, should be {self.k}", CheckerTag.INCORRECT_LENGTH
        # check if all are integers
        for s in solution:
            if not all(isinstance(x, int) and x > 0 for x in s):
                return False, "All elements should be integers", CheckerTag.INCORRECT_FORMAT
        # check if all are unique
        if len(set(tuple(s) for s in solution)) != len(solution):
            return False, "All elements should be unique", CheckerTag.INCORRECT_SOLUTION
        # check if all m are the same
        m_set = set(m for m, _, _, _ in solution)
        if len(m_set) != 1:
            return False, "All elements should have the same m", CheckerTag.INCORRECT_SOLUTION
        # check if all are sorted
        for m, a, b, c in solution:
            if a > b or b > c:
                return False, f"Found {a}, {b}, {c} which is not sorted", CheckerTag.INCORRECT_SOLUTION
            lhs = Fraction(1, a) + Fraction(1, b) + Fraction(1, c) + Fraction(1, a*b*c)
            rhs = Fraction(m, a + b + c)
            if lhs != rhs:
                return False, f"Equation is not satisfied for {m}, {a}, {b}, {c}", CheckerTag.INCORRECT_SOLUTION
        return True, "OK", CheckerTag.CORRECT

    @staticmethod
    def generate() -> "Problem19":
        k = random.randint(11, 21)
        return Problem19(k)

    def get_solution(self):
        return get_solution(self.k)
