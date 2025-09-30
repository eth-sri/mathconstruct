from math_construct.problems.templates import TEMPLATES
PROBLEM_TEMPLATE = TEMPLATES["usamo/problem_2002_5.py"]

import random
from math_construct.problems.problem import Problem, ProblemConfig, Tag, CheckerTag
from math_construct.templates import get_list_template


def check_consecutive(n1, n2):
    return (n1 * n2) % (n1 + n2) == 0

def is_trivial(a, b):
    """Checks if there is some trivial length 3 or 4 solution."""
    for c in range(1, a*b):
        if check_consecutive(a, c) and check_consecutive(c, b):
            return True
    for c1 in range(1, 2*max(a, b)):
        for c2 in range(1, 2*max(a, b)):
            if check_consecutive(a, c1) and check_consecutive(c1, c2) and check_consecutive(c2, b):
                return True
    return False


def get_double(n: int) -> list[int]:
    """Gets path from n to 2n"""
    res = [n, n*(n-1), n*(n-1)*(n-2), n*(n-2), 2*n]
    for i in range(len(res)-1):
        if res[i]*res[i+1] % (res[i] + res[i+1]) != 0:
            assert False
    return res

def get_path(n: int) -> list[int]:
    """Gets path from n to n-1"""
    res = [n, n*(n-1), n*(n-1)*(n-2), n*(n-1)*(n-2)*(n-3)] + list(reversed(get_double((n-1)*(n-2)))) + [n-1]
    for i in range(len(res)-1):
        if res[i]*res[i+1] % (res[i] + res[i+1]) != 0:
            assert False
    return res

def get_solution(a: int, b: int) -> list[int]:
    res = [a]
    if a > b:
        for n in range(a, b, -1):
            res.extend(get_path(n)[1:])
    else:
        for n in range(a, b):
            path = list(reversed(get_path(n+1)))
            res.extend(path[1:])
    return res
    

class Problem_USAMO_2002_5(Problem):
    """2002 USAMO Problem 5"""
    config = ProblemConfig(
        name=Problem.get_name(__file__),
        statement=PROBLEM_TEMPLATE,
        formatting_instructions=get_list_template(),
        parameters=["a", "b"],
        source="2002 USAMO Problem 5",
        original_parameters={"a": 22, "b": 15},
        original_solution=get_solution(22, 15),
        tags=[Tag.NUMBER_THEORY, Tag.FIND_ANY, Tag.IS_SIMPLIFIED],
        problem_url="https://artofproblemsolving.com/wiki/index.php/2002_USAMO_Problems/Problem_5",
        solution_url="https://artofproblemsolving.com/wiki/index.php/2002_USAMO_Problems/Problem_5",
    )
    a: int
    b: int

    def __init__(self, a: int, b: int):
        self.a = a
        self.b = b

    def get_problem(self):
        return PROBLEM_TEMPLATE.format(a=self.a, b=self.b)

    def check(self, x: list[int]) -> tuple[bool, str, CheckerTag]:
        if not all(isinstance(y, int) for y in x):
            return False, "All elements should be integers", CheckerTag.INCORRECT_FORMAT
        if x[0] != self.a:
            return False, f"First element should be {self.a}, but it is {x[0]}", CheckerTag.INCORRECT_FORMAT
        if x[-1] != self.b:
            return False, f"Last element should be {self.b}, but it is {x[-1]}", CheckerTag.INCORRECT_FORMAT
        for i in range(len(x)-1):
            if x[i]*x[i+1] % (x[i] + x[i+1]) != 0:
                return False, f"Product of {x[i]} and {x[i+1]} is not divisible by their sum: {x[i]*x[i+1]} is not divisible by {x[i] + x[i+1]}", CheckerTag.INCORRECT_SOLUTION
        return True, "OK", CheckerTag.CORRECT

    @staticmethod
    def generate() -> "Problem_USAMO_2002_5":
        while True:
            a = random.randint(10, 40)
            b = random.randint(10, 40)
            if not is_trivial(a, b):
                break
        return Problem_USAMO_2002_5(a, b)

    def get_solution(self):
        return get_solution(self.a, self.b)
