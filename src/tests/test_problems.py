from math_construct.parsing import parse_answer, match_list_depth
from math_construct.problems import get_all_problem_classes
from fractions import Fraction
from math import factorial
import math
import json
import copy
import pytest
import time

def test_params():
    """Test that the parameters actually appear in the problem statement."""
    problem_classes = get_all_problem_classes()
    for problem_cls in problem_classes:
        if problem_cls.config.name in ["konhauser-2020-9", "konhauser-2019-1", "konhauser-2016-1"]:
            continue
        for param in problem_cls.config.parameters:
            assert f"{{{param}}}" in problem_cls.config.statement, f"Didn't find parameter {param} in problem {problem_cls.config.name}"

def test_json():
    """Test that the json serialization works."""
    from tempfile import NamedTemporaryFile
    problem_classes = get_all_problem_classes()
    for problem_cls in problem_classes:
        print(problem_cls.config.name)
        problem = problem_cls.get_original()
        problem_json = problem.to_json()
        with NamedTemporaryFile(mode="w") as f:
            json.dump(problem_json, f)
            f.seek(0)
            with open(f.name, "r") as f:
                problem_json = json.load(f)
                problem = problem_cls.from_json(problem_json)
                original_solution = problem.config.original_solution
                assert problem.check_raw(original_solution)

# @pytest.mark.skip(reason="Slow, skip for now")
def test_generate():
    """Test that the generate method works."""
    problem_classes = get_all_problem_classes()
    for problem_cls in problem_classes:
        print(problem_cls.config.name)
        for problem in problem_cls.generate_multiple(4):
            soll = problem.get_solution()
            print(problem.to_json()["param_values"])
            t = time.time()
            if soll is not None:
                assert problem.check_raw(soll)
            print(time.time() - t)

def test_uniqueness():
    problem_class = get_all_problem_classes()
    for problem_cls in problem_class:
        print(problem_cls.config.name)
        orig_problem = problem_cls.get_original()
        orig_sol = orig_problem.config.original_solution
        if problem_cls.config.name in ["imc-2018-6"]: # for these problems its fine
            continue
        if isinstance(orig_sol, (int, float, Fraction)) or len(orig_sol) == 1:
            continue
        if isinstance(orig_sol, list) and all(isinstance(sol, (tuple, list)) for sol in orig_sol) and \
            all(isinstance(el, (int, float, Fraction)) for sol in orig_sol for el in sol):
            if len(set(tuple(sol) for sol in orig_sol)) == len(orig_sol): # should be unique
                assert not orig_problem.check_raw([orig_sol[0]] + orig_sol[:-1])
        if isinstance(orig_sol, list) and all(isinstance(sol, (int, float, Fraction)) for sol in orig_sol):
            if len(set(orig_sol)) == len(orig_sol): # should be unique
                assert not orig_problem.check_raw([orig_sol[0]] + orig_sol[:-1])

def test_length():
    problem_class = get_all_problem_classes()
    for problem_cls in problem_class:
        print(problem_cls.config.name)
        orig_problem = problem_cls.get_original()
        orig_sol = orig_problem.config.original_solution
        if problem_cls.config.name in ["dutch-2024-2"]: # for these problems its fine
            continue
        if isinstance(orig_sol, (int, float, Fraction)) or len(orig_sol) == 1:
            continue
        try:
            assert not orig_problem.check_raw(orig_sol[:-1])
        except:
            pass

def test_str():
    problem_classes = get_all_problem_classes()
    for problem_cls in problem_classes:
        print("========================")
        print(problem_cls.config.name)
        print(problem_cls.config.original_parameters)
        orig_problem = problem_cls.get_original()
        orig_problem_txt = str(orig_problem)
        print(orig_problem_txt)
        if problem_cls.config.name in ["konhauser-2020-9", "konhauser-2019-1"]:
            continue
        for param, param_value in problem_cls.config.original_parameters.items():
            if type(param_value) == int or type(param_value) == str:
                assert str(param_value) in orig_problem_txt

def test_all_problems():
    problem_classes = get_all_problem_classes()
    for problem_cls in problem_classes:
        orig_problem = problem_cls.get_original()
        assert orig_problem.check_raw(orig_problem.config.original_solution)

def test_problem0():
    from math_construct.problems.backups.problem0 import Problem0
    orig_problem = Problem0.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)

    assert Problem0(a=1, b=1).check_raw(["7"])
    assert Problem0(a=2, b=2).check_raw(["11", "11"])
    assert not Problem0(a=2, b=2).check_raw(["12", "11"])

def test_problem3():
    from math_construct.problems.usamts.problem_1998_4_1 import Problem3
    orig_problem = Problem3.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    assert Problem3(a=2, b=1, n=3).check_raw("112")
    assert not Problem3(a=2, b=1, n=3).check_raw("122")
    for a in range(2, 10, 2):
        for b in range(1, 10, 2):
            for n in range(10, 30):
                problem = Problem3(a, b, n)
                assert problem.check_raw(problem.get_solution())

def test_problem5():
    from math_construct.problems.backups.usamo_problem_1976_1 import Problem5
    orig_problem = Problem5.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    assert not orig_problem.check_raw(["wwbwbb", "bbwbwb", "bwwbbw", "bbbwww"])
    assert not Problem5(n_rows=2, n_cols=2).check_raw(["ww", "ww"])
    assert Problem5(n_rows=2, n_cols=2).check_raw(["ww", "bb"])
    for n_rows in range(2, 7):
        for n_cols in range(2, 7):
            if n_rows <= 4 or n_cols <= 4:
                assert Problem5(n_rows, n_cols).check_raw(Problem5(n_rows, n_cols).get_solution())
    
def test_problem6():
    from math_construct.problems.backups.usamts_problem_1998_2_2 import Problem6, get_solution
    orig_problem = Problem6.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    assert Problem6(k=100).check_raw(get_solution(100))

