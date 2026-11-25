from math_construct.problems.templates import TEMPLATES
PROBLEM_TEMPLATE = TEMPLATES["usamts/problem_2001_4_4.py"]

import random
from math_construct.problems.problem import Problem, ProblemConfig, Tag, CheckerTag
from math_construct.templates import get_list_template


def get_solution(k: int) -> list[int]:
    ret = []
    # aaa
    for i in range(0, k+1):
        ret.append(str(i)*3)
    # aab
    for i in range(0, k+1):
        for j in range(i+1, k+1):
            ret.append(str(i)*2 + str(j))
            ret.append(str(j)*2 + str(i))
    # abc and cba
    for i in range(0, k+1):
        for j in range(i+1, k+1):
            for l in range(j+1, k+1):
                ret.append(str(i) + str(j) + str(l))
                ret.append(str(l) + str(j) + str(i))
    return ret

class Problem10(Problem):
    config = ProblemConfig(
        name=Problem.get_name(__file__),
        statement=PROBLEM_TEMPLATE,
        formatting_instructions=get_list_template(),
        parameters=["k"],
        source="USAMTS 01/02 Round 4 Problem 4",
        original_parameters={"k": 9},
        original_solution=get_solution(9),
        problem_url="https://files.usamts.org/Problems_13_4.pdf",
        solution_url="https://files.usamts.org/Solutions_13_4.pdf",
        tags=[Tag.COMBINATORICS, Tag.IS_ORIGINAL, Tag.IS_GENERALIZED, Tag.FIND_MAX_MIN]
    )
    k: int

    def __init__(self, k: int):
        self.m = len(get_solution(k))
        self.k = k

    def get_problem(self):
        return PROBLEM_TEMPLATE.format(k=self.k, m=self.m)

    def check(self, answer: list[str]) -> bool:
        if len(answer) != len(set(answer)):
            return False, f"Not all elements of answer are distinct", CheckerTag.INCORRECT_SOLUTION
        if not all(isinstance(y, str) for y in answer):
            return False, "All elements should be integers", CheckerTag.INCORRECT_FORMAT
        s = set(answer)
        for x in answer:
            if len(x) != 3 or not x.isnumeric():
                return False, f"{x} is not a valid 3-digit number", CheckerTag.INCORRECT_FORMAT
            for i in range(len(x) - 2):
                y = x[:i] + x[i+1] + x[i] + x[i+2:]
                if y in s and y != x:
                    return False, f"{x} and {y} are in the list and differ by a single transposition", CheckerTag.INCORRECT_SOLUTION
        recv = {}
        for x in answer:
            if not all(c in '0123456789'[:self.k + 1] for c in x):
                return False, f"{x} uses digits outside 0-{self.k}", CheckerTag.INCORRECT_SOLUTION
            for y in {x} | {x[:i] + x[i+1] + x[i] + x[i+2:] for i in range(2)}:
                if recv.setdefault(y, x) != x:
                    return False, f"received {y} is ambiguous between {recv[y]} and {x}", CheckerTag.INCORRECT_SOLUTION
        if len(answer) != self.m:
            return False, f"List of size {len(answer)}, should be {self.m}", CheckerTag.INCORRECT_SOLUTION
        return True, "OK", CheckerTag.CORRECT

    @staticmethod
    def generate() -> "Problem10":
        return Problem10(random.randint(2, 9))

    def get_solution(self):
        return get_solution(self.k)
