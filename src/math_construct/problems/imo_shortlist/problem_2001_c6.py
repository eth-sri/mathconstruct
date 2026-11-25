from math_construct.problems.templates import TEMPLATES
PROBLEM_TEMPLATE = TEMPLATES["imo_shortlist/problem_2001_c6.py"]


from math_construct.problems.problem import Problem, ProblemConfig, Tag, CheckerTag
import itertools
import math
import random


FORMATTING_INSTRUCTIONS = r"""Output sequences from the set $S$ as a comma-separated list inside of \boxed{}, e.g. \boxed{01101001, 00110101}."""

def get_solution(n: int) -> list[list[int]]:
    subsets = list(itertools.combinations(range(2*n), n))
    d = {i: [] for i in range(n+1)}
    for sub in subsets:
        f = sum(sub) + n
        sub_str = "".join(["1" if i in sub else "0" for i in range(2*n)])
        d[f%(n+1)].append(sub_str)
    min_set = min(d.values(), key=len)
    return min_set
    

class Problem18(Problem):
    config = ProblemConfig(
        name=Problem.get_name(__file__),
        statement=PROBLEM_TEMPLATE,
        formatting_instructions=FORMATTING_INSTRUCTIONS,
        parameters=["n"],
        source="IMO 2001 Shortlist C6",
        original_parameters={"n": 4},
        original_solution=get_solution(4),
        tags=[Tag.COMBINATORICS, Tag.IS_SIMPLIFIED, Tag.FIND_ANY],
        problem_url="https://olympiads.win.tue.nl/imo/imo2001/imo2001-shortlist.pdf#page=33",
        solution_url="https://olympiads.win.tue.nl/imo/imo2001/imo2001-shortlist.pdf#page=33",
    )
    n: int

    def __init__(self, n: int):
        self.n = n

    def get_problem(self):
        return PROBLEM_TEMPLATE.format(n=self.n)

    def move(self, seq: str, i: int, j: int) -> str:
        """Move the i-th bit of seq to the j-th position"""
        chr_list = list(seq)
        char = chr_list.pop(i)
        chr_list.insert(j, char)
        return "".join(chr_list)

    def check(self, S: list[str]) -> bool:
        # first check if size is at most $\frac {1}{n + 1} \binom{2n}{n}$
        if len(S) > (1/(self.n+1)) * math.comb(2*self.n, self.n):
            return False, f"List of size {len(S)}, which is larger than the required number", CheckerTag.INCORRECT_LENGTH
        if not all(isinstance(x, str) for x in S):
            return False, "All elements should be strings", CheckerTag.INCORRECT_FORMAT
        if not all(len(x) == 2*self.n and set(x) <= {"0", "1"} and x.count("1") == self.n for x in S):
            return False, "All elements should be balanced sequences", CheckerTag.INCORRECT_FORMAT
        # check if every balanced sequence is equal to or is a neighbor of at least one sequence in S
        found = set()
        for sub_str in S:
            for i in range(2*self.n):
                for j in range(2*self.n):
                    found.add(self.move(sub_str, i, j))
        if len(found) != math.comb(2*self.n, self.n):
            return False, "There is a sequence that is not a neighbor of any sequence in S", CheckerTag.INCORRECT_SOLUTION
        return True, "OK", CheckerTag.CORRECT

    @staticmethod
    def generate() -> "Problem18":
        n = random.randint(4, 6)
        return Problem18(n)

    def get_solution(self):
        return get_solution(self.n)
