from math_construct.problems.templates import TEMPLATES
PROBLEM_TEMPLATE = TEMPLATES["imo_shortlist/problem_2017_n6.py"]

from math_construct.problems.problem import Problem, ProblemConfig, Tag, CheckerTag
from fractions import Fraction
import random


FORMATTING_INSTRUCTIONS = r"""Output a comma-separated list of different triples $(x, y, z)$, inside of \boxed, for example \boxed{(\frac{1}{2},\frac{1}{3},\frac{1}{6}), (\frac{1}{3},\frac{1}{4},\frac{1}{12})}."""

def get_solution(n: int) -> list[int]:
    x = [2, 3]
    ret = []
    i = 0
    while len(ret) < n:
        x.append(3*x[-1] - x[-2] - 1)
        num_digits = len(str(1+x[i]+x[i+1]))
        if num_digits < len(ret)+1:
            i += 1
            continue
        a = Fraction(1, 1+x[i]+x[i+1])
        b = Fraction(x[i], 1+x[i]+x[i+1])
        c = Fraction(x[i+1], 1+x[i]+x[i+1])
        ret.append([a, b, c])
        i += 1
        
    return ret


class Problem2017N6(Problem):
    config = ProblemConfig(
        name=Problem.get_name(__file__),
        statement=PROBLEM_TEMPLATE,
        formatting_instructions=FORMATTING_INSTRUCTIONS,
        parameters=["n"],
        source="IMO 2017 Shortlist N6",
        original_parameters={"n": 10},
        original_solution=get_solution(10),
        problem_url="https://www.imo-official.org/problems/IMO2017SL.pdf#page=84",
        solution_url="https://www.imo-official.org/problems/IMO2017SL.pdf#page=84",
        tags=[Tag.NUMBER_THEORY, Tag.IS_SIMPLIFIED, Tag.FIND_INF]
    )
    n: int

    def __init__(self, n: int):
        self.n = n 

    def get_problem(self):
        return PROBLEM_TEMPLATE.format(n=self.n)
    
    def check(self, a: list[list[Fraction]]):
        if len(a) != self.n:
            return False, f"List of size {len(a)}, should be {self.n}", CheckerTag.INCORRECT_LENGTH
        if len(set(tuple(t) for t in a)) != len(a):
            return False, "Triples are not different", CheckerTag.INCORRECT_SOLUTION
        for i, (x, y, z) in enumerate(a):
            if not (x > 0 and y > 0 and z > 0):
                return False, "Triple has non-positive entry", CheckerTag.INCORRECT_SOLUTION
            c = [x.numerator, x.denominator, y.numerator, y.denominator, z.numerator, z.denominator]
            if all(len(str(c[j])) < i+1 for j in range(6)):
                return False, f"For i={i}, all of {x}, {y}, {z} have numerator and denominator with less than {i+1} digits", CheckerTag.INCORRECT_SOLUTION
            if not (x + y + z).is_integer():
                return False, f"Sum of {x}, {y}, {z} is not 1", CheckerTag.INCORRECT_SOLUTION
            if not (1/x + 1/y + 1/z).is_integer():
                return False, f"Sum of {1/x}, {1/y}, {1/z} is not 1", CheckerTag.INCORRECT_SOLUTION
        return True, "OK", CheckerTag.CORRECT
    
    @staticmethod
    def generate() -> "Problem2017N6":
        n = random.randint(5, 25)
        return Problem2017N6(n)

    def get_solution(self):
        return get_solution(self.n)
