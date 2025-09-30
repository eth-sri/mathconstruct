from math_construct.problems.templates import TEMPLATES
PROBLEM_TEMPLATE = TEMPLATES["usamo/problem_2005_1.py"]

import math
import random
from sympy import divisors, isprime, primefactors, multiplicity
from math_construct.problems.problem import Problem, ProblemConfig, Tag, CheckerTag
from math_construct.templates import get_list_template


FORMATTING_INSTRUCTIONS = r"""Assuming that $d_1, d_2, ..., d_k$ are divisors of $n$ greater than 1 in increasing order, output a list of indices $i_1, i_2, ..., i_k$ such that $d_{i_1}, d_{i_2}, ..., d_{i_k}$ is a permutation of $d_1, d_2, ..., d_k$ which satisfies the properties in the task.
Output the list $i_1, i_2, ..., i_k$ as a comma separated list inside of $\boxed{...}$. For example $\boxed{1, 4, 2, 3}$."""

# Precomputed hard variants where brute force is not trivial
HARD_VARIANTS = [[72, 30, 52, 43], [144, 60, 78, 43], [140, 140, 30, 94], [140, 60, 17, 83], [126, 84, 55, 10], [132, 132, 39, 63], [90, 140, 13, 19], [140, 132, 86, 3], [132, 126, 91, 56], [84, 120, 93, 78]]

def perm_to_ids(perm, all_divs):
    return [all_divs.index(x) for x in perm]

def ids_to_perm(ids, all_divs):
    return [all_divs[x] for x in ids]

def get_solution(n: int) -> list[int]:
    ps = primefactors(n)
    if len(ps) == 1:
        d = divisors(n)[1:]
        return perm_to_ids(d, divisors(n))
    if len(ps) == 3 and ps[0]*ps[1]*ps[2] == n:
        return perm_to_ids([ps[0], ps[0]*ps[1], ps[0]*ps[2], ps[2], ps[1]*ps[2], ps[1], ps[0]*ps[1]*ps[2]], divisors(n))
    p = min(ps, key=lambda x: multiplicity(x, n))
    r = multiplicity(p, n)
    k = n//(p**r)

    a = ids_to_perm(get_solution(k), divisors(k))

    if len(a) == 1:
        prefix = []
    else:
        prefix = a[:-1] + [a[-2]*p]
    suffix = [a[-1]*p, a[-1]]
    all_divisors = divisors(n)[1:]
    for x in prefix + suffix:
        all_divisors.remove(x)
    all_divisors = sorted(all_divisors, key=lambda x: -x)
    perm = prefix + all_divisors + suffix
    return perm_to_ids(perm, divisors(n))

class Problem_USAMO_2005_1(Problem):
    """2005 USAMO Problem 1"""
    config = ProblemConfig(
        name=Problem.get_name(__file__),
        statement=PROBLEM_TEMPLATE,
        formatting_instructions=FORMATTING_INSTRUCTIONS,
        parameters=["a", "b", "c", "d"],
        source="2005 USAMO Problem 1",
        original_parameters={"a": 123, "b": 456, "c": 789, "d": 101},
        original_solution=get_solution(123 * 456 * 789 * 101),
        tags=[Tag.NUMBER_THEORY, Tag.FIND_ANY],
        problem_url="https://artofproblemsolving.com/wiki/index.php/2005_USAMO_Problems/Problem_1",
        solution_url="https://artofproblemsolving.com/wiki/index.php/2005_USAMO_Problems/Problem_1",
    )
    a: int
    b: int
    c: int
    d: int

    def __init__(self, a: int, b: int, c: int, d: int):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.n = a * b * c * d

    def get_problem(self):
        return PROBLEM_TEMPLATE.format(a=self.a, b=self.b, c=self.c, d=self.d)

    def check(self, a: list[int]) -> tuple[bool, str, CheckerTag]:
        if set(a) != set(list(range(1, len(divisors(self.n))))):
            return False, "All elements should be integers between 1 and num_divisors(n)", CheckerTag.INCORRECT_FORMAT
        a = ids_to_perm(a, divisors(self.n))
        if not all(isinstance(y, int) for y in a):
            return False, "All elements should be integers", CheckerTag.INCORRECT_FORMAT
        d = divisors(self.n)[1:]
        if set(a) != set(d):
            return False, f"List should contain all divisors of {self.n} other than 1, but it does not", CheckerTag.INCORRECT_FORMAT
        for i in range(len(a)):
            if math.gcd(a[i], a[(i+1)%len(a)]) == 1:
                return False, f"Two adjacent divisors are relatively prime: {a[i]} and {a[(i+1)%len(a)]}", CheckerTag.INCORRECT_SOLUTION
        return True, "OK", CheckerTag.CORRECT

    @staticmethod
    def generate() -> "Problem_USAMO_2005_1":
        h = random.choice(HARD_VARIANTS)
        return Problem_USAMO_2005_1(*h)
        # while True:
        #     n = random.randint(4, 300) * random.randint(4, 300) * random.randint(4, 300)
        #     ps = primefactors(n)
        #     if len(ps) == 2 and ps[0]*ps[1] == n:
        #         continue
        #     return Problem_USAMO_2005_1(n)

    def get_solution(self):
        return get_solution(self.n)

    def get_brute_force_solution(self):
        num_divs = len(divisors(self.n))
        d = list(range(1, num_divs))
        for it in range(100000):
            random.shuffle(d)
            if self.check_raw(d):
                return d
        return d


# d = [(n, len(divisors(n))) for n in range(2, 150)]
# d.sort(key=lambda x: -x[1])
# top = [x[0] for x in d[:20]]

# hard = []

# # generate A * B * C * D where A, B are from top_20 and C, D are random
# for _ in range(10000000):
#     a = random.choice(top)
#     b = random.choice(top)
#     c = random.randint(2, 100)
#     d = random.randint(2, 100)
#     n = a * b * c * d
#     ps = primefactors(n)
#     if len(ps) == 2 and ps[0]*ps[1] == n:
#         continue
#     # problem = Problem_USAMO_2005_1(a, b, c, d)
#     problem = Problem_USAMO_2005_1.generate()
#     assert problem.check_raw(problem.get_solution())
#     sol = problem.get_solution()
#     if len(str(problem.get_solution())) >= 4000:
#         continue
#     print("n = ", n, len(str(sol)))
#     bf_solution = problem.get_brute_force_solution()
#     if not problem.check_raw(bf_solution):
#         hard += [[a, b, c, d]]
#         print("current hard: ", hard)

# while True:
#     problem = Problem_USAMO_2005_1.generate()
#     if not problem.check_raw(problem.get_brute_force_solution()):
#         assert False


