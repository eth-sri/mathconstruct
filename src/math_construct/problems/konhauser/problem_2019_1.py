from math_construct.problems.templates import TEMPLATES
PROBLEM_TEMPLATE = TEMPLATES["konhauser/problem_2019_1.py"]

import random
from math_construct.problems.problem import Problem, ProblemConfig, Tag, CheckerTag


LIST_FORMATTING_TEMPLATE = r"""Output the answer as a comma separated list of lists inside of $\boxed{...}$. For instance, $\boxed{(1,2,3),(4,5,6)}$. The $i$-th element of your list should indicate the students assigned to project $i$. Thus, you should include the already assigned projects as well."""



def get_solution(permutation):
    sol = [
        [2,3,4,5],
        [1,3,6,7],
        [1,2,8,9],
        [1,5,10,11],
        [1,4,12,13],
        [2,7,11,13],
        [2,6,10,12],
        [3,9,10,13],
        [3,8,11,12],
        [4,7,8,10],
        [4,6,9,11],
        [5,7,9,12],
        [5,6,8,13]
    ]
    perm_map = {
        i + 1: int(x) for i, x in enumerate(permutation.split(","))
    }
    inverse_perm_map = {
        v: k for k, v in perm_map.items()
    }
    perm = [
        [perm_map[x] for x in y] for y in sol
    ]
    return [perm[inverse_perm_map[i] - 1] for i in range(1, 14)]


class ProblemKonhauser20191(Problem):
    config = ProblemConfig(
        name=Problem.get_name(__file__),
        statement=PROBLEM_TEMPLATE,
        formatting_instructions=LIST_FORMATTING_TEMPLATE,
        parameters=["permutation"],
        source="Konhauser Problemfest 2019 P1",
        original_parameters={"permutation": "1,2,3,4,5,6,7,8,9,10,11,12,13"},
        problem_url="https://www.macalester.edu/mscs/wp-content/uploads/sites/591/2019/02/KP-2019-.pdf#page=1",
        solution_url="https://www.macalester.edu/mscs/wp-content/uploads/sites/591/2019/02/KP-2019-.pdf#page=4",
        original_solution=get_solution("1,2,3,4,5,6,7,8,9,10,11,12,13"),
        tags=[Tag.COMBINATORICS, Tag.FIND_ANY, Tag.IS_ORIGINAL, Tag.IS_GENERALIZED]
    )
    permutation: str

    def __init__(self, permutation: str):
        self.permutation = permutation

    def get_init_table(self) -> list[list[int]]:
        perm = {
            i + 1: int(x) for i, x in enumerate(self.permutation.split(","))
        }
        assignments = {
            perm[1]: (perm[2], perm[3], perm[4], perm[5]),
            perm[4]: (perm[1], perm[5], perm[10], perm[11]),
            perm[7]: (perm[2], perm[6], perm[10], perm[12]),
            perm[10]: (perm[4], perm[7], perm[8], perm[10]),
            perm[13]: (perm[5], perm[6], perm[8], perm[13]),
        }
        return assignments, perm
    
    def get_table_latex(self, table):
        return "\n".join([f"{k}: {','.join([str(v) for v in table[k]])} \\\\" if k in table else f"{k}: Not assigned yet \\\\" for k in range(1, 14)])

    def get_problem(self):
        assignments, perm = self.get_init_table()
        a,b,c,d,e = perm[1], perm[4], perm[7], perm[10], perm[13]
        return PROBLEM_TEMPLATE.format(a=a, b=b, c=c, d=d, e=e, table=self.get_table_latex(assignments))

    def check(self, sol: list[list[int]]) -> bool:
        check_format = self.check_format(sol, expected_length=13, is_integer=True, min_val_inclusive=1, 
                                         max_val_inclusive=13)
        if not check_format[0]:
            return check_format
        if any(len(p) != 4 for p in sol):
            return False, "Each project needs exactly four students.", CheckerTag.INCORRECT_SOLUTION
        assignments, perm = self.get_init_table()
        for k, val in assignments.items():
            if len(val) != len(sol[k - 1]):
                return False, f"Project {k} should have {len(val)} students.", CheckerTag.INCORRECT_SOLUTION
            if ",".join([str(x) for x in sorted(val)]) != ",".join([str(x) for x in sorted(sol[k - 1])]):
                return False, f"Project {k} should have the students {val}.", CheckerTag.INCORRECT_SOLUTION
        student_pairs = []
        for i, assignment in enumerate(sol):
            for j, student_1 in enumerate(assignment):
                for student_2 in assignment[:j]:
                    if student_1 == student_2:
                        return False, f"Student {student_1} is assigned to the same project twice.", CheckerTag.INCORRECT_SOLUTION
                    if student_1 != student_2 and (student_1, student_2) in student_pairs:
                        return False, f"Students {student_1} and {student_2} are assigned to the same project twice.", CheckerTag.INCORRECT_SOLUTION
                    student_pairs.append((student_1, student_2))
                    student_pairs.append((student_2, student_1))
                if i+1 not in sol[student_1 - 1]:
                    return False, f"Student {student_1} is not assigned to project {i+1}, but should be due to reciprocity.", CheckerTag.INCORRECT_SOLUTION
        return True, "OK", CheckerTag.CORRECT
        
    @staticmethod
    def generate() -> "ProblemKonhauser20191":
        random_perm = list(range(1, 14))
        random.shuffle(random_perm)
        random_perm = ",".join([str(x) for x in random_perm])
        return ProblemKonhauser20191(random_perm)
    
    def get_solution(self):
        return get_solution(self.permutation)
