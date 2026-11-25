from math_construct.problems.templates import TEMPLATES
PROBLEM_TEMPLATE = TEMPLATES["bmo_shortlist/problem_2015_n7.py"]

from math_construct.problems.problem import Problem, ProblemConfig, Tag, CheckerTag
import random


FORMATTING_INSTRUCTIONS = r"""Output the sequences as comma-separated tuples inside of \boxed, e.g. \boxed{(1, 2, 3, 4), (7, 10, 11, 12), (2, 3, 4, 9)}."""

from sympy import isprime, primerange

def is_primitive_root(g, p):
    """Check if g is a primitive root modulo p."""
    if pow(g, p-1, p) != 1:
        return False
    for d in range(1, p-1):
        if (p-1) % d == 0 and pow(g, d, p) == 1:
            return False
    return True

def find_primes_with_primitive_root(g, limit):
    """Find primes where g is a primitive root modulo p."""
    primes = list(primerange(3, limit))  # Exclude p=2
    result = [p for p in primes if is_primitive_root(g, p)]
    return result


def compute_possibilities(p: int):
    base = (10**(p-1) - 1)//p
    addition = 10**(p)*142857
    return [addition+base, addition+base*2, addition+base*3, addition+base*4]

def get_solution(k: int) -> list[list[int]]:
    limit = 100
    ps = []
    while len(ps) < k or limit > 100000:
        ps = find_primes_with_primitive_root(10, limit)[1:]
        limit*=10
    ps = ps[:k]
    res = []
    for p in ps:
        res.append(compute_possibilities(p))
    return res

def are_numbers_anagrams(num1, num2):
    # Convert numbers to strings and count the frequency of each digit
    str1 = str(num1)
    str2 = str(num2)
    
    # Anagrams must have the same sorted digit sequence
    return sorted(str1) == sorted(str2)

class ProblemBMO2015N7(Problem):
    config = ProblemConfig(
        name=Problem.get_name(__file__),
        statement=PROBLEM_TEMPLATE,
        formatting_instructions=FORMATTING_INSTRUCTIONS,
        parameters=["N"],
        source="BMO 2015 Shortlist N7",
        original_parameters={"N": 5},
        original_solution=get_solution(5),
        problem_url="https://artofproblemsolving.com/community/c6h1889231p12884001",
        solution_url="https://artofproblemsolving.com/community/c6h1889231p12884001",
        tags=[Tag.NUMBER_THEORY, Tag.FIND_INF, Tag.IS_GENERALIZED, Tag.IS_SIMPLIFIED]
    )
    N: int

    def __init__(self, N: int):
        self.N = N

    def get_problem(self):
        return PROBLEM_TEMPLATE.format(N=self.N)

    def check(self, x: list[tuple[int]]) -> bool:
        if len(x) != self.N:
            return False, f"{self.N} examples expected, received {len(x)}", CheckerTag.INCORRECT_LENGTH
        
        for i, entry in enumerate(x):
            if len(entry) != 4:
                return False, f"Expected examples of length 4, received {len(entry)}", CheckerTag.INCORRECT_FORMAT
            if any(type(e) != int or e <= 0 for e in entry) or len(set(entry)) != 4:
                return False, f"Each example must consist of 4 different positive integers", CheckerTag.INCORRECT_SOLUTION
            x[i] = tuple(sorted(entry))
            
        if len(x) != len(set(x)):
            return False, f"Elements of {x} are non-distinct", CheckerTag.INCORRECT_FORMAT
        
        for entry in x:
            for i in range(4):
                if not are_numbers_anagrams(entry[i], sum(entry) - entry[i]):
                    return False, f"{entry[i]} and {sum(entry) - entry[i]} are not anagrams", CheckerTag.INCORRECT_SOLUTION

        return True, "OK", CheckerTag.CORRECT

    @staticmethod
    def generate() -> "ProblemBMO2015N7":
        k = random.randint(2, 8)
        return ProblemBMO2015N7(k)

    def get_solution(self):
        return get_solution(self.N)
