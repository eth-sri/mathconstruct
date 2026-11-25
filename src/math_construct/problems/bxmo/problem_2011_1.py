from math_construct.problems.templates import TEMPLATES
PROBLEM_TEMPLATE = TEMPLATES["bxmo/problem_2011_1.py"]

import math
import random
from math_construct.problems.problem import Problem, ProblemConfig, Tag, CheckerTag
from math_construct.templates import get_matrix_template
from sympy import primefactors


LIST_FORMATTING_TEMPLATE = r"""Output the answer as a comma separated list of lists inside of \boxed{...}. The first integer in a list should be equal to $m$, the second to $n$. For instance, \boxed{(2,5),(3,6)}."""



def get_solution(l, k):
    pairs = []
    start_val = math.ceil(math.log2(2 * k))
    if 2 ** start_val < 2 * k + 2:
        start_val += 1
    for i in range(start_val, l + start_val):
        m = 2 ** i - 2 * k
        n = m * (m + 2 * k)
        pairs.append([m, n])
    return pairs

class ProblemBxMO20111(Problem):
    config = ProblemConfig(
        name=Problem.get_name(__file__),
        statement=PROBLEM_TEMPLATE,
        formatting_instructions=LIST_FORMATTING_TEMPLATE,
        parameters=["k_squared", "l", "max_val", "k"],
        source="BxMO 2011 P1",
        original_parameters={"k_squared": 1, "l": 3, "max_val": 14, "k": 1},
        problem_url="http://bxmo.org/problems/bxmo-problems-2011-zz.pdf",
        solution_url="http://bxmo.org/problems/bxmo-problems-2011-zz.pdf",
        tags=[Tag.NUMBER_THEORY, Tag.FIND_INF, Tag.IS_ORIGINAL, Tag.IS_GENERALIZED], 
        original_solution=get_solution(3, 1)
    )
    k: int
    k_squared: int
    l: int
    max_val: int

    def __init__(self, k, k_squared: int, l: int, max_val: int):
        self.k = k
        self.k_squared = k_squared
        self.l = l
        self.max_val = max_val

    def get_problem(self):
        return PROBLEM_TEMPLATE.format(k=self.k, k_squared=self.k_squared, l=self.l, max_val=self.max_val)
        
    def check(self, a: list[list[int]]) -> bool:
        sols = [tuple(sol) for sol in a]
        correct, message, tag = self.check_format(sols, is_integer=True, expected_length=self.l, is_unique=True)
        if not correct:
            return correct, message, tag
        check_format = self.check_format([sol[0] for sol in sols], min_val_inclusive=2, max_val_inclusive=self.max_val)
        if not check_format[0]:
            return check_format
        if any(not (sol[0] < sol[1]) for sol in sols):
            return False, "Each pair must satisfy m < n", CheckerTag.INCORRECT_SOLUTION
        # sort sol by increasing n
        a.sort(key=lambda x: x[1])
        # check that n_i / n_{i-1} >= 4
        for i in range(1, len(a)):
            if a[i][1] / a[i-1][1] < 4 - 0.0000001:
                return False, f"n_{i} / n_{i-1} < 4", CheckerTag.INCORRECT_SOLUTION
        for sol in a:
            m, n = sol
            prime_m = primefactors(m)
            prime_n = primefactors(n)
            if set(prime_m) != set(prime_n):
                return False, f"{m} and {n} do not have the same prime factors.", CheckerTag.INCORRECT_SOLUTION
            prime_m_plus_k = primefactors(m + self.k)
            prime_n_plus_k_squared = primefactors(n + self.k_squared)
            if set(prime_m_plus_k) != set(prime_n_plus_k_squared):
                return False, f"{m} + {self.k} and {n} + {self.k_squared} do not have the same prime factors.", CheckerTag.INCORRECT_SOLUTION
        return True, "OK", CheckerTag.CORRECT
            
    @staticmethod
    def generate() -> "ProblemBxMO20111":
        k = random.randint(1, 10)
        k_squared = k ** 2
        l = random.randint(2, 10)
        log_2 = math.ceil(math.log2(k * 2))
        if 2 ** log_2 <= 2 * k:
            log_2 += 1
        ms = [2 ** power - 2 * k for power in range(log_2, log_2 + l)]
        max_val = max(ms)
        problem = ProblemBxMO20111(k, k_squared, l, max_val)
        assert problem.check_raw(get_solution(l, k))
        return problem
    
    def get_solution(self):
        return get_solution(self.l, self.k)
