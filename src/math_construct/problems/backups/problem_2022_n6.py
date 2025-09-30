from math_construct.problems.templates import TEMPLATES
PROBLEM_TEMPLATE = TEMPLATES["backups/problem_2022_n6.py"]

import random
from math_construct.problems.problem import Problem, ProblemConfig, Tag, CheckerTag
import numpy as np
from time import time
from math_construct.templates import get_integer_template


def get_solution(n:int) -> int:
    if n%3 == 0:
        k = n//3
        repeater=1
        for _ in range(k-1):
            repeater = repeater*10**6+1
        return 10110*repeater
    elif n%3 == 2:
        base = 10**136 +2
        for _ in range((n-5)//3):
            base = base*10**6+10110
        return base
    else:
        base = 10**472 + 10**136 + 2*10**336 + 2
        for _ in range((n-10)//3):
            base = base*10**6+10110
        return base


class ProblemJBMO2022N6(Problem):
    config = ProblemConfig(
        name=Problem.get_name(__file__),
        statement=PROBLEM_TEMPLATE,
        formatting_instructions=get_integer_template(),
        parameters=["n"],
        source="2022 JBMO Shortlist N6",
        original_parameters={"n":55},
        original_solution=get_solution(55),
        problem_url="https://artofproblemsolving.com/community/c6h3099045p28018832",
        solution_url="https://artofproblemsolving.com/community/c6h3099045p28018832",
        tags=[Tag.NUMBER_THEORY, Tag.IS_GENERALIZED, Tag.FIND_ANY]
    )
    n: int

    def __init__(self, n: int):
        self.n=n

    def get_problem(self):
        return PROBLEM_TEMPLATE.format(n=self.n, k=int(1.5*self.n))

    def check(self, x: int) -> bool:
        digits = list(map(int, str(x)))

        if len(str(x)) < int(1.5*self.n):
            return False, f"{x} contains less then {int(1.5*self.n)} digits", CheckerTag.INCORRECT_FORMAT

        if x % 2022 != 0:
            return False, f"{x} is not divisible by 2022", CheckerTag.INCORRECT_SOLUTION

        if sum([digit**2 for digit in digits]) != self.n:
            return False, f"Sum of digits is {sum([digit**2 for digit in digits])} instead of {self.n}", CheckerTag.INCORRECT_SOLUTION
        
        return True, "OK", CheckerTag.CORRECT

    @staticmethod
    def generate() -> "ProblemJBMO2022N6":
        n=1
        while n in [1, 2, 4, 7]:
            n = random.randint(43, 100)
        return ProblemJBMO2022N6(n)

    def get_solution(self):
        return get_solution(self.n)
    
    def bruteforce(self):
        def sum_of_digit_squares(n):
            return sum(int(d)**2 for d in str(n))
        start_time = time()
        n = (10**(int(1.5*self.n) - 1) + 2022)//2022
        while n <= n*10*2022:  # reasonable upper limit
            num = n * 2022
            digit_sum = sum_of_digit_squares(num)
            if digit_sum == self.n:
                return num
            n += 1
            if n % 100 == 0 and time() - start_time > 120:
                return 1
