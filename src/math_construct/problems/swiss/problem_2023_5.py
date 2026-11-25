from math_construct.problems.templates import TEMPLATES
PROBLEM_TEMPLATE = TEMPLATES["swiss/problem_2023_5.py"]

import sympy
from math_construct.problems.problem import Problem, ProblemConfig, Tag, CheckerTag
from math_construct.utils import latex2sympy_fixed


class ProblemSwiss20235(Problem):
    config = ProblemConfig(
        name=Problem.get_name(__file__),
        statement=PROBLEM_TEMPLATE,
        formatting_instructions=r"Write a valid LaTeX function in function of the variable $x$ that does not contain $f(x)$ or $D$ inside \boxed. For instance, \boxed{x^2} or \boxed{e^x}.",
        parameters=[],
        source="Swiss Math Olympiad Finals 2023",
        original_parameters=dict(),
        problem_url="https://mathematical.olympiad.ch/fileadmin/user_upload/Archiv/Intranet/Olympiads/Mathematics/deploy/exams/2023/FinalRound/MasterSolution/finalRoundSolution2023.pdf#page=8",
        solution_url="https://mathematical.olympiad.ch/fileadmin/user_upload/Archiv/Intranet/Olympiads/Mathematics/deploy/exams/2023/FinalRound/MasterSolution/finalRoundSolution2023.pdf#page=8",
        original_solution=r"\frac{1-x}{1+x}",
        tags=[Tag.IS_ORIGINAL, Tag.FIND_ANY, Tag.ALGEBRA, Tag.IS_SIMPLIFIED]
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
        f_x_times_x = (1 + x) * sympy_expression + x # simple automatic check if this is constant
        simplified = sympy.simplify(f_x_times_x)
        if simplified.free_symbols or simplified != 1:
            return False, "Function does not satisfy the inequality.", CheckerTag.INCORRECT_SOLUTION
        return True, "OK", CheckerTag.CORRECT

    @classmethod
    def has_variations(cls):
        return False

    @staticmethod
    def generate() -> "ProblemSwiss20235":
        return ProblemSwiss20235()
    
    def get_solution(self):
        return r"\frac{1-x}{1+x}"
