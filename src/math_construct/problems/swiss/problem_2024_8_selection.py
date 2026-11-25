from math_construct.problems.templates import TEMPLATES
PROBLEM_TEMPLATE = TEMPLATES["swiss/problem_2024_8_selection.py"]

import math
import random
import sympy
from math_construct.problems.problem import Problem, ProblemConfig, Tag, CheckerTag
from math_construct.utils import latex2sympy_fixed
import sys


class ProblemSwissSelection20248(Problem):
    config = ProblemConfig(
        name=Problem.get_name(__file__),
        statement=PROBLEM_TEMPLATE,
        formatting_instructions=r"Write a valid LaTeX function in function of the variable $x$ that does not contain $f(x)$ inside \boxed. For instance, \boxed{x^2} or \boxed{e^x}.",
        parameters=[],
        source="Swiss Math Olympiad IMO Selection 2024",
        problem_url="https://mathematical.olympiad.ch/fileadmin/user_upload/Archiv/Intranet/Olympiads/Mathematics/deploy/exams/2024/Selection/MasterSolution/selectionSolution2024.pdf#page=23",
        solution_url="https://mathematical.olympiad.ch/fileadmin/user_upload/Archiv/Intranet/Olympiads/Mathematics/deploy/exams/2024/Selection/MasterSolution/selectionSolution2024.pdf#page=23",
        original_parameters=dict(),
        original_solution=r"\frac{1}{x}",
        tags=[Tag.IS_ORIGINAL, Tag.ALGEBRA, Tag.FIND_ANY]
    )

    def __init__(self):
        pass

    def get_problem(self):
        return PROBLEM_TEMPLATE
        
    def check(self, a: str) -> bool:
        if "=" in a:
            a = a[a.rfind("=") + 1:]
        sympy_expression = latex2sympy_fixed(a)
        if sympy_expression is None:
            return False, "Invalid LaTeX expression.", CheckerTag.INCORRECT_FORMAT
        x = sympy.symbols("x")
        f_x_times_x = x * sympy_expression # simple automatic check if this is constant
        simplified = sympy.simplify(f_x_times_x)
        if simplified.free_symbols:
            return False, "Function does not satisfy the inequality.", CheckerTag.INCORRECT_SOLUTION
        if simplified.is_positive is not True:
            return False, "f must map R_{>0} to R_{>0}", CheckerTag.INCORRECT_SOLUTION
        return True, "OK", CheckerTag.CORRECT

    @classmethod
    def has_variations(cls):
        return False

    @staticmethod
    def generate() -> "ProblemSwissSelection20248":
        return ProblemSwissSelection20248()
    
    def get_solution(self):
        return r"\frac{1}{x}"
