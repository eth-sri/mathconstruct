from math_construct.problems.templates import TEMPLATES
PROBLEM_TEMPLATE = TEMPLATES["backups/imc_problem_2022_6.py"]

import random
from sympy import isprime
from fractions import Fraction
from math_construct.problems.problem import Problem, ProblemConfig, Tag, CheckerTag
from math_construct.templates import get_list_template
from itertools import permutations
    

def get_solution(p: int) -> list[int]:
    x = []
    for i in range(1, p):
        for j in range(1, p):
            if i * j % p == 1:
                x.append(j)
                break
    return x

def check_permutation(perm, p):
    total = 0
    for i in range(len(perm)-1):
        total = (total + perm[i] * perm[i+1]) % p
    total2 = 0
    f = 1
    for i in range(len(perm)):
        # total2 = (total2 + perm[i]*(i+1)) % p
        # total2 += perm[i]/perm[i+1] if i+1 < len(perm) else 0
        if i+1 < len(perm):
            #total2 += perm[i] * (1.0/perm[i+1] - 1)
            f += Fraction(perm[i], perm[i+1])
            total2 += perm[i] * (i+1) % p
        else:
            total2 += perm[i] * (i+1) % p
    total2 += 1
    return total == 2 and f.numerator%p == 0


def brute_force(p) -> list[int]:
    numbers = list(range(1, p))

    found = False
    attempts = 0
    while not found and attempts < 30000:
        random.shuffle(numbers)
        if check_permutation(numbers, p):
            found = True
            return numbers
        attempts += 1
    return None

class Problem_IMC_2022_6(Problem):
    config = ProblemConfig(
        name=Problem.get_name(__file__),
        statement=PROBLEM_TEMPLATE,
        formatting_instructions=get_list_template(),
        parameters=["p"],
        source="IMC 2022 P6",
        original_parameters={"p": 461},
        original_solution=get_solution(461),
        problem_url="https://www.imc-math.org.uk/imc2022/imc2022day2solutions.pdf#page=2",
        solution_url="https://www.imc-math.org.uk/imc2022/imc2022day2solutions.pdf#page=2",
        tags=[Tag.COMBINATORICS, Tag.IS_SIMPLIFIED, Tag.FIND_ANY],
    )
    p: int

    def __init__(self, p: int):
        self.p = p

    def get_problem(self):
        return PROBLEM_TEMPLATE.format(p=self.p)

    def check(self, x: list[int]) -> bool:
        if len(x) != self.p - 1:
            return False, f"The number of elements is not equal to p-1 ({self.p-1}).", CheckerTag.INCORRECT_LENGTH
        for i in range(self.p - 1):
            if x[i] < 1 or x[i] > self.p - 1:
                return False, f"Element {x[i]} is not in the range 1 to {self.p-1}.", CheckerTag.INCORRECT_FORMAT
        if len(set(x)) != self.p - 1:
            return False, f"The set of elements is not equal to {self.p-1}.", CheckerTag.INCORRECT_SOLUTION
        t = sum([x[i] * x[i+1] for i in range(self.p - 2)]) % self.p
        if t != 2:
            return False, f"The sum is not equal to 2 modulo {self.p}.", CheckerTag.INCORRECT_SOLUTION
        fsum = 1
        for i in range(len(x)-1):
            fsum += Fraction(x[i], x[i+1])
        if fsum.numerator % self.p != 0:
            return False, f"The sum is not divisible by {self.p}.", CheckerTag.INCORRECT_SOLUTION
        return True, "OK", CheckerTag.CORRECT

    @staticmethod
    def generate() -> "Problem_IMC_2022_6":
        GOODP = [461, 479, 499, 491, 491, 467, 439]
        p = random.choice(GOODP)
        return Problem_IMC_2022_6(p)

    def get_solution(self):
        return get_solution(self.p)
