from math_construct.problems.templates import TEMPLATES
PROBLEM_TEMPLATE = TEMPLATES["serbian/problem_2023_tst_1.py"]

import random

from math_construct.problems.problem import Problem, ProblemConfig, Tag, CheckerTag
from math_construct.templates import get_list_template


FORMATTING_INSTRUCTIONS = r"""Output a comma-separated list of distinct pairs within a \boxed environment indicating (1-indexed) acquaintances. For example: \boxed{(1, 2), (3, 4)} indicates that Spartans 1 and 2, and Spartans 3 and 4 know each other. Output each pair once, i.e., if $(i, j)$ is in the list, $(j, i)$ should not be in the list."""

def get_solution(n: int, maxe: int) -> list[list[int]]:
    # get s 
    currn = 0 
    s = 0 
    while currn < n: 
        s += 1 
        currn += s
    
    edges = [] 
    start = 1
    for i in range(1, s+1): 
        end = start + i 
        for curr in range(start, end):
            for other in range(end, n+1):
                edges.append([curr, other])
        start = end 
    return edges


class ProblemSerbianTst2023_1(Problem):
    config = ProblemConfig(
        name=Problem.get_name(__file__),
        statement=PROBLEM_TEMPLATE,
        formatting_instructions=FORMATTING_INSTRUCTIONS,
        parameters=["n", "maxe"],
        source="Serbian Team Selection Contest 2023 Problem 1",
        problem_url="https://dms.rs/wp-content/uploads/2023/06/IZBORNO_FORMULACIJE_SVE_2023.pdf",
        solution_url="https://dms.rs/wp-content/uploads/2023/06/RESENJA_IZBORNO_SVE_2023.pdf",
        original_parameters={"n": 28, "maxe": 322}, # reduced from source due to large output size
        original_solution=get_solution(28, 322),
        tags=[Tag.COMBINATORICS, Tag.FIND_MAX_MIN, Tag.IS_SIMPLIFIED, Tag.IS_TRANSLATED]
    )
    n: int 
    maxe: int 

    def __init__(self, n: int, maxe: int):
        self.n = n
        self.maxe = maxe
        # validate variant 
        currn = 0 
        s = 0 
        while currn < n: 
            s += 1 
            currn += s
        if currn != n:
            raise ValueError(f"Invalid variant with n = {n}")
        curr_maxe = 0 
        for i in range(s+1): 
            curr_maxe += i * (n-i)
        curr_maxe  = curr_maxe // 2 
        if curr_maxe != maxe:
            raise ValueError(f"Invalid variant with maxe = {maxe}")

    def get_problem(self):
        return PROBLEM_TEMPLATE.format(n=self.n, maxe=self.maxe)
    
    def check(self, solution: list[list[int]]) -> tuple[bool, str, CheckerTag]:
        # length  
        if len(solution) != self.maxe:
            return False, f"List of size {len(solution)}, should be {self.maxe}", CheckerTag.INCORRECT_LENGTH

        # format 
        fs = set()
        for p in solution:
            if len(p) != 2: 
                return False, f"Pair {p} is not of size 2", CheckerTag.INCORRECT_FORMAT
            if not all(isinstance(v, int) and 1 <= v <= self.n for v in p):
                return False, f"Pair {p} has a vertex outside 1..n", CheckerTag.INCORRECT_FORMAT
            if p[0] == p[1]: 
                return False, f"Pair {p} is a self edge, this is not allowed", CheckerTag.INCORRECT_FORMAT
            #insert into set 
            fs.add(str(sorted(p)))
        if len(fs) != self.maxe:
            return False, f"Pairs are not distinct", CheckerTag.INCORRECT_FORMAT 
        
        # constraints 
        degs = [0] * (self.n+1)
        for p in solution:
            degs[p[0]] += 1
            degs[p[1]] += 1
        for p in solution: 
            if degs[p[0]] == degs[p[1]]:
                return False, f"Pair {p} has the same number of acquaintances", CheckerTag.INCORRECT_SOLUTION

        return True, "OK", CheckerTag.CORRECT

    @staticmethod
    def generate() -> "ProblemSerbianTst2023_1":
        s = random.choice([6, 7]) # 8 has 5k output chars, but 5 is likely very bruteforceable
        n = sum(range(s+1))
        maxe = sum([i * (n-i) for i in range(s+1)]) // 2 
        return ProblemSerbianTst2023_1(n, maxe)

    def get_solution(self):
        return get_solution(self.n, self.maxe)
