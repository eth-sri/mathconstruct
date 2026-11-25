from math_construct.problems.templates import TEMPLATES
PROBLEM_TEMPLATE = TEMPLATES["konhauser/problem_2014_7.py"]

import math
import random
from math_construct.problems.problem import Problem, ProblemConfig, Tag, CheckerTag
from math_construct.templates import get_list_template


def get_solution(a: int, b: int, c: int):
    return [math.log(b + c, a), 1]

class ProblemKonhauser20147(Problem):
    config = ProblemConfig(
        name=Problem.get_name(__file__),
        statement=PROBLEM_TEMPLATE,
        formatting_instructions=get_list_template("You can use valid LaTeX expressions to represent the numbers."),
        parameters=["a", "b", "c", "d", "e", "f"],
        source="Konhauser Problemfest 2015 P7",
        original_parameters={"a": 3, "b": 3, "c": 2, "d": 9, "e": 6, "f": 19},
        problem_url="https://www.macalester.edu/mscs/wp-content/uploads/sites/591/2015/01/KP2014.pdf#page=2",
        solution_url="https://www.macalester.edu/mscs/wp-content/uploads/sites/591/2015/01/KP2014.pdf#page=7",
        original_solution=get_solution(3, 3, 2),
        tags=[Tag.IS_SIMPLIFIED, Tag.FIND_ALL, Tag.ALGEBRA, Tag.IS_ORIGINAL, Tag.IS_GENERALIZED]
    )
    a: int
    b: int
    c: int
    d: int
    e: int
    f: int

    def __init__(self, a: int, b: int, c: int, d: int, e: int, f: int):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e
        self.f = f

    def get_problem(self):
        return PROBLEM_TEMPLATE.format(
            a=self.a, b=self.b, c=self.c, d=self.d, e=self.e, f=self.f
        )

    def check(self, sol: list[float]) -> bool:
        checker_format = self.check_format(sol, expected_length=2)
        if not checker_format[0]:
            return checker_format
        x, y = sol
        eq1 = self.a ** x - self.b ** y - self.c ** y
        eq2 = self.d ** x - self.e ** y - self.f ** y
        if abs(eq1) > 0.001 * min(1, max(self.a ** x, self.b ** y + self.c ** y)):
            return False, f"First equation is not satisfied with difference: {eq1}.", CheckerTag.INCORRECT_SOLUTION
        if abs(eq2) > 0.001 * min(1, max(self.d ** x, self.e ** y + self.f ** y)):
            return False, f"Second equation is not satisfied with difference: {eq2}.", CheckerTag.INCORRECT_SOLUTION
        return True, "OK", CheckerTag.CORRECT
        
    @staticmethod
    def generate() -> "ProblemKonhauser20147":
        a, b, c = 2, 1, 1
        while abs(int(math.log(b + c, a)) - math.log(b + c, a)) < 0.00001:
            a = random.randint(2, 8)
            c = random.randint(2, 8)
            b = random.randint(2, 10)
        d = a ** 2
        e = b * c
        f = b ** 2 + c ** 2 + e
        return ProblemKonhauser20147(a=a, b=b, c=c, d=d, e=e, f=f)
    
    def get_solution(self):
        return get_solution(self.a, self.b, self.c)
