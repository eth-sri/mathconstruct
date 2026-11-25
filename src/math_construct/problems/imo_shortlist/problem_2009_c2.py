from math_construct.problems.templates import TEMPLATES
PROBLEM_TEMPLATE = TEMPLATES["imo_shortlist/problem_2009_c2.py"]

from math_construct.problems.problem import Problem, ProblemConfig, Tag, CheckerTag
import itertools
import math
import random


FORMATTING_INSTRUCTIONS = r"""Output a comma-separated list of triples, inside of \boxed, for example \boxed{(2,3,4), (5,6,7)}."""

def get_solution(n: int, N: int) -> list[list[int]]:
    ret = [] 
    if n % 3 == 2:
        k = (n+1) // 3 
        a = list(range(2*k))
        b = list(range(k+1, 2*k+1)) + list(range(k))
        c = list(reversed(range(0, 2*k-1, 2))) + list(reversed(range(1, 2*k, 2)))
    elif n % 3 == 0:
        k = n // 3 
        a = list(range(2*k+1))
        b = list(range(k, 2*k+1)) + list(range(k))
        c = list(reversed(range(0, 2*k+1, 2))) + list(reversed(range(1, 2*k, 2)))
    else:
        k = (n-1) // 3 
        a = list(range(2*k+1))
        b = list(range(k, 2*k+1)) + list(range(k))
        c = list(reversed(range(1, 2*k+2, 2))) + list(reversed(range(2, 2*k+1, 2)))
    return [[a[i], b[i], c[i]] for i in range(N)]

class Problem2009C2(Problem):
    config = ProblemConfig(
        name=Problem.get_name(__file__),
        statement=PROBLEM_TEMPLATE,
        formatting_instructions=FORMATTING_INSTRUCTIONS,
        parameters=["n", "N"],
        source="IMO 2009 Shortlist C2",
        original_parameters={"n": 30, "N": 21},
        original_solution=get_solution(30, 21),
        problem_url="https://www.imo-official.org/problems/IMO2009SL.pdf#page=29",
        solution_url="https://www.imo-official.org/problems/IMO2009SL.pdf#page=29",
        tags=[Tag.COMBINATORICS, Tag.FIND_INF, Tag.IS_SIMPLIFIED]
    )
    n: int
    N: int

    def __init__(self, n: int, N: int):
        self.n = n
        self.N = int(2*self.n/3)+1

    def get_problem(self):
        return PROBLEM_TEMPLATE.format(n=self.n, N=self.N)
    
    def check(self, solution: list[list[int]]) -> tuple[bool, str, CheckerTag]:
        N = self.N
        # format 
        if len(solution) != N:
            return False, f"List of size {len(solution)}, should be N({self.n})={N}", CheckerTag.INCORRECT_LENGTH
        if any(len(triple) != 3 for triple in solution):
            return False, "Some list element is not a triple", CheckerTag.INCORRECT_FORMAT

        # conditions 
        for triple in solution:
            if not all(isinstance(v, int) and v >= 0 for v in triple):
                return False, f"Triple {triple} must consist of nonnegative integers", CheckerTag.INCORRECT_FORMAT
            if sum(triple) != self.n:
                return False, f"Sum of elements in triple {triple} is not {self.n}", CheckerTag.INCORRECT_SOLUTION
        for i in range(N):
            for j in range(i+1, N): 
                for idx in range(3):
                    if solution[i][idx] == solution[j][idx]:
                        return False, f"Triple {solution[i]} and {solution[j]} have the same element at index {idx}", CheckerTag.INCORRECT_SOLUTION
        return True, "OK", CheckerTag.CORRECT
        
    @staticmethod
    def generate() -> "Problem2009C2":
        n = random.randint(20, 50)
        N = int(2*n/3)+1
        return Problem2009C2(n,N)

    def get_solution(self):
        return get_solution(self.n, self.N)
