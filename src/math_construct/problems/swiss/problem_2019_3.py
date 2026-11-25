from math_construct.problems.templates import TEMPLATES
PROBLEM_TEMPLATE = TEMPLATES["swiss/problem_2019_3.py"]

import random
from math_construct.problems.problem import Problem, ProblemConfig, Tag, CheckerTag

LIST_FORMATTING_TEMPLATE = r"""Output the answer as a comma separated list of lists inside of $\boxed{...}$. Each list should contain the first period of the sequence that satisfies the property. For instance, \boxed{(1,0.2,0.5),(3,4,5)} indicates the sequences 1,0.2,0.5,1,0.2,0.5,... and 3,4,5,3,4,5,..."""



def get_solution(k, m):
    return [
        [a / (k - 1), 1 / a] for a in range(1, m + 1)
    ]

class ProblemSwiss20193(Problem):
    config = ProblemConfig(
        name=Problem.get_name(__file__),
        statement=PROBLEM_TEMPLATE,
        formatting_instructions=LIST_FORMATTING_TEMPLATE,
        parameters=["k", "m"],
        source="Swiss Math Olympiad Finals 2019",
        problem_url="https://mathematical.olympiad.ch/fileadmin/user_upload/Archiv/Intranet/Olympiads/Mathematics/deploy/exams/2019/FinalRound/MasterSolution/finalRoundSolution2019.pdf#page=5",
        solution_url="https://mathematical.olympiad.ch/fileadmin/user_upload/Archiv/Intranet/Olympiads/Mathematics/deploy/exams/2019/FinalRound/MasterSolution/finalRoundSolution2019.pdf#page=5",
        original_parameters={"k": 4, "m": 10},
        original_solution=get_solution(4, 10),
        tags=[Tag.IS_SIMPLIFIED, Tag.ALGEBRA, Tag.FIND_ALL, Tag.IS_GENERALIZED] 
    )
    k: int
    m: int

    def __init__(self, k: int, m: int):
        self.k = k
        self.m = m

    def get_problem(self):
        return PROBLEM_TEMPLATE.format(k=self.k, m=self.m)
        
    def check(self, a: list[list[int]]) -> bool:
        checker = self.check_format(a, expected_length=self.m, is_unique=True)
        if not checker[0]:
            return checker
        if any(not isinstance(seq, list) or len(seq) == 0 or any(v <= 0 for v in seq) for seq in a):
            return False, "Each sequence must be a non-empty list of positive reals.", CheckerTag.INCORRECT_FORMAT
        def minimal_period(seq):
            for p in range(1, len(seq) + 1):
                if len(seq) % p == 0 and all(abs(seq[t] - seq[t % p]) < 1e-12 for t in range(len(seq))):
                    return tuple(seq[:p])
        if len(set(minimal_period(seq) for seq in a)) != len(a):
            return False, "Sequences are not distinct.", CheckerTag.INCORRECT_FORMAT
        for i, seq in enumerate(a):
            for j in range(2, len(seq) + 2):
                if abs(seq[j % len(seq)] - (1 / self.k) * (1 / seq[(j - 1)  % len(seq)] + seq[(j - 2) % len(seq)])) > 1e-8:
                    return False, f"Sequence {i} does not satisfy the property at index {j-2,j-1,j}.", CheckerTag.INCORRECT_SOLUTION
        return True, "OK", CheckerTag.CORRECT

    @staticmethod
    def generate() -> "ProblemSwiss20193":
        k = random.randint(2, 50)
        m = random.randint(10, 20)
        return ProblemSwiss20193(k, m)
    
    def get_solution(self):
        return get_solution(self.k, self.m)
