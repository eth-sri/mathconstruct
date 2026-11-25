from math_construct.problems.templates import TEMPLATES
PROBLEM_TEMPLATE = TEMPLATES["bulgarian/problem_pms_10_4.py"]

import random
from math_construct.problems.problem import Problem, ProblemConfig, Tag, CheckerTag
import numpy as np
from copy import deepcopy
from sympy import nextprime


EXTRA_FORMATTING_INSTRUCTIONS = r"""Output the answer as a pair of lists inside $\boxed{...}$. The first list should contain the number assigned to each vertex. The second list should contain the edges, represented as pairs of 1-based indices, formatted as lists of length 2. Format the final output as $\boxed{[vertices, edges]}$. For example, $\boxed{[[1,2,3], [[1, 2], [1, 3]]]}$."""

def get_solution(n: int, e: int) -> tuple[list[int], list[tuple[int]]]:
    solutions_dp = [[], []]  # Base cases for n = 0 and n = 1

    for i in range(2, n + 1):
        solutions_dp.append([])

        if i == 2:
            solutions_dp[-1].append(([2, 3], []))
            solutions_dp[-1].append(([2, 4], [(1, 2)]))
        elif i == 3:
            solutions_dp[-1].append(([2, 3, 5], []))
            solutions_dp[-1].append(([2, 4, 5], [(1, 2)]))
            solutions_dp[-1].append(([2, 4, 6], [(1, 2), (1, 3)]))
            solutions_dp[-1].append(([2, 4, 8], [(1, 2), (1, 3), (2, 3)]))
        else:
            prev_solutions = solutions_dp[i - 1]
            max_prev_prime = max(prev_solutions[0][0])
            new_prime = nextprime(max_prev_prime)

            for ei in range(i * (i - 1) // 2 + 1):
                if ei <= (i - 1) * (i - 2) // 2:
                    base_list, base_edges = prev_solutions[ei]
                    new_list = base_list + [new_prime]
                    new_edges = list(base_edges)  # Shallow copy
                else:
                    base_list, base_edges = prev_solutions[ei - (i - 1)]
                    new_list = [num * new_prime for num in base_list] + [new_prime]
                    new_edges = list(base_edges) + [(k, i) for k in range(1,i)]  # Shallow copy

                solutions_dp[-1].append((new_list, new_edges))

    return solutions_dp[n][e]

class ProblemBulPMS20204P10_4(Problem):
    config = ProblemConfig(
        name=Problem.get_name(__file__),
        statement=PROBLEM_TEMPLATE,
        formatting_instructions=EXTRA_FORMATTING_INSTRUCTIONS,
        parameters=["N", "e"],
        source="Bulgarian Spring National Competition 2020 10th Grade P4",
        original_parameters={"N": 15, "e": 43},
        original_solution=get_solution(15, 43),
        problem_url="https://klasirane.com/competitions/PMS/All",
        solution_url="https://klasirane.com/competitions/PMS/All",
        tags=[Tag.COMBINATORICS, Tag.FIND_ANY, Tag.IS_ORIGINAL, Tag.IS_TRANSLATED]
    )
    e: int
    N: int

    def __init__(self, N: int, e:int):
        self.N = N
        self.e = e

    def get_problem(self):
        return PROBLEM_TEMPLATE.format(N=self.N, e=self.e)

    def check(self, x: list[list[str]]) -> bool:
        if len(x) != 2:
            return False, f"Example should contain 2 lists - 1 for vertices, 1 for edges", CheckerTag.INCORRECT_FORMAT
        
        if len(x[0]) != self.N:
            return False, f"Vertex list should contain {self.N} numbers", CheckerTag.INCORRECT_LENGTH
        
        if len(x[1]) != self.e:
            return False, f"Edge list should contain {self.e} tuples", CheckerTag.INCORRECT_FORMAT

        vertices = x[0]
        edges = x[1]
        if any(type(v) != int or v <= 0 for v in vertices) or len(set(vertices)) != len(vertices):
            return False, "Vertex labels must be distinct natural numbers", CheckerTag.INCORRECT_SOLUTION

        for i, edge in enumerate(edges):
            if len(edge) != 2 or edge[0] > self.N or edge[0] < 1 or edge[1] > self.N or edge[1] < 1:
                return False, f"Edge entry should contain a pair of valid indices", CheckerTag.INCORRECT_SOLUTION
            if edge[0] == edge[1]:
                return False, "Self-loops are not edges", CheckerTag.INCORRECT_SOLUTION
            edges[i] = tuple(sorted(edge))
            if vertices[edge[0]-1] % vertices[edge[1]-1] != 0 and vertices[edge[1]-1] % vertices[edge[0]-1] != 0:
                return False, f"Vertices {edge[0]} and {edge[1]} should not be connected but are.", CheckerTag.INCORRECT_SOLUTION
        edge_set = set(edges)
        if len(edge_set) != len(edges):
            return False, "Duplicate edges", CheckerTag.INCORRECT_SOLUTION

        for i in range(self.N):
            for j in range(i+1, self.N):
                if (vertices[i] % vertices[j] == 0 or vertices[j] % vertices[i] == 0) and not (i+1, j+1) in edge_set:
                    return False, f"Vertices {i+1} and {j+1} should be connected but are not.", CheckerTag.INCORRECT_SOLUTION

        
        return True, "OK", CheckerTag.CORRECT

    @staticmethod
    def generate() -> "ProblemBulPMS20204P10_4":
        N = random.randint(10, 20)
        e = random.randint(30, N*(N-1)//2)
        return ProblemBulPMS20204P10_4(N, e)

    def get_solution(self):
        return get_solution(self.N, self.e)
