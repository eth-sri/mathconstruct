from math_construct.problems.templates import TEMPLATES
PROBLEM_TEMPLATE = TEMPLATES["misc/problem_balticway_2005_19.py"]

from math_construct.problems.problem import Problem, ProblemConfig, Tag, CheckerTag

import random


FORMATTING_INSTRUCTIONS = r"""Output the sequences as a list of comma-separated tuples of increasing integers inside of \boxed, e.g. \boxed{(1, 2, 3, 4, 5), (7, 10, 11, 12, 14), (2, 3, 4, 9, 10)}."""

def get_solution(N: int, M: int) -> list[tuple[int]]:
    pythagorean_triples = []
    n = 2
    m = 1
    while len(pythagorean_triples) < N:
        if n**2 - m**2 < 2*m*n:
            pythagorean_triples.append((n**2 - m**2, 2*m*n, m**2 + n**2))
        else:
            pythagorean_triples.append((2*m*n, n**2 - m**2, m**2 + n**2))
        
        if m == n-1:
            n += 1
        else:
            m += 1
    seq = []
    for triple in pythagorean_triples:
        example = [(triple[0]**(M-1))**2, (triple[0]**(M-2)*triple[1])**2]
        for i in range(M-2):
            example.append((triple[0]**(M-3-i)*triple[1]*triple[2]**(i+1))**2)
        seq.append(tuple(example))
    return seq

def is_square(num: int) -> bool:
  if num == 1:
      return True
  x = num // 2
  seen = set([x])
  while x * x != num:
    x = (x + (num // x)) // 2
    if x in seen: return False
    seen.add(x)
  return True

class ProblemBaltic2005P19(Problem):
    config = ProblemConfig(
        name=Problem.get_name(__file__),
        statement=PROBLEM_TEMPLATE,
        formatting_instructions=FORMATTING_INSTRUCTIONS,
        parameters=["N", "M"],
        source="Baltic Way 2005 Extralist 05.19",
        original_parameters={"N": 10, "M": 15},
        original_solution=get_solution(10, 15),
        problem_url="https://www.balticway07.dk/data/ekstra/bw02-06-online-a5.pdf",
        solution_url="https://www.balticway07.dk/data/ekstra/bw02-06-online-a5.pdf",
        tags=[Tag.NUMBER_THEORY, Tag.FIND_ANY, Tag.IS_GENERALIZED]
    )
    N: int
    M: int

    def __init__(self, N: int, M: int):
        self.N = N
        self.M = M

    def get_problem(self):
        return PROBLEM_TEMPLATE.format(N=self.N, M=self.M)

    def check(self, x: list[tuple[int]]) -> bool:
        if len(x) != self.N:
            return False, f"{self.N} examples expected, received {len(x)}", CheckerTag.INCORRECT_LENGTH

        for i, entry in enumerate(x):
            x[i] = tuple(sorted(entry))

        if len(set(x)) != len(x):
            return False, f"Examples should be unique", CheckerTag.INCORRECT_FORMAT
        
        for i, entry in enumerate(x):
            if len(entry) != self.M:
                return False, f"Each sequence should contain {self.M} numbers, received {len(entry)}", CheckerTag.INCORRECT_FORMAT
            for num in entry:
                if not (isinstance(num, int) and num > 0):
                    return False, f"All numbers should be positive integers, found {num}", CheckerTag.INCORRECT_FORMAT
                if not is_square(num):
                    return False, f"Number {num} in entry {entry} is not a square number", CheckerTag.INCORRECT_SOLUTION
            
            entry_sum = sum([num for num in entry])
            if not is_square(entry_sum):
                return False, f"Sum of the squares of {entry} - {entry_sum} is not a square number", CheckerTag.INCORRECT_SOLUTION
            
        return True, "OK", CheckerTag.CORRECT

    @staticmethod
    def generate() -> "ProblemBaltic2005P19":
        N = random.randint(3, 10)
        M = random.randint(7, 10)
        return ProblemBaltic2005P19(N, M)

    def get_solution(self):
        return get_solution(self.N, self.M)
