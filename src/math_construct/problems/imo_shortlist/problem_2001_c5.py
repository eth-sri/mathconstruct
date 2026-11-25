from math_construct.problems.templates import TEMPLATES
PROBLEM_TEMPLATE = TEMPLATES["imo_shortlist/problem_2001_c5.py"]

from math_construct.problems.problem import Problem, ProblemConfig, Tag, CheckerTag
import random


FORMATTING_INSTRUCTIONS = r"""Output the sequences as comma-separated tuples inside of \boxed{}, e.g. \boxed{(1, 2), (1, 2, 3), (1, 1, 1, 1, 0)}."""

def get_solution(k: int) -> list[list[int]]:
    res = [[2,0,2,0], [1,2,1,0], [2,1,2,0,0]][:k]
    p = 3
    while len(res) < k:
        res += [[p,2,1] + [0]*(p-3) + [1,0,0,0]]
        p += 1
    return res

class Problem17(Problem):
    config = ProblemConfig(
        name=Problem.get_name(__file__),
        statement=PROBLEM_TEMPLATE,
        formatting_instructions=FORMATTING_INSTRUCTIONS,
        parameters=["k"],
        source="IMO 2001 Shortlist C5",
        original_parameters={"k": 10},
        original_solution=get_solution(10),
        tags=[Tag.COMBINATORICS, Tag.IS_SIMPLIFIED, Tag.FIND_ALL], 
        problem_url="https://olympiads.win.tue.nl/imo/imo2001/imo2001-shortlist.pdf#page=31",
        solution_url="https://olympiads.win.tue.nl/imo/imo2001/imo2001-shortlist.pdf#page=31",
    )
    k: int

    def __init__(self, k: int):
        self.k = k

    def get_problem(self):
        return PROBLEM_TEMPLATE.format(k=self.k)

    def check(self, x: list[list[int]]) -> bool:
        if len(x) != self.k:
            return False, f"List of size {len(x)}, should be {self.k}", CheckerTag.INCORRECT_LENGTH
        if not all(isinstance(seq, list) for seq in x):
            return False, "All elements should be lists", CheckerTag.INCORRECT_FORMAT
        # assert they are all unique
        if len(set(tuple(seq) for seq in x)) != len(x):
            return False, "All elements should be unique", CheckerTag.INCORRECT_FORMAT

        for seq in x:
            if len(seq) == 0:
                return False, "Sequences must be non-empty", CheckerTag.INCORRECT_FORMAT
            if not all(isinstance(i, int) for i in seq):
                return False, "All elements should be integers", CheckerTag.INCORRECT_FORMAT
            for i in range(len(seq)):
                if seq.count(i) != seq[i]:
                    return False, f"Sequence {seq} has {seq.count(i)} occurrences of {i}, should be {seq[i]}", CheckerTag.INCORRECT_SOLUTION
        return True, "OK", CheckerTag.CORRECT

    @staticmethod
    def generate() -> "Problem17":
        k = random.randint(5, 25)
        return Problem17(k)

    def get_solution(self):
        return get_solution(self.k)
