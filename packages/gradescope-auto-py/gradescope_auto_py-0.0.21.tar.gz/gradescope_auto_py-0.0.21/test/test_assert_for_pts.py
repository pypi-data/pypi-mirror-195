import json
import pathlib

import gradescope_auto_py as gap
from gradescope_auto_py.assert_for_pts import *

hw0_folder = pathlib.Path(gap.__file__).parents[1] / 'test' / 'ex' / 'hw0'

s = "assert 3+2==5, 'addition fail (3 pts)'"


def test_init():
    afp = AssertForPoints.from_string(s=s)
    assert afp.name == "assert 3 + 2 == 5, 'addition fail (3 pts)'"
    assert afp.score_max == 3

    afp = AssertForPoints.from_ast_assert(ast_assert=ast.parse(s).body[0])
    assert afp.name == "assert 3 + 2 == 5, 'addition fail (3 pts)'"
    assert afp.score_max == 3

    # test not plural pts ("pt") and decimal point values
    afp = AssertForPoints.from_string(s="assert 3+2==5, 'addition fail (.1 "
                                       "pt)'")
    assert afp.score_max == .1


def test_eq():
    afp = AssertForPoints.from_string(s=s)
    assert afp == afp


def test_iter_assert_for_pts():
    with open(hw0_folder / 'hw0_grader_config.json', 'r') as f:
        afp_set_expect = set(json.load(f)['afp_list'])

    afp_iter = AssertForPoints.iter_assert_for_pts(hw0_folder / 'hw0.py')
    afp_set = set([afp.name for afp in afp_iter])

    assert afp_set == afp_set_expect
