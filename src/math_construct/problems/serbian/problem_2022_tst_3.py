from math_construct.problems.templates import TEMPLATES
PROBLEM_TEMPLATE = TEMPLATES["serbian/problem_2022_tst_3.py"]

import random

from math_construct.problems.problem import Problem, ProblemConfig, Tag, CheckerTag
from math_construct.templates import get_list_template
from sympy import sieve


FORMATTING_INSTRUCTIONS = r"""Output a comma-separated list of configurations. Each configuration is a list where the first element is $n$, and the following $n$ elements indicate the token coloring going clockwise (0 for black and 1 for white tokens). For example: \boxed{(3, 0, 1, 0), (4, 1, 0, 1)} is a valid output."""

def get_solution(m: int) -> list[list[int]]:
    # We need m primes of form 4k+3 
    primes = []
    i = 2
    while len(primes) < m:
        i += 1 
        if i in sieve and i % 4 == 3:
            primes.append(i)
    # For each find the configuration
    ret = [] 
    for p in primes: 
        tokens = [1]
        quadresidues = set() 
        for i in range(1, p):
            quadresidues.add((i*i) % p)
        for i in range(1, p):
            if i in quadresidues:
                tokens.append(1)
            else:
                tokens.append(0)
        ret.append([p] + tokens)
    return ret 

class ProblemSerbianTst2022_3(Problem):
    config = ProblemConfig(
        name=Problem.get_name(__file__),
        statement=PROBLEM_TEMPLATE,
        formatting_instructions=FORMATTING_INSTRUCTIONS,
        parameters=["m"],
        source="Serbian Team Selection Contest 2022 Problem 3",
        problem_url="https://dms.rs/wp-content/uploads/2022/05/ZADACI_IZBORNO_IMO_2022.pdf",
        solution_url="https://dms.rs/wp-content/uploads/2022/05/RESENJA_IZBORNO_IMO_2022.pdf",
        original_parameters={"m": 6}, # reduced from source due to large output size
        original_solution=get_solution(6),
        tags=[Tag.NUMBER_THEORY, Tag.FIND_INF, Tag.IS_SIMPLIFIED, Tag.IS_TRANSLATED]
    )
    m: int 

    def __init__(self, m: int):
        self.m = m

    def get_problem(self):
        return PROBLEM_TEMPLATE.format(m=self.m)
    
    def check(self, solution: list[list[int]]) -> tuple[bool, str, CheckerTag]:
        # length  
        if len(solution) != self.m:
            return False, f"List of size {len(solution)}, should be {self.m}", CheckerTag.INCORRECT_LENGTH
        # uniqueness
        if len(set(tuple(sol) for sol in solution)) != len(solution):
            return False, "All elements should be unique", CheckerTag.INCORRECT_FORMAT

        if len(set(sol[0] for sol in solution if len(sol) > 0)) != len(solution):
            return False, "The numbers n should be distinct", CheckerTag.INCORRECT_FORMAT
        # format 
        for sol in solution:
            if len(sol) == 0: 
                return False, f"Empty configuration provided", CheckerTag.INCORRECT_FORMAT
            n = sol[0] 
            if n <= 0 or n % 2 == 0:
                return False, f"Configuration {sol} has n={n}, which is not a positive odd integer", CheckerTag.INCORRECT_FORMAT
            if len(sol) != sol[0] + 1:
                return False, f"Configuration {sol} is not of size n+1", CheckerTag.INCORRECT_FORMAT
            if any(x not in [0, 1] for x in sol[1:]):
                return False, f"Configuration {sol} has invalid colors", CheckerTag.INCORRECT_FORMAT
        
        # constraints
        for sol in solution:
            n = sol[0]
            tokens = sol[1:]
            maxquality = 0 
            for k in range(1, n):
                # quality? 
                rotated_tokens = tokens[k:] + tokens[:k]
                quality = 0
                for t1, t2 in zip(tokens, rotated_tokens):
                    if t1 == t2:
                        quality += 1 
                maxquality = max(maxquality, quality)
            if maxquality > (n-1) // 2:
                return False, f"Quality of some k is above (n-1)/2 for {sol}", CheckerTag.INCORRECT_SOLUTION
        return True, "OK", CheckerTag.CORRECT

    @staticmethod
    def generate() -> "ProblemSerbianTst2022_3":
        m = random.randint(4, 10) # 9 is 243 outputs
        return ProblemSerbianTst2022_3(m)

    def get_solution(self):
        return get_solution(self.m)
