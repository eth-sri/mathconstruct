from math_construct.problems.templates import TEMPLATES
PROBLEM_TEMPLATE = TEMPLATES["bulgarian/problem_pms_2008_8_3.py"]

from math_construct.problems.problem import Problem, ProblemConfig, Tag, CheckerTag
import numpy as np
import random


FORMATTING_INSTRUCTIONS = r"""Output a list of tuples, containing the numbers $n$ and the corresponding $n$-digit number for which $R_{n} = 9 n - 2$. Output the sequences as a list of comma-separated tuples inside of \boxed, e.g. \boxed{(2, 19), (3, 123)}."""


def get_solution(N: int) -> list[int]:
    n = 1
    ex = []
    base_ex = [8, 80, 800]
    while len(ex) < N:
        k = (2**(6*(n//3))*base_ex[n%3] + 1)//9
        ex.append((k, 9*10**(k-1)-1))
        n+=1
    return ex

class ProblemBulPMS2008P8_3(Problem):
    config = ProblemConfig(
        name=Problem.get_name(__file__),
        statement=PROBLEM_TEMPLATE,
        formatting_instructions=FORMATTING_INSTRUCTIONS,
        parameters=["N"],
        source="Bulgarian Spring National Competition 2008 8th Grade P3",
        original_parameters={"N": 5},
        original_solution=get_solution(5),
        problem_url="https://klasirane.com/competitions/PMS/All",
        solution_url="https://klasirane.com/competitions/PMS/All",
        tags=[Tag.NUMBER_THEORY, Tag.FIND_INF, Tag.IS_SIMPLIFIED, Tag.IS_TRANSLATED]
    )
    N: int

    def __init__(self, N: int):
        self.N = N

    def get_problem(self):
        return PROBLEM_TEMPLATE.format(N=self.N)

    def check(self, x: list[tuple[int]]) -> bool:
        if len(x) != self.N:
            return False, f"{self.N} examples expected, received {len(x)}", CheckerTag.INCORRECT_LENGTH
        
        # assert that all are unique
        if len(set([tuple(el) for el in x])) != len(x):
            return False, "All examples should be unique", CheckerTag.INCORRECT_FORMAT
        
        if len(set(el[0] for el in x)) != len(x):
            return False, "All values of n should be distinct", CheckerTag.INCORRECT_FORMAT
        for i, entry in enumerate(x):
            if len(entry) != 2:
                return False, f"Each sequence should contain a pair of example $n$ and an n-digit number", CheckerTag.INCORRECT_FORMAT
            if len(str(entry[1])) != entry[0]:
                return False, f"Example should have {entry[0]} digits.", CheckerTag.INCORRECT_FORMAT
            
        for i, entry in enumerate(x):
            mod = sum([int(i) for i in str(entry[1])])
            if entry[1] % mod != 9*entry[0] - 2:
                return False, f"Example {entry[1]} should be {9*entry[0] - 2} mod {mod}", CheckerTag.INCORRECT_SOLUTION
        return True, "OK", CheckerTag.CORRECT

    @staticmethod
    def generate() -> "ProblemBulPMS2008P8_3":
        N = random.randint(3, 7)
        return ProblemBulPMS2008P8_3(N)

    def get_solution(self):
        return get_solution(self.N)
