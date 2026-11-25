from math_construct.problems.templates import TEMPLATES
PROBLEM_TEMPLATE = TEMPLATES["bulgarian/problem_ifym_2022_d1_p6_8th.py"]

from math_construct.problems.problem import Problem, ProblemConfig, Tag, CheckerTag
from math_construct.templates import get_list_template
import numpy as np
import random
import math


def get_solution(N:int, n: int) -> list[int]:
    seq = []
    for i in range(N):
        seq.append(n*10**(N+10-i)-n)
    return seq

class ProblemIFYM_2022_P6_1_8(Problem):
    config = ProblemConfig(
        name=Problem.get_name(__file__),
        statement=PROBLEM_TEMPLATE,
        formatting_instructions=get_list_template(),
        parameters=["N", "n"],
        source="IFYM 2022 P6 Day 1",
        original_parameters={"N": 20, "n": 343},
        original_solution=get_solution(20, 343),
        problem_url="https://klasirane.com/competitions/IFYM/2-8-9%20%D0%BA%D0%BB%D0%B0%D1%81",
        solution_url="https://klasirane.com/competitions/IFYM/2-8-9%20%D0%BA%D0%BB%D0%B0%D1%81",
        tags=[Tag.FIND_ANY, Tag.NUMBER_THEORY, Tag.IS_GENERALIZED, Tag.IS_TRANSLATED]
    )
    n: int
    N: int

    def __init__(self, N:int, n: int):
        self.n = n
        self.N = N

    def get_problem(self):
        return PROBLEM_TEMPLATE.format(n=self.n, N=self.N)

    def check(self, x: list[int]) -> bool:

        if len(x) != self.N:
            return False, f"Sequence should contain {self.N} elements", CheckerTag.INCORRECT_LENGTH

        for num in x:
            if type(num) != int or num <= 0:
                return False, "All numbers must be natural numbers", CheckerTag.INCORRECT_FORMAT
            if num % self.n != 0:
                return False, f"All numbers in the sequence must be divisible by {self.n}", CheckerTag.INCORRECT_SOLUTION
        
        for i in range(self.N - 1):
            x_str, y_str = str(x[i]), str(x[i+1])
    
            # y must have exactly one more digit than x
            if len(x_str) != len(y_str) + 1:
                return False, f"Number {y_str} cannot be achieved from {x_str} by removing 1 digit", CheckerTag.INCORRECT_SOLUTION
            
            shift = 0
            j = 0
            while j < len(y_str):
                if x_str[j+shift] == y_str[j]:
                    j += 1
                    continue
                elif shift != 0:
                    return False, f"Number {y_str} cannot be achieved from {x_str} by removing 1 digit", CheckerTag.INCORRECT_SOLUTION
                elif x_str[j+shift] == '0':
                    return False, f"Number {y_str} cannot be achieved from {x_str} by removing 1 digit", CheckerTag.INCORRECT_SOLUTION
                else:
                    shift += 1
            if shift == 0 and x_str[-1] == '0':
                return False, f"Number {y_str} cannot be achieved from {x_str} by removing 1 non-zero digit", CheckerTag.INCORRECT_SOLUTION

        return True, "OK", CheckerTag.CORRECT
        
    @staticmethod
    def generate() -> "ProblemIFYM_2022_P6_1_8":
        n = random.randint(10, 10000)
        N = random.randint(10, 40)
        return ProblemIFYM_2022_P6_1_8(N, n)

    def get_solution(self):
        return get_solution(self.N, self.n)
