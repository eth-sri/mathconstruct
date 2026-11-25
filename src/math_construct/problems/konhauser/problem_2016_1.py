from math_construct.problems.templates import TEMPLATES
PROBLEM_TEMPLATE = TEMPLATES["konhauser/problem_2016_1.py"]

import random
from fractions import Fraction
from math_construct.problems.problem import Problem, ProblemConfig, Tag, CheckerTag
from math_construct.utils import latex2sympy_fixed

LIST_FORMATTING_TEMPLATE = r"""Output the answer as a comma separated list of lists inside of $\boxed{...}$. Each list first contains the current time in days, then a list of the worms' current lengths before the cut, and then a list of the worms' current lengths after the cut.

For instance, to cut a worm of length 1 into two worms of length 0.5 at time $\frac{1}{2}$, you would output '$\frac{1}{2}, (1), (0.5, 0.5)$'. A correct solution to produce $4$ worms in 1 day would be:
$\boxed{
    (0, (1), (0.5, 0.5)),
    (\frac{1}{2}, (1, 1), (0.5, 0.5, 1)),
    (\frac{1}{2}, (1, 0.5, 0.5), (0.5, 0.5, 0.5, 0.5)),
}$
Note that you cannot cut more than one worm in a single line. The last line where all worms are full-grown at time 1 must be omitted."""


def get_solution(number):
    steps = [[0, [1], [Fraction(1, 2 ** (number - 1)), Fraction(1 - 1 / 2 ** (number - 1))]]]
    current_worms = [Fraction(1, 2 ** (number - 1)), Fraction(1 - 1 / 2 ** (number - 1))]
    current_time = 0
    while len([worm for worm in current_worms if worm > 0.999999999]) < number:
        extra_time = min([1 - worm for worm in current_worms if worm < 1])
        current_time += extra_time
        current_worms = [min(1, worm + extra_time) for worm in current_worms]
        if all([worm > 0.999999999 for worm in current_worms]):
            break
        grown_worm_index = current_worms.index(1)
        min_size_worm = min(current_worms)
        new_worms = current_worms[:grown_worm_index] + current_worms[grown_worm_index + 1:] + [min_size_worm, 1 - min_size_worm]
        steps.append([
            current_time, current_worms, new_worms
        ])
        current_worms = new_worms[:]
    return steps

class ProblemKonhauser20161(Problem):
    config = ProblemConfig(
        name=Problem.get_name(__file__),
        statement=PROBLEM_TEMPLATE,
        formatting_instructions=LIST_FORMATTING_TEMPLATE,
        parameters=["number", "time"],
        source="Konhauser Problemfest 2016 P1",
        problem_url="https://www.macalester.edu/mscs/wp-content/uploads/sites/591/2016/03/Konhauser2016.pdf#page=1",
        solution_url="https://www.macalester.edu/mscs/wp-content/uploads/sites/591/2016/03/Konhauser2016.pdf#page=6",
        original_parameters={"time": "1", "number": 6},
        original_solution=get_solution(6),
        tags=[Tag.COMBINATORICS, Tag.FIND_ANY, Tag.IS_ORIGINAL, Tag.IS_GENERALIZED]
    )
    time: str
    number: int

    def __init__(self, time: str, number: int):
        self.time = time
        self.number = number

    def get_problem(self):
        float_time = float(latex2sympy_fixed(self.time).evalf())
        if float_time < 1:
            timestr = f"${self.time}$ of a day"
        else:
            timestr = "1 day"
        return PROBLEM_TEMPLATE.format(number=self.number, timestr=timestr)

    def check(self, sol: list[list[float]]) -> bool:
        float_time = float(latex2sympy_fixed(self.time).evalf())
        current_worms = [1]
        current_time = 0
        for row in sol:
            if len(row) != 3:
                return False, f"Incorrect number of elements in a row for {row}", CheckerTag.INCORRECT_FORMAT
        for row in sol:
            if row[0] < current_time:
                return False, f"Time is decreasing for {row} with current time {current_time}", CheckerTag.INCORRECT_SOLUTION
            if row[0] > float_time + 1e-6:
                return False, f"Time is larger than alloted time {float_time} for {row}.", CheckerTag.INCORRECT_SOLUTION
            if row[0] > current_time:
                current_worms = [min(1, worm + (row[0] - current_time)) for worm in current_worms]
            if not sorted(current_worms) == sorted(row[1]):
                return False, f"Incorrect worm lengths before cut for {row}, expected {current_worms}.", CheckerTag.INCORRECT_SOLUTION
            if len(row[1]) != len(row[2]) - 1:
                return False, f"Incorrect number of worms after cut for {row}.", CheckerTag.INCORRECT_SOLUTION
            cut_worm = None
            worms_row_2 = row[2].copy()
            for worm in row[1]:
                if worm not in worms_row_2:
                    if cut_worm is not None or worm != 1:
                        return False, f"More than one worm was cut or worm with length != was cut for {row}", CheckerTag.INCORRECT_SOLUTION
                    cut_worm = worm
                else:
                    worms_row_2.remove(worm)
            if not len(worms_row_2) == 2:
                return False, f"Incorrect number of worms after cut for {row}. Worms in cut: {worms_row_2}", CheckerTag.INCORRECT_SOLUTION
            if not all(0 < w < 1 for w in worms_row_2):
                return False, "Cut pieces must have lengths strictly between 0 and 1", CheckerTag.INCORRECT_SOLUTION
            if not sum(worms_row_2) == 1:
                return False, f"Incorrect worm lengths after cut for {row}. {worms_row_2} does not sum to 1.", CheckerTag.INCORRECT_SOLUTION
            current_worms = row[2].copy()
            current_time = row[0]

        if current_time < float_time:
            current_worms = [min(1, worm + (float_time - current_time)) for worm in current_worms]
        n_fully_grown = sum([1 for worm in current_worms if worm > 0.999])
        if not n_fully_grown == self.number:
            return False, f"Incorrect number of fully grown worms, found {n_fully_grown} but expected {self.number}.", CheckerTag.INCORRECT_SOLUTION
        return True, "OK", CheckerTag.CORRECT
        
    @staticmethod
    def generate() -> "ProblemKonhauser20161":
        number = random.randint(4, 10)
        time = r"\frac{" + str(2 ** (number) - 1) + r"}{" + str(2 ** number) + "}"
        return ProblemKonhauser20161(time, number)

    def get_solution(self):
        return get_solution(self.number)