def test_problem7():
    from math_construct.problems.usamts.problem_1999_1_2 import Problem7
    orig_problem = Problem7.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    assert not orig_problem.check_raw([2, 3, (10**1999-1)//9, (5*10**1998+1)//3+1])

    for k in range(100, 1000):
        new_problem = Problem7(k)
        assert new_problem.check_raw(new_problem.get_solution())

def test_problem9():
    from math_construct.problems.usamts.problem_2001_3_3 import Problem9
    orig_problem = Problem9.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    for n in range(4, 100):
        assert Problem9(n).check_raw(Problem9(n).get_solution())

def test_problem10():
    from math_construct.problems.usamts.problem_2001_4_4 import Problem10, get_solution
    orig_problem = Problem10.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    assert Problem10(k=5).check_raw(get_solution(5))
    

def test_problem12():
    from math_construct.problems.usamts.problem_2002_1_2 import Problem12
    orig_problem = Problem12.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    for k in range(1, 30):
        assert Problem12(k).check_raw(Problem12(k).get_solution())

def test_problem13():
    from math_construct.problems.backups.problem_1990_3 import Problem13, get_solution
    orig_problem = Problem13.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    for i in range(30, 500, 13):
        assert Problem13(2*i + 1).check_raw(get_solution(2*i+1))
        assert not Problem13(2*i +1).check_raw([i for i in range(1, 34)])
    
    for problem in Problem13.generate_multiple(10):
        print(problem.get_solution(), problem.n)
        assert problem.check_raw(problem.get_solution())

def test_problem14():
    from math_construct.problems.usamo.problem_2000_4 import Problem14, get_solution
    orig_problem = Problem14.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)

    assert not Problem14(2, 3).check_raw(["oo", "ox"])
    assert not Problem14(2, 3).check_raw(["ox", "xx"])
    assert Problem14(2, 2).check_raw(["ox", "ox"])
    
    assert Problem14(3, 3).check_raw(["oxo", "oxo", "oxo"])
    assert not Problem14(3, 3).check_raw(["oxo", "xxo", "ooo"])

def test_problem15():
    from math_construct.problems.usamo.problem_2001_1 import Problem15
    orig_problem = Problem15.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    assert Problem15(30).check_raw(orig_problem.config.original_solution)

def test_problem16():
    from math_construct.problems.tot.problem_2018_1 import Problem16, get_solution
    orig_problem = Problem16.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    assert Problem16(3).check_raw(get_solution(3))
    assert not Problem16(3).check_raw([Fraction(1,2), Fraction(1,3), Fraction(2,3)])
    
def test_problem17():
    from math_construct.problems.imo_shortlist.problem_2001_c5 import Problem17, get_solution
    orig_problem = Problem17.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    assert Problem17(1).check_raw([[2,0,2,0]])
    assert not Problem17(1).check_raw([[2,0,2,1]])

def test_problem18():
    from math_construct.problems.imo_shortlist.problem_2001_c6 import Problem18, get_solution
    orig_problem = Problem18.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    assert not orig_problem.check_raw(orig_problem.config.original_solution[:-1])
    assert Problem18(6).check_raw(get_solution(6))

def test_problem19():
    from math_construct.problems.imo_shortlist.problem_2002_n4 import Problem19, get_solution
    orig_problem = Problem19.get_original()
    orig_sol = orig_problem.config.original_solution
    assert orig_problem.check_raw(orig_sol)
    assert not orig_problem.check_raw(orig_sol[:-1])
    assert not orig_problem.check_raw([orig_sol[0]] + orig_sol[:-1])
    assert not Problem19(1).check_raw([[12, 1, 2, 2]])
    

def test_problem20():
    from math_construct.problems.imo_shortlist.problem_2001_n6 import Problem20, get_solution
    orig_problem = Problem20.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    assert Problem20(4, 100).check_raw([1, 2, 5, 100])
    assert not Problem20(4, 100).check_raw([1, 2, 4, 5])
    for _ in range(100):
        problem = Problem20.generate()
        assert problem.check_raw(get_solution(problem.p, problem.n))

def test_problem21():
    from math_construct.problems.tot.problem_2005_1 import Problem21
    orig_problem = Problem21.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    assert Problem21(3).check_raw([1, 2, 4])
    assert not Problem21(3).check_raw([1, 2, 3])

def test_problem22():
    from math_construct.problems.imo_shortlist.problem_2022_a5 import Problem22, get_solution
    orig_problem = Problem22.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    assert Problem22(2).check_raw(get_solution(2))
    assert Problem22(3).check_raw(get_solution(3))
    assert Problem22(4).check_raw(get_solution(4))
    assert not Problem22(2).check_raw([1, 1, 1])

def test_problem23():
    from math_construct.problems.imo_shortlist.problem_2020_a3 import Problem23
    orig_problem = Problem23.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    assert Problem23().check_raw(orig_problem.config.original_solution)
    assert not Problem23().check_raw([1, 1, 1, 1])

def test_problem_dutch_2009_4():
    from math_construct.problems.backups.problem_2009_4 import ProblemDutch20094
    orig_problem = ProblemDutch20094.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    assert not orig_problem.check_raw(orig_problem.config.original_solution[:-1])
    assert not orig_problem.check_raw([[el[2]] for el in orig_problem.config.original_solution])
    assert not orig_problem.check_raw([el[:2] for el in orig_problem.config.original_solution])
    for problem in ProblemDutch20094.generate_multiple(10, 30):
        assert problem.check_raw(problem.get_solution())

    new_problem = ProblemDutch20094(3, 1)
    assert new_problem.check_raw([[11, 11, 121]])
    assert not new_problem.check_raw([[3, 3, 9]])
    assert not new_problem.check_raw([[11, 11, 121], [12, 21, 252]])
    new_problem = ProblemDutch20094(3, 2)
    assert not new_problem.check_raw([[11, 11, 121], [11, 11, 121]])

def test_problem_dutch_2010_4():
    from math_construct.problems.dutch.problem_2010_4 import ProblemDutch20104
    orig_problem = ProblemDutch20104.get_original()
    orig_sol = orig_problem.config.original_solution
    assert orig_problem.check_raw(orig_sol)
    assert not orig_problem.check_raw(orig_sol[:-1])
    assert not orig_problem.check_raw(orig_sol[:4] + orig_sol[:4])

    for problem in ProblemDutch20104.generate_multiple(20, 100):
        assert problem.check_raw(problem.get_solution())

    new_problem = ProblemDutch20104(1, 5)
    assert new_problem.check_raw([[Fraction(2, 12), Fraction(2, 12)]])
    assert new_problem.check_raw([[1 / 6, 1 / 6]])

def test_problem_dutch_2011_3():
    from math_construct.problems.backups.problem_2011_3 import ProblemDutch20113
    orig_problem = ProblemDutch20113.get_original()
    orig_sol = orig_problem.config.original_solution
    assert orig_problem.check_raw(orig_sol)
    assert not orig_problem.check_raw(orig_sol[:-1])
    orig_sol[0][0] += 1
    assert not orig_problem.check_raw(orig_sol)
    orig_sol[0][0] -= 1
    orig_sol[0][1] -= 2
    orig_sol[0][2] += 2
    assert not orig_problem.check_raw(orig_sol)
    new_problem = ProblemDutch20113(4)
    sol = [
        [0, 1, 0, 1],
        [1, 0, 1, 1],
        [3, 1, 0, 0],
        [1, 1, 3, 0],
    ]
    assert new_problem.check_raw(sol)

def test_problem_dutch_2012_2():
    from math_construct.problems.dutch.problem_2012_2 import ProblemDutch20122
    orig_problem = ProblemDutch20122.get_original()
    orig_sol = orig_problem.config.original_solution
    assert orig_problem.check_raw(orig_sol)
    assert not orig_problem.check_raw(orig_sol[:-1])
    orig_sol[0][0] -= 1
    assert not orig_problem.check_raw(orig_sol)

    for problem in [ProblemDutch20122(i) for i in range(3, 20, 2)]:
        assert problem.check_raw(problem.get_solution())

def test_problem_dutch_2014_3():
    from math_construct.problems.dutch.problem_2014_3 import ProblemDutch20143
    orig_problem = ProblemDutch20143.get_original()
    orig_sol = orig_problem.config.original_solution
    assert orig_problem.check_raw(orig_sol)
    assert not orig_problem.check_raw(orig_sol[:-1])
    orig_sol[0][0] += 1
    assert not orig_problem.check_raw(orig_sol)
    orig_sol[0][0] -= 1
    orig_sol[-1][2] += 1
    assert not orig_problem.check_raw(orig_sol)
    for problem in ProblemDutch20143.generate_multiple(10):
        assert problem.check_raw(problem.get_solution())

def test_problem_dutch_2018_1():
    from math_construct.problems.dutch.problem_2018_1 import ProblemDutch20181
    orig_problem = ProblemDutch20181.get_original()
    orig_sol = orig_problem.config.original_solution
    assert orig_problem.check_raw(orig_sol)
    assert not orig_problem.check_raw(orig_sol[:-1])
    assert not orig_problem.check_raw(orig_sol[:-1] + [orig_sol[0]])
    assert not orig_problem.check_raw(orig_sol[:-1] + [484])
    assert not orig_problem.check_raw(orig_sol[:-1] + [4448884448])

    for problem in [ProblemDutch20181(i, 1) for i in range(11, 20)]: 
        assert problem.check_raw(problem.get_solution())

    new_problem = ProblemDutch20181(3, 1)
    assert not new_problem.check_raw([444])
    assert not new_problem.check_raw([484])
    new_problem = ProblemDutch20181(6, 1)
    assert new_problem.check_raw([444444])

def test_problem_dutch_2018_2():
    from math_construct.problems.dutch.problem_2018_2 import ProblemDutch20182
    orig_problem = ProblemDutch20182.get_original()
    orig_sol = orig_problem.config.original_solution
    assert orig_problem.check_raw(orig_sol)
    assert not orig_problem.check_raw(orig_sol[:-1])
    assert not orig_problem.check_raw(orig_sol[:-1] + [orig_sol[0]])
    assert not orig_problem.check_raw(orig_sol[:-1] + [[]])
    assert orig_problem.check_raw(orig_sol[1:] + [orig_sol[0][::-1]])

    for problem in [ProblemDutch20182(i, 1) for i in range(2, 20)]: 
        assert problem.check_raw(problem.get_solution())

    new_problem = ProblemDutch20182(6, 1)
    assert new_problem.check_raw([[1, 2, 3, 4, 5, 6]])
    assert new_problem.check_raw([[6]])
    assert new_problem.check_raw([[2, 4, 6]])
    assert not new_problem.check_raw([[2, 3, 6]])

def test_problem_dutch_2019_2():
    from math_construct.problems.dutch.problem_2019_2 import ProblemDutch20192
    orig_problem = ProblemDutch20192.get_original()
    orig_sol = orig_problem.config.original_solution
    assert orig_problem.check_raw(orig_sol)
    assert not orig_problem.check_raw(orig_sol[:-1])
    assert not orig_problem.check_raw(orig_sol[:-1] + [orig_sol[0]])
    orig_sol[0][0][0] += 1
    assert not orig_problem.check_raw(orig_sol)
    orig_sol[0][0][-1] -= 1
    assert not orig_problem.check_raw(orig_sol)
    orig_sol[0][-1][0] -= 1
    assert not orig_problem.check_raw(orig_sol)

    for problem in [ProblemDutch20192(i, 2) for i in range(2, 8)]: 
        assert problem.check_raw(problem.get_solution())

    new_problem = ProblemDutch20192(2, 1)
    assert new_problem.check_raw(
        [[
            [0, 0, 1, 1],
            [0, 0, 1, 1],
            [1, 1, 0, 0],
            [1, 1, 0, 0]
        ]]
    )
    assert new_problem.check_raw(
        [[
            [0, 1, 1],
            [1, 0, 1],
            [1, 1, 0],
        ]]
    )
    assert not new_problem.check_raw(
        [[
            [0, 1, 1],
            [1, 0, 1],
        ]]
    )
    assert not new_problem.check_raw(
        [[
            [0, 1, 0],
            [1, 0, 1],
            [0, 1, 0],
        ]]
    )

def test_problem_dutch_2019_4():
    from math_construct.problems.misc.problem_vwo_2019_4 import ProblemVWO20194
    orig_problem = ProblemVWO20194.get_original()
    orig_sol = orig_problem.config.original_solution
    assert orig_problem.check_raw(orig_sol)
    assert not orig_problem.check_raw(orig_sol[:-1])
    orig_sol[3] += 1
    assert not orig_problem.check_raw(orig_sol)

    for problem in [ProblemVWO20194(i, i) for i in range(4, 40, 2)]:
        assert problem.check_raw(problem.get_solution())
    
    for problem in [ProblemVWO20194(i, i - 1) for i in range(5, 40, 2)]:
        assert problem.check_raw(problem.get_solution())

    new_problem = ProblemVWO20194(5, 4)
    sol = [1, 2, 3, 4, 5]
    assert new_problem.check_raw(sol)
    assert not new_problem.check_raw(sol[::-1])
    assert new_problem.check_raw([2, 3, 4, 5, 1])

def test_problem_dutch_2021_3():
    from math_construct.problems.backups.problem_2021_3 import ProblemDutch20213
    orig_problem = ProblemDutch20213.get_original()
    orig_sol = orig_problem.config.original_solution
    assert orig_problem.check_raw(orig_sol)
    assert not orig_problem.check_raw(orig_sol[:-2])
    orig_sol[1][0] += 1
    assert not orig_problem.check_raw(orig_sol)

    for problem in ProblemDutch20213.generate_multiple(10):
        assert problem.check_raw(problem.get_solution())

    new_problem = ProblemDutch20213(7)
    sol = [
        [0, 0],
        [1, 0],
        [1, -2],
        [-2, -2],
        [-2, -6],
        [-7, -6],
        [-7, 0],
        [0, 0],
    ]
    assert new_problem.check_raw(sol)

def test_problem_dutch_2024_2():
    from math_construct.problems.dutch.problem_2024_2 import ProblemDutch20242
    orig_problem = ProblemDutch20242.get_original()
    orig_sol = orig_problem.config.original_solution
    assert orig_problem.check_raw(orig_sol)
    assert not orig_problem.check_raw(orig_sol[:-2])
    orig_sol[1][0] += 1
    assert not orig_problem.check_raw(orig_sol)

    for problem in ProblemDutch20242.generate_multiple(10):
        assert problem.check_raw(problem.get_solution())

    new_problem = ProblemDutch20242(5)
    sol = [
        [0, 0],
        [1, 1],
        [3, 2],
        [2, -1],
        [1, -5],
        [0, 0]
    ]
    assert new_problem.check_raw(sol)

def test_bxmo_2019_2():
    from math_construct.problems.bxmo.problem_2019_2 import ProblemBxMO20192
    orig_problem = ProblemBxMO20192.get_original()
    orig_sol = orig_problem.config.original_solution
    assert orig_problem.check_raw(orig_sol)
    assert not orig_problem.check_raw(orig_sol[:-1])
    orig_sol[0][0] += 2
    orig_sol[0][4] -= 2
    assert not orig_problem.check_raw(orig_sol)
    orig_sol[0][0] -= 2
    orig_sol[0][4] += 2
    orig_sol[0][0] += 1
    assert not orig_problem.check_raw(orig_sol)

    for problem in [ProblemBxMO20192(2 * n + 1) for n in range(2, 15)]:
        assert problem.check_raw(problem.get_solution())

    new_problem = ProblemBxMO20192(5)
    sol = [
        [0, 0, 2, 0, 0],
        [0, 2, 1, 2, 0],
        [2, 1, 2, 1, 2],
        [0, 2, 1, 2, 0],
        [0, 0, 2, 0, 0]
    ]
    assert new_problem.check_raw(sol)

def test_bxmo_problem_2020_4():
    from math_construct.problems.bxmo.problem_2020_4 import ProblemBxMO20204
    orig_problem = ProblemBxMO20204.get_original()
    orig_sol = orig_problem.config.original_solution
    assert orig_problem.check_raw(orig_sol)

    for problem in [ProblemBxMO20204(n) for n in range(10, 100, 2)]:
        assert problem.check_raw(problem.get_solution())

    new_problem = ProblemBxMO20204(10)
    assert new_problem.check_raw(2 ** 19 * 405)
    assert new_problem.check_raw(2 ** 9 * 405)
    assert not new_problem.check_raw(2 ** 8 * 405)

def test_bxmo_problem_2021_2():
    from math_construct.problems.bxmo.problem_2021_2 import ProblemBxMO20212
    orig_problem = ProblemBxMO20212.get_original()
    orig_sol = orig_problem.config.original_solution
    assert orig_problem.check_raw(orig_sol)
    orig_sol[0][0] -= 1
    assert not orig_problem.check_raw(orig_sol)
    orig_sol[2][1] += 1
    assert not orig_problem.check_raw(orig_sol)

    for problem in ProblemBxMO20212.generate_multiple(50):
        assert problem.check_raw(problem.get_solution())

    new_problem = ProblemBxMO20212(7, 5)

    sol = [
        [1, 0, 0, 0, 1],
        [0, 0, 1, 0, 0],
        [0, 1, 0, 1, 0],
        [0, 1, 0, 0, 0],
        [1, 0, 0, 0, 0],
    ]

    assert new_problem.check_raw(sol)
    sol[1], sol[2] = sol[2], sol[1]
    assert new_problem.check_raw(sol)
    assert not new_problem.check_raw([
        [1, 0, 0, 0, 1],
        [0, 1, 0, 0, 0],
        [0, 1, 0, 1, 0],
        [0, 1, 0, 0, 0],
        [1, 0, 0, 0, 0],
    ])

def test_problem_bxmo_2015_4():
    from math_construct.problems.bxmo.problem_2015_4 import ProblemBxMO20154
    orig_problem = ProblemBxMO20154.get_original()
    orig_sol = orig_problem.config.original_solution
    assert orig_problem.check_raw(orig_sol)
    assert not orig_problem.check_raw(orig_sol[:-1])
    orig_sol[0][0] += 1
    assert not orig_problem.check_raw(orig_sol)
    orig_sol[0][0] += 55
    orig_sol[0][1] += 56
    orig_sol[0][2] += 57
    assert not orig_problem.check_raw(orig_sol)

    for problem in [ProblemBxMO20154(n) for n in range(5, 20)]:
        assert problem.check_raw(problem.get_solution())

    new_problem = ProblemBxMO20154(5)
    sol = [
        [1,6,11],
        [2,7,12],
        [3,8,13],
        [4,9,14],
        [5,10,15]
    ]
    assert new_problem.check_raw(sol)
    sol_false = [
        [1,5,9,13],
        [2,6,10,14],
        [3,7,11,15],
        [4,8,12]
    ]
    assert not new_problem.check_raw(sol_false)

def test_problem_bxmo_2011_1():
    from math_construct.problems.bxmo.problem_2011_1 import ProblemBxMO20111
    orig_problem = ProblemBxMO20111.get_original()
    orig_sol = orig_problem.config.original_solution
    assert orig_problem.check_raw(orig_sol)
    assert not orig_problem.check_raw(orig_sol[:-1])
    assert not orig_problem.check_raw(orig_sol[:-1] + [orig_sol[0]])

    for problem in [ProblemBxMO20111.generate() for _ in range(50)]:
        assert problem.check_raw(problem.get_solution())

    new_problem = ProblemBxMO20111(3, 9, 1, 10)
    assert new_problem.check_raw([[2, 2 * 2 ** 3]])
    assert new_problem.check_raw([[10, 10 * 2 ** 4]])
    assert not new_problem.check_raw([[26, 26 * 2 ** 5]])

def test_problem_serbiantst_2020_4(): 
    from math_construct.problems.serbian.problem_2020_tst_4 import ProblemSerbianTst2020_4
    orig_problem = ProblemSerbianTst2020_4.get_original()
    orig_sol = orig_problem.config.original_solution
    assert orig_problem.check_raw(orig_sol)
    assert not orig_problem.check_raw(orig_sol[:-1])
    for m in range(1, 15):
        problem = ProblemSerbianTst2020_4(m)
        sol = problem.get_solution()
        print(sol)
        assert problem.check_raw(sol)
        sol[m-1][0] += Fraction(1, 2)
        assert not problem.check_raw(sol)

def test_problem_serbiantst_2023_1(): 
    from math_construct.problems.serbian.problem_2023_tst_1 import ProblemSerbianTst2023_1
    orig_problem = ProblemSerbianTst2023_1.get_original()
    orig_sol = orig_problem.config.original_solution
    assert orig_problem.check_raw(orig_sol)
    assert not orig_problem.check_raw(orig_sol[:-1])
    for s in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
        n = sum(range(s+1))
        maxe = sum([i * (n-i) for i in range(s+1)]) // 2 
        sol = ProblemSerbianTst2023_1(n, maxe).get_solution()
        assert ProblemSerbianTst2023_1(n, maxe).check_raw(sol)

def test_problem_serbiantst_2022_3(): 
    from math_construct.problems.serbian.problem_2022_tst_3 import ProblemSerbianTst2022_3
    orig_problem = ProblemSerbianTst2022_3.get_original()
    orig_sol = orig_problem.config.original_solution
    assert orig_problem.check_raw(orig_sol)
    assert not orig_problem.check_raw(orig_sol[:-1])
    for m in range(2, 15):
        problem = ProblemSerbianTst2022_3(m)
        sol = problem.get_solution()
        assert problem.check_raw(sol)
    assert not ProblemSerbianTst2022_3(1).check_raw([3, 1, 1, 1])

def test_swiss_2024_3():
    from math_construct.problems.swiss.problem_2024_3 import ProblemSwiss20243
    orig_problem = ProblemSwiss20243.get_original()
    orig_sol = orig_problem.config.original_solution
    assert orig_problem.check_raw(orig_sol)
    assert not orig_problem.check_raw(orig_sol[:-1])
    orig_sol[0] += 1
    assert not orig_problem.check_raw(orig_sol)

    new_problem = ProblemSwiss20243(6, 28)
    b = math.sqrt((6 + math.sqrt(8)) / 2)
    sol = [
        math.sqrt(7), b,  math.sqrt(7) / b, 1
    ]
    assert new_problem.check_raw(sol)
    sol[0] += 0.01
    assert not new_problem.check_raw(sol)
    for problem in ProblemSwiss20243.generate_multiple(10):
        assert problem.check_raw(problem.get_solution())

def test_swiss_selection_2024_12():
    from math_construct.problems.swiss.problem_2024_12_selection import ProblemSwissSelection202412
    orig_problem = ProblemSwissSelection202412.get_original()
    orig_sol = orig_problem.config.original_solution
    assert orig_problem.check_raw(orig_sol)
    assert not orig_problem.check_raw("n+2")
    assert not orig_problem.check_raw("n")
    assert not orig_problem.check_raw("n^2")
    assert not orig_problem.check_raw("m+1")

def test_swiss_selection_2024_11():
    from math_construct.problems.swiss.problem_2024_11_selection import ProblemSwissSelection202411
    orig_problem = ProblemSwissSelection202411.get_original()
    orig_sol = orig_problem.config.original_solution
    assert orig_problem.check_raw(orig_sol)
    assert not orig_problem.check_raw(orig_sol[:-1])
    assert not orig_problem.check_raw(orig_sol[:-1] + [orig_sol[0]])

    assert 2 * 4 * ProblemSwissSelection202411.g(4) == 16
    assert 2 * 5 * ProblemSwissSelection202411.g(5) == 50
    assert 2 * 6 * ProblemSwissSelection202411.g(6) == 96

    for problem in ProblemSwissSelection202411.generate_multiple(10, seed_start=1):
        assert problem.check_raw(problem.get_solution())

def test_swiss_selection_2024_8():
    from math_construct.problems.swiss.problem_2024_8_selection import ProblemSwissSelection20248
    orig_problem = ProblemSwissSelection20248.get_original()
    orig_sol = orig_problem.config.original_solution
    assert orig_problem.check_raw(orig_sol)
    assert not orig_problem.check_raw("x")
    assert not orig_problem.check_raw("y")
    assert not orig_problem.check_raw("x^2")

def test_swiss_selection_2024_5():
    from math_construct.problems.swiss.problem_2024_5_selection import ProblemSwissSelection20245
    orig_problem = ProblemSwissSelection20245.get_original()
    orig_sol = orig_problem.config.original_solution
    assert orig_problem.check_raw(orig_sol)
    assert not orig_problem.check_raw(orig_sol[:-1])
    assert not orig_problem.check_raw([orig_sol[1], orig_sol[0]])

    for problem in ProblemSwissSelection20245.generate_multiple(10):
        assert problem.check_raw(problem.get_solution())

def test_swiss_selection_2022_1():
    from math_construct.problems.swiss.problem_2022_1_selection import ProblemSwissSelection20221
    orig_problem = ProblemSwissSelection20221.get_original()
    orig_sol = orig_problem.config.original_solution
    assert orig_problem.check_raw(orig_sol)
    assert not orig_problem.check_raw([1, 0, 0])
    assert not orig_problem.check_raw([1, 0, 1])
    for n in range(2, 30):
        problem = ProblemSwissSelection20221(n)
        sol = problem.get_solution()
        assert problem.check_raw(sol)

def test_swiss_selection_2022_12():
    from math_construct.problems.backups.problem_2022_12_selection import ProblemSwissSelection202212
    orig_problem = ProblemSwissSelection202212.get_original()
    orig_sol = orig_problem.config.original_solution
    assert orig_problem.check_raw(orig_sol)
    assert not orig_problem.check_raw("x")
    assert not orig_problem.check_raw(r"\frac{1}{y}")
    assert not orig_problem.check_raw("x^2")

def test_swiss_2023_5():
    from math_construct.problems.swiss.problem_2023_5 import ProblemSwiss20235
    orig_problem = ProblemSwiss20235.get_original()
    orig_sol = orig_problem.config.original_solution
    assert orig_problem.check_raw(orig_sol)
    assert not orig_problem.check_raw("x")
    assert not orig_problem.check_raw("y")
    assert not orig_problem.check_raw("x^2")

def test_swiss_selection_2020_1():
    from math_construct.problems.swiss.problem_2020_1_selection import ProblemSwissSelection20201
    orig_problem = ProblemSwissSelection20201.get_original()
    orig_sol = orig_problem.config.original_solution
    orig_sol = [list(el) for el in orig_sol]
    assert orig_problem.check_raw(orig_sol)
    assert not orig_problem.check_raw(orig_sol[:-1])
    orig_sol[0][0] += 1
    assert not orig_problem.check_raw(orig_sol)
    orig_sol[0][0] += 1
    assert not orig_problem.check_raw(orig_sol)

    new_problem = ProblemSwissSelection20201(2)
    sol = [
        [0, 1],
        [1, 0]
    ]
    assert new_problem.check_raw(sol)

    for problem in ProblemSwissSelection20201.generate_multiple(10):
        assert problem.check_raw(problem.get_solution())

def test_swiss_2019_3():
    from math_construct.problems.swiss.problem_2019_3 import ProblemSwiss20193
    orig_problem = ProblemSwiss20193.get_original()
    orig_sol = orig_problem.config.original_solution
    assert orig_problem.check_raw(orig_sol)
    assert not orig_problem.check_raw(orig_sol[:-1])
    orig_sol[0][0] += 1
    assert not orig_problem.check_raw(orig_sol)

    for problem in [ProblemSwiss20193.generate() for _ in range(50)]:
        assert problem.check_raw(problem.get_solution())

def test_swiss_selection_2018_8():
    from math_construct.problems.swiss.problem_2018_8_selection import ProblemSwissSelection20188
    orig_problem = ProblemSwissSelection20188.get_original()
    orig_sol = orig_problem.config.original_solution
    assert orig_problem.check_raw(orig_sol)

    for problem in [ProblemSwissSelection20188.generate() for _ in range(50)]:
        assert problem.check_raw(problem.get_solution())

def test_konhauser_2023_3():
    from math_construct.problems.konhauser.problem_2023_3 import ProblemKonhauser20233
    orig_problem = ProblemKonhauser20233.get_original()
    orig_sol = orig_problem.config.original_solution
    assert orig_problem.check_raw(orig_sol)
    assert not orig_problem.check_raw(orig_sol[:-1])
    assert not orig_problem.check_raw(orig_sol[:-1] + [orig_sol[0]])
    orig_sol[0][0] += 1
    assert not orig_problem.check_raw(orig_sol)

    new_problem = ProblemKonhauser20233(5, 1)
    assert new_problem.check_raw([[1, 1, 0, 1]])
    assert not new_problem.check_raw([[1, 1, 0, 0]])
    assert not new_problem.check_raw([[1, 1, 1]])
    assert new_problem.check_raw([[1, 1, 0, 0, 0]])

    for problem in ProblemKonhauser20233.generate_multiple(10):
        assert problem.check_raw(problem.get_solution())

def test_konhauser_2021_6():
    from math_construct.problems.backups.problem_2021_6 import ProblemKonhauser20216
    orig_problem = ProblemKonhauser20216.get_original()
    orig_sol = orig_problem.config.original_solution
    assert orig_problem.check_raw(orig_sol)
    assert not orig_problem.check_raw(r"\frac{20}{3} x^{2} - 20x")
    assert not orig_problem.check_raw(r"\frac{20}{3} x^{3} - 21x")
    assert not orig_problem.check_raw(r"\frac{x}{\sin(x)}")

    new_problem = ProblemKonhauser20216(3, 3, 2)
    assert new_problem.check_raw(r"\frac{3}{3} x^{2} - 3x")
    
    for new_problem in ProblemKonhauser20216.generate_multiple(10):
        print(new_problem.get_solution(), new_problem.m)
        assert new_problem.check_raw(new_problem.get_solution())

def test_konhauser_2021_10():
    from math_construct.problems.konhauser.problem_2021_10 import ProblemKonhauser202110
    orig_problem = ProblemKonhauser202110.get_original()
    orig_sol = orig_problem.config.original_solution
    assert orig_problem.check_raw(orig_sol)

    new_problem = ProblemKonhauser202110(3, 2, 1)
    assert new_problem.check_raw([136])
    assert not new_problem.check_raw([128])
    assert not new_problem.check_raw([72])
    assert not new_problem.check_raw([1032])

    new_problem = ProblemKonhauser202110(3, 2, 2)
    assert not new_problem.check_raw([136, 136])
    assert new_problem.check_raw([136, 160])

    for problem in ProblemKonhauser202110.generate_multiple(10):
        assert problem.check_raw(problem.get_solution())

def test_konhauser_2020_9():
    from math_construct.problems.konhauser.problem_2020_9 import ProblemKonhauser20209
    orig_problem = ProblemKonhauser20209.get_original()
    orig_sol = orig_problem.config.original_solution
    assert orig_problem.check_raw(orig_sol)
    assert not orig_problem.check_raw(orig_sol[:-1])
    assert not orig_problem.check_raw(orig_sol[1:] + [orig_sol[0]])
    for i in range(len(orig_sol)):
        orig_sol[i] += 1
        assert not orig_problem.check_raw(orig_sol)
        orig_sol[i] -= 1
    
    for problem in ProblemKonhauser20209.generate_multiple(10):
        assert problem.check_raw(problem.get_solution())

def test_konhauser_2019_1():
    from math_construct.problems.konhauser.problem_2019_1 import ProblemKonhauser20191
    orig_problem = ProblemKonhauser20191.get_original()
    orig_sol = orig_problem.config.original_solution
    assert orig_problem.check_raw(orig_sol)
    assert not orig_problem.check_raw(orig_sol[:-1])
    assert not orig_problem.check_raw(orig_sol[1:] + [orig_sol[0]])
    orig_sol[0][0] += 1
    assert not orig_problem.check_raw(orig_sol)
    orig_sol[0][0] -= 1
    orig_sol[1][0] += 1
    assert not orig_problem.check_raw(orig_sol)
    orig_sol[1][0] += 1
    assert not orig_problem.check_raw(orig_sol)

    new_problem = ProblemKonhauser20191("2,1,3,4,5,6,7,9,8,10,11,13,12")
    sol = [
        [2,3,6,7],
        [1,3,4,5],
        [2,1,8,9],
        [2,5,10,11],
        [2,4,12,13],
        [1,7,11,12],
        [1,6,10,13],
        [3,9,11,13],
        [3,8,10,12],
        [4,7,9,10],
        [4,6,8,11],
        [5,6,9,12],
        [5,7,8,13],
        
    ]
    assert new_problem.check_raw(sol)

    for problem in ProblemKonhauser20191.generate_multiple(10):
        assert problem.check_raw(problem.get_solution())

def test_konhauser_2017_2():
    from math_construct.problems.backups.problem_2017_2 import ProblemKonhauser20172
    orig_problem = ProblemKonhauser20172.get_original()
    orig_sol = orig_problem.config.original_solution
    assert orig_problem.check_raw(orig_sol)
    assert not orig_problem.check_raw(orig_sol[:-1])
    assert orig_problem.check_raw(orig_sol[1:] + [orig_sol[0]])
    orig_sol[0][0] += 1
    assert not orig_problem.check_raw(orig_sol)
    orig_sol[0][0] -= 2
    assert not orig_problem.check_raw(orig_sol)
    orig_sol[0][0] += 1
    orig_sol[1][3] += 1
    assert not orig_problem.check_raw(orig_sol)

    for problem in ProblemKonhauser20172.generate_multiple(10):
        assert problem.check_raw(problem.get_solution())

    new_problem = ProblemKonhauser20172(3)
    sol = [
        [1, 1, 1],
        [1, 1, 0],
        [1, 0, 1],
    ]
    assert new_problem.check_raw(sol)

def test_konhauser_2016_1():
    from math_construct.problems.konhauser.problem_2016_1 import ProblemKonhauser20161
    orig_problem = ProblemKonhauser20161.get_original()
    orig_sol = orig_problem.config.original_solution
    assert orig_problem.check_raw(orig_sol)
    new_problem = ProblemKonhauser20161(r"\frac{31}{32}", 6)
    assert new_problem.check_raw(orig_sol)
    orig_sol[0][0] -= 0.01
    assert not new_problem.check_raw(orig_sol)
    orig_sol[0][0] += 0.01
    orig_sol[1][1][0] += 0.01
    assert not new_problem.check_raw(orig_sol)
    orig_sol[1][1][0] -= 0.01
    orig_sol[1][2].append(0)
    assert not new_problem.check_raw(orig_sol)
    orig_sol[1][2].pop()
    orig_sol[1][2].append(1)
    assert not new_problem.check_raw(orig_sol)
    orig_sol[1][2].pop()
    new_problem = ProblemKonhauser20161(r"\frac{30}{32}", 6)
    assert not new_problem.check_raw(orig_sol)

    for problem in ProblemKonhauser20161.generate_multiple(10):
        assert problem.check_raw(problem.get_solution())

def test_konhauser_2016_3():
    from math_construct.problems.konhauser.problem_2016_3 import ProblemKonhauser20163
    orig_problem = ProblemKonhauser20163.get_original()
    orig_sol = orig_problem.config.original_solution
    assert orig_problem.check_raw(orig_sol)
    assert not orig_problem.check_raw(orig_sol[:-1])
    assert not orig_problem.check_raw([orig_sol[0][:-1], orig_sol[1]])
    orig_sol[0][0][0] += 10
    assert not orig_problem.check_raw(orig_sol)
    orig_sol[0][0][0] -= 9
    assert not orig_problem.check_raw(orig_sol)
    orig_sol[0][0][0] -= 1
    orig_sol[1][0] -= 3
    assert not orig_problem.check_raw(orig_sol)

    for problem in ProblemKonhauser20163.generate_multiple(10):
        assert problem.check_raw(problem.get_solution())

    new_problem = ProblemKonhauser20163(3, 5)
    sol = [
        [
            [3, 2, 7],
            [2, 6, 4],
            [5, 1, 2],
            [4, 3, 1],
            [1, 4, 3],
        ], [7, 5, 6]
    ]
    assert new_problem.check_raw(sol)

def test_konhauser_2016_6():
    from math_construct.problems.backups.problem_2016_6 import ProblemKonhauser20166
    orig_problem = ProblemKonhauser20166.get_original()
    orig_sol = orig_problem.config.original_solution
    assert orig_problem.check_raw(orig_sol)
    orig_sol += [41]
    assert not orig_problem.check_raw(orig_sol)
    orig_sol.pop()
    orig_sol[-1] += 1
    assert not orig_problem.check_raw(orig_sol)
    orig_sol[-1] -= 1
    orig_sol = [3.14 * el for el in orig_sol]
    assert orig_problem.check_raw(orig_sol)

    for problem in ProblemKonhauser20166.generate_multiple(10):
        assert problem.check_raw(problem.get_solution())

def test_konhauser_2015_2():
    from math_construct.problems.konhauser.problem_2015_2 import ProblemKonhauser20152
    orig_problem = ProblemKonhauser20152.get_original()
    orig_sol = orig_problem.config.original_solution
    assert orig_problem.check_raw(orig_sol)
    assert not orig_problem.check_raw(orig_sol[:-1])
    assert not orig_problem.check_raw(orig_sol[1:] + [orig_sol[1]])
    orig_sol[0] += 1
    assert not orig_problem.check_raw(orig_sol)

    for problem in ProblemKonhauser20152.generate_multiple(10):
        assert problem.check_raw(problem.get_solution())

    new_problem = ProblemKonhauser20152(3, 6, 4.5, 4)
    sol = [
        (12 + 128 ** 0.5) / 2, (12 - 128 ** 0.5) / 2
    ]
    assert new_problem.check_raw(sol)

def test_konhauser_2014_7():
    from math_construct.problems.konhauser.problem_2014_7 import ProblemKonhauser20147
    orig_problem = ProblemKonhauser20147.get_original()
    orig_sol = orig_problem.config.original_solution
    assert orig_problem.check_raw(orig_sol)
    assert not orig_problem.check_raw(orig_sol[:-1])
    orig_sol[0] += 0.01
    assert not orig_problem.check_raw(orig_sol)

    for _ in range(20):
        new_problem = ProblemKonhauser20147.generate()
        sol = new_problem.get_solution()
        assert new_problem.check_raw(sol)
        sol[0] += 1
        assert not new_problem.check_raw(sol)
        sol[0] -= 1
        sol[1] += 0.05
        assert not new_problem.check_raw(sol)

def test_konhauser_2013_1():
    from math_construct.problems.konhauser.problem_2013_1 import ProblemKonhauser20131
    import copy
    orig_problem = ProblemKonhauser20131.get_original()
    orig_sol = orig_problem.config.original_solution
    assert orig_problem.check_raw(orig_sol)
    assert not orig_problem.check_raw(orig_sol[:-1])
    orig_sol_copy = copy.deepcopy(orig_sol)
    orig_sol_copy[0][0] += 1
    assert not orig_problem.check_raw(orig_sol_copy)
    
    orig_sol_copy[0] = (3, 0)
    assert not orig_problem.check_raw(orig_sol_copy)

    for problem in ProblemKonhauser20131.generate_multiple(100):
        assert problem.check_raw(problem.get_solution())

    new_problem = ProblemKonhauser20131(8, 6)
    orig_sol = ProblemKonhauser20131.config.original_solution
    orig_sol = [[2 * el[0], 2 * el[1]] for el in orig_sol]
    assert new_problem.check_raw(orig_sol)

def test_problem_imoshortlist_2003n2():
    from math_construct.problems.imo_shortlist.problem_2003_n2 import Problem2003N2, get_solution 
    orig_problem = Problem2003N2.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    for i in range(5):
        assert Problem2003N2(i).check_raw(get_solution(i))
    assert get_solution(6) == [3,2,1,21,221,2221]
    assert Problem2003N2(3).check_raw([2222221, 1, 3])
    assert not Problem2003N2(3).check_raw([1, 3, 1])
    assert not Problem2003N2(3).check_raw([1, 2, 3, 21])

def test_problem_imoshortlist_2003n3():
    from math_construct.problems.imo_shortlist.problem_2003_n3 import Problem2003N3, get_solution 
    orig_problem = Problem2003N3.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    for i in range(5):
        assert Problem2003N3(i).check_raw(get_solution(i))
    assert Problem2003N3(1).check_raw([[7, 2]])
    assert Problem2003N3(1).check_raw([[52479, 18]])
    assert not Problem2003N3(1).check_raw([[2, 1]])
    assert not Problem2003N3(1).check_raw([[5, 10]])

def test_problem_imoshortlist_2005c8():
    from math_construct.problems.imo_shortlist.problem_2005_c8 import Problem2005C8, get_solution 
    orig_problem = Problem2005C8.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    for i in range(5, 15):
        assert Problem2005C8(i).check_raw(get_solution(i))
    small_problem = Problem2005C8(5)
    assert small_problem.check_raw([[[2, 4], [2, 5]], [[1, 3], [3, 5]]])
    assert small_problem.check_raw([[[5, 3], [3, 1]], [[5, 2], [2, 4]]])
    assert not small_problem.check_raw([[[5, 3], [3, 1]], [[5, 2], [2, 4]], [1,2,3]])
    assert not small_problem.check_raw([[[5, 3], [3, 1], [1, 2]], [[5, 2], [2, 4]]])
    assert not small_problem.check_raw([[[5, 3], [3, 1, 2]], [[5, 2], [2, 4]]])
    assert not small_problem.check_raw([[[5, 3], [3, 3]], [[5, 2], [2, 4]]])
    assert not small_problem.check_raw([[[5, 1], [5, 3]], [[5, 2], [2, 4]]])
    assert not small_problem.check_raw([[[1, 5], [5, 3]], [[5, 2], [2, 4]]])
    assert not small_problem.check_raw([[[5, 3], [2, 4]], [[5, 2], [2, 4]]])

    # valid but suboptimal arrangement 
    assert not Problem2005C8(6).check_raw([[[1, 3], [1, 4], [1, 5]], [[2, 4], [2, 5], [2, 6]]])

def test_problem_imoshortlist_2006c5():
    from math_construct.problems.imo_shortlist.problem_2006_c5 import Problem2006C5, get_solution
    orig_problem = Problem2006C5.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    for n, k in Problem2006C5.pairs:
        assert Problem2006C5(n, k).check_raw(get_solution(n, k))
    assert Problem2006C5(4,3).check_raw([[3,4,1,2], [4,3,2,1], [2,1,4,3]])
    assert Problem2006C5(8,2).check_raw([[3,4,1,2,7,8,5,6], [2,1,4,3,6,5,8,7]])
    assert not Problem2006C5(8,2).check_raw([[2,1,4,3,6,5,8,7]])
    assert not Problem2006C5(8,2).check_raw([[3,4,1,2,7,8], [2,1,4,3,6,5,8,7]])
    assert not Problem2006C5(8,2).check_raw([[3,4,1,2,7,9,5,6], [2,1,4,3,6,5,8,7]])
    assert not Problem2006C5(8,2).check_raw([[3,4,1,2,7,7,5,6], [2,1,4,3,6,5,8,7]])
    assert not Problem2006C5(8,2).check_raw([[1,4,3,2,7,8,5,6], [2,1,4,3,6,5,8,7]])
    assert not Problem2006C5(8,2).check_raw([[4,4,1,2,7,8,5,6], [2,1,4,3,6,5,8,7]])
    assert not Problem2006C5(8,2).check_raw([[2,1,4,3,6,5,8,7], [2,1,4,3,6,5,8,7]])
    assert not Problem2006C5(8,2).check_raw([[2,1,4,3,6,5,8,7], [4,5,7,1,2,8,3,6]]) # cycle broken

def test_problem_imoshortlist_2008a2():
    from math_construct.problems.imo_shortlist.problem_2008_a2 import Problem2008A2, get_solution
    orig_problem = Problem2008A2.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    assert Problem2008A2(30).check_raw(get_solution(30))
    assert not Problem2008A2(2).check_raw(get_solution(1))
    assert not Problem2008A2(1).check_raw(get_solution(2))
    sol = get_solution(3)
    assert Problem2008A2(3).check_raw(sol)
    sol[-1][2], sol[-1][1] = sol[-1][1], sol[-1][2]
    assert Problem2008A2(3).check_raw(sol)
    sol[0][0], sol[1][0] = sol[1][0], sol[0][0]
    assert not Problem2008A2(3).check_raw(sol)

def test_problem_imoshortlist_2009c2():
    from math_construct.problems.imo_shortlist.problem_2009_c2 import Problem2009C2, get_solution
    orig_problem = Problem2009C2.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    for n in range(4, 10):
        N = int(2*n/3)+1
        assert Problem2009C2(n, N).check_raw(get_solution(n, N))
    expected = {
        5: [[0, 3, 2], [1, 4, 0], [2, 0, 3], [3, 1, 1]],
        6: [[0, 2, 4], [1, 3, 2], [2, 4, 0], [3, 0, 3], [4, 1, 1]],
        7: [[0, 2, 5], [1, 3, 3], [2, 4, 1], [3, 0, 4], [4, 1, 2]]
    }
    for n, exp in expected.items():
        N = int(2*n/3)+1
        sol = get_solution(n, N)
        assert len(exp) == len(sol)
        for e, s in zip(exp, sol):
            assert len(e) == len(s) 
            assert all(x == y for x, y in zip(e, s))
    
    assert Problem2009C2(5, 4).check_raw([[0, 3, 2], [3, 1, 1], [1, 4, 0], [2, 0, 3]])
    assert not Problem2009C2(5, 4).check_raw([[0, 3, 2], [1, 4, 0], [2, 0, 3]])

def test_problem_imoshortlist_2010n1():
    from math_construct.problems.imo_shortlist.problem_2010_n1 import Problem2010N1, get_solution
    orig_problem = Problem2010N1.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    for k in [42, 51]:
        sol = get_solution(k)
        assert Problem2010N1(k).check_raw(sol)
        sol[-5] -= 1 
        assert not Problem2010N1(k).check_raw(sol)

def test_problem_imoshortlist_2011a1():
    from math_construct.problems.imo_shortlist.problem_2011_a1 import Problem2011A1, get_solution
    orig_problem = Problem2011A1.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    for n in range(1, 11):
        sol = get_solution(n)
        assert Problem2011A1(n).check_raw(sol)
    assert Problem2011A1(1).check_raw([[1, 5, 7, 11]])
    assert Problem2011A1(1).check_raw([[1, 11, 29, 19]])
    assert not Problem2011A1(1).check_raw([[10, 110, 290, 190]]) # bound
    assert not Problem2011A1(2).check_raw([[1, 11, 29, 19]])
    assert not Problem2011A1(1).check_raw([[1, 11, 29, 19, 50]])
    assert not Problem2011A1(1).check_raw([[1, 2, 3, 4]])

def test_problem_imoshortlist_2012c2(): 
    from math_construct.problems.imo_shortlist.problem_2012_c2 import Problem2012C2, get_solution
    orig_problem = Problem2012C2.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    for n in range(6, 11):
        m = int((2*n-1)/5)
        sol = get_solution(n, m)
        assert Problem2012C2(n, m).check_raw(sol)
    assert Problem2012C2(6,2).check_raw([[3, 2], [5, 1]])
    assert Problem2012C2(6,2).check_raw([[1, 5], [2, 3]])

    assert not Problem2012C2(6,2).check_raw([[1, 5]])
    assert not Problem2012C2(6,2).check_raw([[1, 5, 3], [2, 3]])
    assert not Problem2012C2(6,2).check_raw([[1, 7], [2, 3]])
    assert not Problem2012C2(6,2).check_raw([[1, 5], [0, 6]])
    assert not Problem2012C2(6,2).check_raw([[1, 6], [2, 4]])
    assert not Problem2012C2(6,2).check_raw([[1, 5], [1, 3]])
    assert not Problem2012C2(6,2).check_raw([[1, 5], [2, 4]])
    
def test_problem_imoshortlist_2014_c3(): 
    from math_construct.problems.imo_shortlist.problem_2014_c3 import Problem2014C3, get_solution
    orig_problem = Problem2014C3.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    for n in range(5, 17):
        sol = get_solution(n, 4)
        assert Problem2014C3(n, 4).check_raw(sol)
    assert not orig_problem.check_raw([[3, 2], [5, 1]])

def test_problem_imoshortlist_2014_n2():
    from math_construct.problems.imo_shortlist.problem_2014_n2 import Problem2014N2, get_solution
    orig_problem = Problem2014N2.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    for n in [1, 40]:
        sol = get_solution(n)
        assert Problem2014N2(n).check_raw(sol)
    assert Problem2014N2(1).check_raw([[7, 13]])
    assert Problem2014N2(1).check_raw([[65519, 67159]])
    assert not Problem2014N2(1).check_raw([[13, 7]])
    assert not Problem2014N2(2).check_raw([[7, 13]])
    assert not Problem2014N2(1).check_raw([[7, 13, 14]])
    assert not Problem2014N2(1).check_raw([[-6, 13]])
    assert not Problem2014N2(1).check_raw([[6, 13]])
    assert not Problem2014N2(1).check_raw([[7, 14]])


def test_problem_imoshortlist_2018_c1():
    from math_construct.problems.imo_shortlist.problem_2018_c1 import Problem_IMOShortlist2018C1, get_solution
    orig_problem = Problem_IMOShortlist2018C1.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    for n in range(3, 13):
        assert Problem_IMOShortlist2018C1(n).check_raw(get_solution(n))

def test_problem_imc_2022_6():
    from math_construct.problems.backups.imc_problem_2022_6 import Problem_IMC_2022_6, get_solution
    orig_problem = Problem_IMC_2022_6.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    assert not orig_problem.check_raw([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    assert Problem_IMC_2022_6(17).check_raw(get_solution(17))
    assert Problem_IMC_2022_6(23).check_raw(get_solution(23))
    new_problem = Problem_IMC_2022_6.generate()

def test_problem_imc_2019_9():
    from math_construct.problems.imc.problem_2019_9 import Problem_IMC_2019_9, get_solution
    orig_problem = Problem_IMC_2019_9.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    assert not Problem_IMC_2019_9(2).check_raw([[1,0],[0,1], [1,0],[0,-1]])
    assert Problem_IMC_2019_9(6).check_raw(get_solution(6))

def test_problem_imc_2018_6():
    from math_construct.problems.imc.problem_2018_6 import Problem_IMC_2018_6, get_solution
    orig_problem = Problem_IMC_2018_6.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    assert Problem_IMC_2018_6(3, 2).check_raw(get_solution(3, 2))
    assert not Problem_IMC_2018_6(3, 2).check_raw([[1, 0], [1, 0], [1, 0]])
    assert not Problem_IMC_2018_6(2, 4).check_raw([[1, 0, -1, -1], [0, 1, 1, 1]])
    for k in range(8, 21):
        for n in range((k+1)//2, (k+1)//2+5):
            assert Problem_IMC_2018_6(n, k).check_raw(get_solution(n, k))

def test_problem_imc_2013_3():
    from math_construct.problems.imc.problem_2013_3 import Problem_IMC_2013_3, get_solution
    orig_problem = Problem_IMC_2013_3.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    assert not Problem_IMC_2013_3(2).check_raw([[1, 1, 0, 0], [1, 1, 0, 0], [1, 1, 0, 0], [1, 1, 0, 0], [1, 1, 0, 0], [1, 1, 0, 0]])
    for n in range(4, 25):
        sol = get_solution(n)
        assert Problem_IMC_2013_3(n).check_raw(sol)

def test_problem_imc_2012_2():
    from math_construct.problems.imc.problem_2012_2 import Problem_IMC_2012_2, get_solution
    orig_problem = Problem_IMC_2012_2.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    assert not Problem_IMC_2012_2(3).check_raw([[0, 1, 1], [0, 2, 2], [0, 3, 3]])
    for n in range(3, 15):
        sol = get_solution(n)
        assert Problem_IMC_2012_2(n).check_raw(sol)

def test_problem_usamo_2017_1():
    from math_construct.problems.usamo.problem_2017_1 import Problem_USAMO_2017_1, get_solution
    orig_problem = Problem_USAMO_2017_1.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    assert not Problem_USAMO_2017_1(1).check_raw([[2, 3]])
    assert Problem_USAMO_2017_1(17).check_raw(get_solution(17))
    #for k in range

def test_problem_putnam_2023_b2():
    from math_construct.problems.putnam.problem_2023_b2 import Problem_Putnam2023B2, get_solution
    orig_problem = Problem_Putnam2023B2.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    assert not Problem_Putnam2023B2(1).check_raw([100])
    for m in range(3, 26):
        assert Problem_Putnam2023B2(m).check_raw(get_solution(m))

def test_problem_putnam_2022_b4():
    from math_construct.problems.putnam.problem_2022_b4 import Problem_Putnam2022B4, get_solution
    orig_problem = Problem_Putnam2022B4.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    assert not Problem_Putnam2022B4(6).check_raw([1, 2, 3, 4, 5, 6])
    for n in range(9, 26):
        if n%3 == 0:
            assert Problem_Putnam2022B4(n).check_raw(get_solution(n))

def test_problem_bmosl_2008_n1():
    from math_construct.problems.bmo_shortlist.problem_2008_n1 import ProblemBMO2008N1, get_solution
    orig_problem = ProblemBMO2008N1.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    for i in range(1, 60):
        assert ProblemBMO2008N1(i).check_raw(get_solution(i))

def test_problem_bmosl_2018_n5():
    from math_construct.problems.backups.problem_2008_n5 import ProblemBMO2008N5, get_solution
    orig_problem = ProblemBMO2008N5.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    for m in range(10, 60):
        for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293]:
            assert ProblemBMO2008N5(m, p).check_raw(get_solution(m, p))

def test_problem_bmosl_2014_n4():
    from math_construct.problems.backups.problem_2014_n4 import ProblemBMO2014N4, get_solution
    orig_problem = ProblemBMO2014N4.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    for k in range(15, 100):
        assert ProblemBMO2014N4(k).check_raw(get_solution(k))

def test_problem_bmosl_2015_n2():
    from math_construct.problems.backups.problem_2015_n2 import ProblemBMO2015N2, get_solution
    orig_problem = ProblemBMO2015N2.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    for k in range(10, 100):
        assert ProblemBMO2015N2(k).check_raw(get_solution(k))

def test_problem_bmosl_2015_n7():
    from math_construct.problems.bmo_shortlist.problem_2015_n7 import ProblemBMO2015N7, get_solution
    orig_problem = ProblemBMO2015N7.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    for k in range(1, 20):
        assert ProblemBMO2015N7(k).check_raw(get_solution(k))

def test_problem_bmosl_2016_n3():
    from math_construct.problems.backups.problem_2016_n3 import ProblemBMO2016N3, get_solution
    orig_problem = ProblemBMO2016N3.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    for k in range(5, 25):
        assert ProblemBMO2016N3(k).check_raw(get_solution(k))

def test_problem_bmosl_2019_c1():
    from math_construct.problems.bmo_shortlist.problem_2019_c1 import ProblemBMO2019C1, get_solution
    orig_problem = ProblemBMO2019C1.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    assert not orig_problem.check_raw([i//2+1 for i in range(200)])
    for k in range(5, 100):
        assert ProblemBMO2019C1(k).check_raw(get_solution(k))

def test_problem_jbmosl_2022_n6():
    from math_construct.problems.backups.problem_2022_n6 import ProblemJBMO2022N6, get_solution
    orig_problem = ProblemJBMO2022N6.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    for k in range(1, 101):
        if k not in [1, 2, 4, 7]:
            print('n6 k', k, ProblemJBMO2022N6(k).check(get_solution(k)))
            assert ProblemJBMO2022N6(k).check_raw(get_solution(k))

def test_problem_jbmosl_2023_c1():
    from math_construct.problems.jbmo_shortlist.problem_2023_c1 import ProblemJBMO2023C1, get_solution
    orig_problem = ProblemJBMO2023C1.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    for k in range(3, 500, 62):
        assert ProblemJBMO2023C1(2*k-1, k).check_raw(get_solution(k))

def test_problem_jbmosl_2023_n3():
    from math_construct.problems.jbmo_shortlist.problem_2023_n3 import ProblemJBMO2023N5
    orig_problem = ProblemJBMO2023N5.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)


def test_problem_jbmosl_2021_C5():
    from math_construct.problems.jbmo_shortlist.problem_2021_c5 import ProblemJBMO2021C5, get_solution
    orig_problem = ProblemJBMO2021C5.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    for N in range(10, 100, 11):
        assert ProblemJBMO2021C5(N, 10, 8).check_raw(get_solution(N, 10, 8))
    for a in range(3, 15):
        assert ProblemJBMO2021C5(100, a, 8).check_raw(get_solution(100, a, 8))
    for b in range(3, 15):
        assert ProblemJBMO2021C5(100, 10, b).check_raw(get_solution(100, 10, b))

def test_problem_jbmosl_2019_C4():
    from math_construct.problems.jbmo_shortlist.problem_2019_c4 import ProblemJBMO2019C4, get_solution
    orig_problem = ProblemJBMO2019C4.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    for N in range(10, 100, 11):
        assert ProblemJBMO2019C4(N).check_raw(get_solution(N))
    wrong_example = [['b', 'b', 'b', 'b', 'b', 'b', 'b'],
                     ['b', 'w', 'w', 'w', 'w', 'w', 'b'],
                     ['b', 'w', 'b', 'b', 'b', 'b', 'b'],
                     ['b', 'w', 'w', 'w', 'w', 'w', 'b'],
                     ['b', 'b', 'b', 'b', 'b', 'b', 'b']]
    assert not ProblemJBMO2019C4(7).check_raw(wrong_example)
    incomplete_example = [['b', 'b', 'b', 'b', 'b', 'b', 'b'],
                     ['b', 'w', 'w', 'w', 'w', 'w', 'b'],
                     ['b', 'w', 'b', 'w', 'b', 'w', 'b'],
                     ['b', 'w', 'w', 'w', 'w', 'w', 'b'],
                     ['b', 'b', 'b', 'b', 'b', 'b', 'b']]
    assert not ProblemJBMO2019C4(7).check_raw(incomplete_example)


def test_problem_hmo_2023_5():
    from math_construct.problems.croatian.problem_2023_5 import Problem_HMO_2023_5, get_solution
    orig_problem = Problem_HMO_2023_5.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)

    problem1 = Problem_HMO_2023_5(5, 5, 10)
    assert problem1.check_raw(problem1.get_solution())
    assert not problem1.check_raw([[0] * 10] * 10)
    problem2 = Problem_HMO_2023_5(5, 7, 20)
    assert problem2.check_raw(problem2.get_solution())
    

def test_problem_hmo_2022_1():
    from math_construct.problems.croatian.problem_2022_1 import Problem_HMO_2022_1, get_solution
    orig_problem = Problem_HMO_2022_1.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    assert not orig_problem.check_raw(list(range(20)))
    for n in range(16, 40, 2):
        assert Problem_HMO_2022_1(n).check_raw(Problem_HMO_2022_1(n).get_solution())


def test_problem_jbmosl_2018_P3():
    from math_construct.problems.jbmo_shortlist.problem_2018_p3 import ProblemJBMO2018A3, get_solution
    orig_problem = ProblemJBMO2018A3.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    for N in range(12, 500, 27):
        assert ProblemJBMO2018A3(N).check_raw(get_solution(N))

def test_problem_jbmosl_2018_N4():
    from math_construct.problems.jbmo_shortlist.problem_2018_n4 import ProblemJBMO2018N4, get_solution
    orig_problem = ProblemJBMO2018N4.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    for N in range(2, 8):
        assert ProblemJBMO2018N4(N).check_raw(get_solution(N))

def test_problem_jbmosl_2006_p14():
    from math_construct.problems.backups.problem_2006_14 import ProblemJBMO2006P14, get_solution
    orig_problem = ProblemJBMO2006P14.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    for N in range(1000, 4000, 11):
        assert ProblemJBMO2006P14(N).check_raw(get_solution(N))
    assert not ProblemJBMO2006P14(13).check_raw([0, 1, 2])
    assert not ProblemJBMO2006P14(13).check_raw([1, 1, 6, 12])
    assert not ProblemJBMO2006P14(13).check_raw([1, 5, 6, 12])
    assert ProblemJBMO2006P14(13).check_raw([1, 6, 12])

def test_problem_hmo_2020_4():
    from math_construct.problems.croatian.problem_2020_4 import Problem_HMO_2020_4, get_solution
    orig_problem = Problem_HMO_2020_4.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    for n in range(1, 26):
        assert Problem_HMO_2020_4(n).check_raw(get_solution(n))

def test_problem_imo_2017_n3():
    from math_construct.problems.imo_shortlist.problem_2017_n3 import Problem2017N3, get_solution
    orig_problem = Problem2017N3.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    for a in range(2, 10):
        for b in range(2, 10):
            assert Problem2017N3(a * b).check_raw(get_solution(a * b))

def test_problem_imo_2017_n6():
    from math_construct.problems.imo_shortlist.problem_2017_n6 import Problem2017N6, get_solution
    orig_problem = Problem2017N6.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    for n in range(5, 25):
        sol = get_solution(n)
        assert Problem2017N6(n).check_raw(sol)
        
def test_problem_jbmosl_2016_c2():
    from math_construct.problems.jbmo_shortlist.problem_2016_c2 import ProblemJBMO2016C2
    orig_problem = ProblemJBMO2016C2.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    assert not orig_problem.check_raw([i for i in range(1, 26)])

def test_problem_jbmosl_2008_c1():
    from math_construct.problems.jbmo_shortlist.problem_2008_c1 import ProblemJBMO2008C1, get_solution
    orig_problem = ProblemJBMO2008C1.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    assert orig_problem.check_raw([[[1, 1], [1, 2], [1, 3], [1, 4], [2, 1], [2, 2], [2, 3], [2, 4], [3, 1], [3, 2], [3, 3], [3, 4], [4, 1], [4, 2], [4, 3], [4, 4], [5, 1], [5, 2], [5, 3], [5, 4]], [[5, 4, 5, 5], [4, 4, 4, 5], [3, 4, 3, 5], [2, 4, 2, 5], [1, 4, 1, 5], [5, 3, 5, 4], [4, 3, 4, 4], [3, 3, 3, 4], [2, 3, 2, 4], [1, 3, 1, 4], [5, 2, 5, 3], [4, 2, 4, 3], [3, 2, 3, 3], [2, 2, 2, 3], [1, 2, 1, 3], [5, 1, 5, 2], [4, 1, 4, 2], [3, 1, 3, 2], [2, 1, 2, 2], [1, 1, 1, 2]]])
    for N in range(10, 90, 7):
        assert ProblemJBMO2008C1(N).check_raw(get_solution(N))

def test_problem_baltic_2005_19():
    from math_construct.problems.misc.problem_balticway_2005_19 import ProblemBaltic2005P19, get_solution
    orig_problem = ProblemBaltic2005P19.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    for N in range(10, 15):
        for M in range(10, 15):
            assert ProblemBaltic2005P19(N, M).check_raw(get_solution(N, M))

def test_problem_bul_p1():
    from math_construct.problems.bulgarian.problem_pms_2008_8_3 import ProblemBulPMS2008P8_3, get_solution
    orig_problem = ProblemBulPMS2008P8_3.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    for N in range(3, 10):
        assert ProblemBulPMS2008P8_3(N).check_raw(get_solution(N))

def test_problem_bul_p2():
    from math_construct.problems.bulgarian.problem_pms_2021_10_3 import ProblemBulPMS2021P10_3, get_solution
    orig_problem = ProblemBulPMS2021P10_3.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    for N in range(5, 20):
        assert ProblemBulPMS2021P10_3(2*N+1).check_raw(get_solution(2*N+1))

def test_problem_imo_2016_a5():
    from math_construct.problems.imo_shortlist.problem_2016_a5 import Problem2016A5, get_solution
    orig_problem = Problem2016A5.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    # assert not orig_problem.check_raw(Fraction(3, 4))
    for n in range(2, 300):
        assert Problem2016A5(n).check_raw(get_solution(n))
    for n in range(10**19, 10**19+300):
        f = get_solution(n)
        assert Problem2016A5(n).check_raw(f)

def test_problem_imo_2016_c4():
    from math_construct.problems.imo_shortlist.problem_2016_c4 import Problem2016C4, get_solution
    orig_problem = Problem2016C4.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    for n in range(9, 100, 9):
        assert Problem2016C4(n).check_raw(get_solution(n))

def test_problem_hmo_2018_4():
    from math_construct.problems.croatian.problem_2018_4 import Problem_HMO_2018_4, get_solution
    orig_problem = Problem_HMO_2018_4.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    for n in range(2, 9):
        assert Problem_HMO_2018_4(n).check_raw(get_solution(n))

def test_problem_hmo_2017_2():
    from math_construct.problems.croatian.problem_2017_2 import Problem_HMO_2017_2, get_solution
    orig_problem = Problem_HMO_2017_2.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    for i in range(8):
        for j in range(8):
            if orig_problem.config.original_solution[i][j] != "o":
                small_solution = copy.deepcopy(orig_problem.config.original_solution)
                small_solution[i] = small_solution[i][:j] + "o" + small_solution[i][j+1:]
                not Problem_HMO_2017_2(19).check_raw(small_solution)
                continue
            for r in ["A", "B", "C", "D"]:
                wrong_solution = copy.deepcopy(orig_problem.config.original_solution)
                wrong_solution[i] = wrong_solution[i][:j] + r + wrong_solution[i][j+1:]
                assert not Problem_HMO_2017_2(20).check_raw(wrong_solution)


def test_problem_bul_p3():
    from math_construct.problems.bulgarian.problem_pms_10_4 import ProblemBulPMS20204P10_4, get_solution
    orig_problem = ProblemBulPMS20204P10_4.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    for N in range(3, 20):
        for e in range(0, N*(N-1)//2+1):
            print(N, e)
            assert ProblemBulPMS20204P10_4(N, e).check_raw(get_solution(N, e))

def test_problem_bul_p4():
    from math_construct.problems.bulgarian.problem_mo_r2_2021_8_4 import ProblemBulMO2021P8_4, get_solution
    orig_problem = ProblemBulMO2021P8_4.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    for N in range(30, 80):
        assert ProblemBulMO2021P8_4(N).check_raw(get_solution(N))

def test_problem_hmmt_20017_team_p7():
    from math_construct.problems.backups.problem_feb2017_teamp7 import ProblemHMMTFeb2017TeamP7, get_solution
    orig_problem = ProblemHMMTFeb2017TeamP7.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    p = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59]
    for N in p:
        assert ProblemHMMTFeb2017TeamP7(N).check_raw(get_solution(N))

def test_problem_bul_p5():
    from math_construct.problems.backups.problem_ifym_2013_d4_p8 import ProblemIFYM_2013_P8_4_8, get_solution
    orig_problem = ProblemIFYM_2013_P8_4_8.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    for N in range(10, 100):
        assert ProblemIFYM_2013_P8_4_8(N).check_raw(get_solution(N))

def test_problem_bul_p7():
    from math_construct.problems.bulgarian.problem_ifym_2022_d1_p6_8th import ProblemIFYM_2022_P6_1_8, get_solution
    orig_problem = ProblemIFYM_2022_P6_1_8.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    for N in range(10, 100, 7):
        for n in [10, 23, 133, 455, 1234, 9988]:
            assert ProblemIFYM_2022_P6_1_8(N, n).check_raw(get_solution(N, n))

def test_problem_hmo_2015_4():
    from math_construct.problems.backups.problem_2015_4 import Problem_HMO_2015_4, get_solution
    orig_problem = Problem_HMO_2015_4.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    for n in range(2, 30):
        assert Problem_HMO_2015_4(n).check_raw(get_solution(n))

def test_problem_hmo_2014_2():
    from math_construct.problems.croatian.problem_2014_2 import Problem_HMO_2014_2, get_solution
    orig_problem = Problem_HMO_2014_2.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    assert not orig_problem.check_raw([[1] * 25] * 25)
    for p in [2, 3, 5]:
        M = p+1
        assert Problem_HMO_2014_2(M, (M-1)**2).check_raw(get_solution(M, (M-1)**2))

def test_problem_hmo_2013_4():
    from math_construct.problems.croatian.problem_2013_4 import Problem_HMO_2013_4, get_solution
    orig_problem = Problem_HMO_2013_4.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    for k in range(5, 15):
        assert Problem_HMO_2013_4(k).check_raw(get_solution(k))

def test_problem_putnam_2015_a2():
    from math_construct.problems.putnam.problem_2015_a2 import Problem_Putnam2015A2, get_solution
    orig_problem = Problem_Putnam2015A2.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    Problem_Putnam2015A2.generate()
    for k in range(5, 15):
        for l in range(5, 15):
            if k%2==1 and l%2==1:
                assert Problem_Putnam2015A2(k*l).check_raw(get_solution(k*l))

def test_problem_hmo_2012_4():
    from math_construct.problems.backups.problem_2012_4 import Problem_HMO_2012_4, get_solution
    orig_problem = Problem_HMO_2012_4.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    for d in range(5, 150):
        n = get_solution(d)
        assert Problem_HMO_2012_4(d).check_raw(n)

def test_problem_imo_2000_c4():
    from math_construct.problems.imo_shortlist.problem_2000_c4 import Problem2000C4, get_solution
    orig_problem = Problem2000C4.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    for n in range(5, 25):
        for k in range(n//2+1, 2*n//3):
            assert Problem2000C4(n, k).check_raw(get_solution(n, k))

def test_problem_usamo_1998_5():
    from math_construct.problems.backups.usamo_problem_1998_5 import USAMO_1998_5, get_solution
    orig_problem = USAMO_1998_5.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    for n in range(2, 8):
        assert USAMO_1998_5(n).check_raw(get_solution(n))

def test_problem_imo_2020_n1():
    from math_construct.problems.imo_shortlist.problem_2020_n1 import Problem_IMOShortlist2020_N1, get_solution
    orig_problem = Problem_IMOShortlist2020_N1.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    assert not orig_problem.check_raw([17, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    for k in range(5, 55):
        assert Problem_IMOShortlist2020_N1(k).check_raw(get_solution(k))

def test_problem_bul_p8():
    from math_construct.problems.bulgarian.problem_pms_2022_10_p3 import ProblemBulPMS2022P10_3, get_solution
    orig_problem = ProblemBulPMS2022P10_3.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    for n in range(10, 100):
        assert ProblemBulPMS2022P10_3(n).check_raw(get_solution(n))

def test_problem_imo_2023_a5():
    from math_construct.problems.imo_shortlist.problem_2023_a5 import Problem2023A5, get_solution
    orig_problem = Problem2023A5.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    for N in range(6, 50, 2):
        n, k = 2*N-1, math.ceil((N+1)/2)
        assert Problem2023A5(n, k).check_raw(get_solution(n, k))

def test_problem_imo_2023_c2():
    from math_construct.problems.imo_shortlist.problem_2023_c2 import Problem2023C2, get_solution
    orig_problem = Problem2023C2.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    assert not orig_problem.check_raw([1, 2, 3, 4, 5, 6, 7])
    for k in range(2, 7):
        assert Problem2023C2(k).check_raw(get_solution(k))

def test_problem_imo_2022_c1():
    from math_construct.problems.imo_shortlist.problem_2022_c1 import Problem2022C1, get_solution
    orig_problem = Problem2022C1.get_original()
    sol = orig_problem.config.original_solution
    assert orig_problem.check_raw(sol)
    assert not orig_problem.check_raw([1]*orig_problem.n)
    for n in range(2, 100, 4):
        C = (n+2)//4
        sol = get_solution(n, C)
        check = Problem2022C1(n, C).check_raw(sol)
        assert check

        

def test_problem_serbianmo_2016_2_p4():
    from math_construct.problems.backups.problem_2016_reg_g1_4 import ProblemSerbianRegional2016_G1_4, get_solution
    orig_problem = ProblemSerbianRegional2016_G1_4.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    for N in range(3, 15):
        assert ProblemSerbianRegional2016_G1_4(2*N).check_raw(get_solution(2*N))

def test_problem_serbianmo_2013_2_1():
    from math_construct.problems.serbian.problem_2013_mo_4 import ProblemSMO2013_4
    orig_problem = ProblemSMO2013_4.get_original()
    #orig_sol = orig_problem.config.original_solution
    #assert orig_problem.check_raw(orig_sol)
    #assert not orig_problem.check_raw(orig_sol[:-1])
    for n in range(2, 22, 2):
        problem = ProblemSMO2013_4(n)
        sol = problem.get_solution()
        assert problem.check_raw(sol)
        sol[n-1][0] = sol[n-1][1]
        assert not problem.check_raw(sol)
    assert not ProblemSMO2013_4(2).check_raw([[1, 2, 3], [4, 5, 6]])

def test_problem_serbianmo_2006_2_p3():
    from math_construct.problems.backups.problem_2006_2_p3 import ProblemSMO2006_2_3AP4, get_solution
    orig_problem = ProblemSMO2006_2_3AP4.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    for N in range(10, 50):
        assert ProblemSMO2006_2_3AP4(N).check_raw(get_solution(N))

def test_problem_swiss_2021_r2_z1():
    from math_construct.problems.swiss.problem_2021_r2_z1 import ProblemSwiss2021R2Z1, get_solution
    orig_problem = ProblemSwiss2021R2Z1.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    for N in range(5, 35):
        assert ProblemSwiss2021R2Z1(N).check_raw(get_solution(N))

def test_problem_bul_p6():
    from math_construct.problems.bulgarian.problem_ifym_2015_p7_d4_8th import ProblemIFYM_2015_P7_4_8, get_solution
    orig_problem = ProblemIFYM_2015_P7_4_8.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    for N in range(5, 30):
        assert ProblemIFYM_2015_P7_4_8(2**N).check_raw(get_solution(2**N))
def test_problem_imo_2021_a3():
    from math_construct.problems.imo_shortlist.problem_2021_a3 import Problem2021A3, get_solution
    orig_problem = Problem2021A3.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    for n in range(2, 50):
        assert Problem2021A3(n).check_raw(get_solution(n))

def test_problem_imo_2022_c8():
    from math_construct.problems.imo_shortlist.problem_2022_c8 import Problem2022C8, get_solution
    orig_problem = Problem2022C8.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    for n in range(3, 50):
        assert Problem2022C8(n).check_raw(get_solution(n))

def test_problem_usamo_2006_2():
    from math_construct.problems.usamo.problem_2006_2 import Problem_USAMO_2006_2, get_solution
    orig_problem = Problem_USAMO_2006_2.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    assert not orig_problem.check_raw(list(range(21)))
    for k in range(10, 30):
        N = 2*k**3 + 3*k**2 + 3*k
        assert Problem_USAMO_2006_2(k, N).check_raw(get_solution(k, N))

def test_problem_usamo_2006_4():
    from math_construct.problems.usamo.problem_2006_4 import Problem_USAMO_2006_4, get_solution
    orig_problem = Problem_USAMO_2006_4.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    for n in range(50, 100):
        if n == 5:
            continue
        solution = get_solution(n)
        assert Problem_USAMO_2006_4(n).check_raw(solution)

def test_problem_usamo_2005_1():
    from math_construct.problems.usamo.problem_2005_1 import Problem_USAMO_2005_1, get_solution
    from sympy import primefactors
    orig_problem = Problem_USAMO_2005_1.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    for a in range(2, 15):
        for b in range(2, 15):
            for c in range(2, 15):
                for d in range(2, 15):
                    n = a * b * c * d
                    ps = primefactors(n)
                    if len(ps) == 2 and ps[0]*ps[1] == n:
                        continue
                    assert Problem_USAMO_2005_1(a, b, c, d).check_raw(get_solution(n))


def test_problem_emc_2023_2():
    from math_construct.problems.emc.problem_2023_2 import ProblemEMC20232, get_solution
    orig_problem = ProblemEMC20232.get_original()
    orig_sol = orig_problem.config.original_solution
    assert orig_problem.check_raw(orig_sol)
    assert not orig_problem.check_raw(orig_sol[:-1])
    assert not orig_problem.check_raw(orig_sol[1:] + [orig_sol[0]])
    assert not orig_problem.check_raw(orig_sol[::-1])
    for n in range(5, 35):
        sol = get_solution(n)
        assert ProblemEMC20232(n).check_raw(sol)
        assert not ProblemEMC20232(n).check_raw(sol[:-1])
        assert not ProblemEMC20232(n).check_raw(sol[1:] + [sol[0]])
        assert not ProblemEMC20232(n).check_raw(sol[::-1])

def test_problem_emc_2022_2():
    from math_construct.problems.emc.problem_2022_2 import ProblemEMC20222, get_solution
    orig_problem = ProblemEMC20222.get_original()
    orig_sol = orig_problem.config.original_solution
    assert orig_problem.check_raw(orig_sol)
    assert not orig_problem.check_raw(orig_sol[:-1])
    assert not orig_problem.check_raw(orig_sol[:-1] + [orig_sol[0]])
    for n in range(5,15):
        sol = get_solution(n)
        assert ProblemEMC20222(n).check_raw(sol)
        assert not ProblemEMC20222(n).check_raw(sol[:-1])
        assert ProblemEMC20222(n).check_raw(sol[::-1])

    problem = ProblemEMC20222(1)
    assert not problem.check_raw([4, 2, 2])

def test_problem_emc_2021_1():
    from math_construct.problems.emc.problem_2021_1 import ProblemEMC20211, get_solution
    orig_problem = ProblemEMC20211.get_original()
    orig_sol = orig_problem.config.original_solution
    assert orig_problem.check_raw(orig_sol)
    assert not orig_problem.check_raw(orig_sol[:-1])
    assert not orig_problem.check_raw(orig_sol[:-1] + [orig_sol[0]])
    orig_sol[0] -= 1
    assert not orig_problem.check_raw(orig_sol)
    orig_sol[0] += 2
    assert not orig_problem.check_raw(orig_sol)
    for n in range(5,15):
        sol = get_solution(n)
        assert ProblemEMC20211(n).check_raw(sol)
        assert not ProblemEMC20211(n).check_raw(sol[:-1])
        assert ProblemEMC20211(n).check_raw(sol[::-1])

def test_problem_emc_2016_3():
    from math_construct.problems.emc.problem_2016_3 import ProblemEMC20163, get_solution
    orig_problem = ProblemEMC20163.get_original()
    orig_sol = orig_problem.config.original_solution
    assert orig_problem.check_raw(orig_sol)
    assert not orig_problem.check_raw(orig_sol[:-1])
    assert not orig_problem.check_raw(orig_sol[:-1] + [orig_sol[0]])
    orig_sol[0] -= 1
    assert not orig_problem.check_raw(orig_sol)
    orig_sol[0] += 2
    assert not orig_problem.check_raw(orig_sol)
    for n in range(10, 50):
        sol = get_solution(n)
        assert ProblemEMC20163(n).check_raw(sol)
        assert not ProblemEMC20163(n).check_raw(sol[:-1])
        assert ProblemEMC20163(n).check_raw(sol[::-1])

def test_problem_emc_2016_1():
    from math_construct.problems.emc.problem_2016_1 import ProblemEMC20161, get_solution
    orig_problem = ProblemEMC20161.get_original()
    orig_sol = orig_problem.config.original_solution
    assert orig_problem.check_raw(orig_sol)
    assert not orig_problem.check_raw(orig_sol[:-1])
    for n in range(5, 20):
        sol = get_solution(n)
        assert ProblemEMC20161(n).check_raw(sol)

    simple = ProblemEMC20161(2)
    assert simple.check_raw([55, 57])
    assert not simple.check_raw([53, 55])
    assert not simple.check_raw([8, 9])
def test_problem_usamo_2002_5():
    from math_construct.problems.usamo.problem_2002_5 import Problem_USAMO_2002_5, get_solution
    orig_problem = Problem_USAMO_2002_5.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    for a in range(10, 100):
        for b in range(10, 100):
            if a != b:
                assert Problem_USAMO_2002_5(a, b).check_raw(get_solution(a, b))

def test_problem_putnam_2009_b6():
    from math_construct.problems.putnam.problem_2009_b6 import Problem_Putnam2009B6, get_solution
    orig_problem = Problem_Putnam2009B6.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    assert not orig_problem.check_raw(list(range(orig_problem.m)))
    for m in range(8, 55):
        for n in range(1, 30):
            assert Problem_Putnam2009B6(m, n).check_raw(get_solution(m, n))

def test_problem_handouts_p1():
    from math_construct.problems.misc.problem_handout_nz1 import ProblemNZNT, get_solution
    orig_problem = ProblemNZNT.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    assert not orig_problem.check_raw([orig_problem.config.original_solution[0]] + orig_problem.config.original_solution[:-1])
    for N in range(1, 9):
        assert ProblemNZNT(N).check_raw(get_solution(N))

def test_problem_handouts_p2():
    from math_construct.problems.backups.problem_polish_mo_r2_p5 import ProblemPolish53_R2P5, get_solution
    orig_problem = ProblemPolish53_R2P5.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    assert not orig_problem.check_raw(1234)
    for N in range(5, 20):
        assert ProblemPolish53_R2P5(N).check_raw(get_solution(N))


def test_problem_usamts_1998_1_4():
    from math_construct.problems.usamts.problem_1998_1_4 import Problem_USAMTS_1998_1_4
    orig_problem = Problem_USAMTS_1998_1_4.get_original()
    assert orig_problem.check_raw(orig_problem.config.original_solution)
    for d in range(2, 10):
        problem = Problem_USAMTS_1998_1_4(d)
        assert problem.check_raw(problem.get_solution())

#@pytest.mark.skip(reason="Situational")
def test_lengthstudy():
    from math_construct.problems.bxmo.problem_2015_4 import ProblemBxMO20154
    from math_construct.problems.serbian.problem_2020_tst_4 import ProblemSerbianTst2020_4
    from math_construct.problems.swiss.problem_2018_8_selection import ProblemSwissSelection20188
    from math_construct.problems.usamo.problem_2006_2 import Problem_USAMO_2006_2
    from math_construct.problems.imo_shortlist.problem_2012_c2 import Problem2012C2
    from math_construct.problems.imo_shortlist.problem_2014_c3 import Problem2014C3

    from math_construct.problems.dutch.problem_2010_4 import ProblemDutch20104
    from math_construct.problems.imc.problem_2013_3 import Problem_IMC_2013_3
    from math_construct.problems.imo_shortlist.problem_2008_a2 import Problem2008A2
    from math_construct.problems.dutch.problem_2024_2 import ProblemDutch20242
    from math_construct.problems.imc.problem_2012_2 import Problem_IMC_2012_2

    problem_classes = [ProblemBxMO20154, ProblemSerbianTst2020_4, ProblemSwissSelection20188, Problem_USAMO_2006_2]
    problem_classes.extend([ProblemDutch20104, Problem_IMC_2013_3, Problem2008A2, ProblemDutch20242, Problem_IMC_2012_2])
    problem_classes.append(Problem2014C3)
    for i, cls in enumerate(problem_classes):
        print(i)
        print(cls)
        variants = cls.generate_multiple_explicit(24)
        print(len(variants)) 
        unique_params = set()
        for variant in variants:
            parameter_names = variant.config.parameters
            parameter_values = [getattr(variant, param) for param in parameter_names]
            params = list(zip(parameter_names, parameter_values))
            unique_params.add(str(params))

            sol = variant.get_solution() 
            ok = variant.check_raw(sol)
            print(f"Variant {params}: sol of strlen {len(str(sol))}: verdict {ok}")
        assert(len(unique_params) == 24)