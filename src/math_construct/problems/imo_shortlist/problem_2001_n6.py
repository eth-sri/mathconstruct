from math_construct.problems.templates import TEMPLATES
PROBLEM_TEMPLATE = TEMPLATES["imo_shortlist/problem_2001_n6.py"]

import random

from math_construct.problems.problem import Problem, ProblemConfig, Tag, CheckerTag
from math_construct.templates import get_list_template


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def get_largest_prime_le(n: int) -> int:
    for i in range(n, 1, -1):
        if is_prime(i):
            return i
    return 2

def get_solution(p: int, n: int) -> list[int]:
    # Find largest prime <= sqrt(n//2)
    q = get_largest_prime_le(int((n//2)**0.5))
    f = [2*q*i + i*i%q for i in range(1,q+1)]
    return f[:p]


class Problem20(Problem):
    config = ProblemConfig(
        name=Problem.get_name(__file__),
        statement=PROBLEM_TEMPLATE,
        formatting_instructions=get_list_template(),
        parameters=["p", "n"],
        source="IMO 2001 Shortlist N6",
        original_parameters={"p": 100, "n": 25000},
        original_solution=get_solution(100, 25000),
        tags=[Tag.NUMBER_THEORY, Tag.IS_ORIGINAL, Tag.FIND_ANY, Tag.IS_GENERALIZED],
        problem_url="https://olympiads.win.tue.nl/imo/imo2001/imo2001-shortlist.pdf#page=70",
        solution_url="https://olympiads.win.tue.nl/imo/imo2001/imo2001-shortlist.pdf#page=70",
    )
    p: int
    n: int

    def __init__(self, p: int, n: int):
        self.p = p
        self.n = n

    def get_problem(self):
        return PROBLEM_TEMPLATE.format(p=self.p, n=self.n)

    def check(self, solution: list[int]) -> bool:
        if len(solution) != self.p:
            return False, f"List of size {len(solution)}, should be {self.p}", CheckerTag.INCORRECT_LENGTH
        if not all(isinstance(x, int) and 0 < x <= self.n for x in solution):
            return False, "All elements should be positive integers", CheckerTag.INCORRECT_FORMAT
        sums = set()
        for i in range(len(solution)):
            for j in range(i+1, len(solution)):
                curr_sum = solution[i] + solution[j]
                if curr_sum in sums:
                    return False, f"Sum of pairs {i} and {j} is already in the list", CheckerTag.INCORRECT_SOLUTION
                sums.add(curr_sum)
        return True, "OK", CheckerTag.CORRECT

    @staticmethod
    def generate() -> "Problem20":
        # n = random.randint(100, 50000)
        # maxp = get_largest_prime_le(int((n//2)**0.5))
        # p = random.randint(maxp//2, maxp)
        # ^ mostly bad

        # n = random.randint(25000, 50000)
        # maxp = get_largest_prime_le(int((n//2)**0.5))
        # p = random.randint(int(maxp*0.9), maxp)
        # ^ mostly good but not 100% so let's hardcode

        safe_pairs = [
            (92, 20000), (95, 20000), (97, 20000), (98, 25000), (100, 25000), 
            (109, 25000), (107, 30000), (113, 30000), (117, 35000), (124, 35000),
            (131, 35000), (125, 40000), (132, 40000), (139, 40000), (134, 45000),
            (141, 45000), (149, 45000), (141, 50000), (149, 50000), (157, 50000)
        ]
        p, n = random.choice(safe_pairs) 
        assert Problem20(p, n).check_raw(get_solution(p, n))
        return Problem20(p, n)

    def get_solution(self):
        return get_solution(self.p, self.n)
