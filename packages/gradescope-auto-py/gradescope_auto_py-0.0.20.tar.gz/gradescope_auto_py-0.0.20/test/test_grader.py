import json
import pathlib
import re

import gradescope_auto_py as gap

# build config
hw0_folder = pathlib.Path(gap.__file__).parents[1] / 'test' / 'ex' / 'hw0'

file_config = hw0_folder / 'hw0_grader_config.json'
file_submit = hw0_folder / 'case_typical0' / 'hw0_stud.py'
file_prep_expect = hw0_folder / 'case_typical0' / 'hw0_prep.py'
file_submit_err_syntax = hw0_folder / 'case_syntax_error' / 'hw0_stud.py'
file_submit_err_runtime = hw0_folder / 'case_runtime_error' / 'hw0_stud.py'
file_json_expected = hw0_folder / 'test.json'

grader_config = gap.GraderConfig.from_json(file=file_config)


def json_assert_eq(json_dict, file_json_expected, msg=''):
    """ compares a json dictionray with expected file (normalizes tmp dirs) """
    json_dict['output'] = re.sub('/tmp/.*/',
                                 '/tmp/<tmp-folder-here>/',
                                 json_dict['output'])

    # confirm expected outputs
    with open(file_json_expected, 'r') as f:
        json_expected = json.load(f)

    s = json.dumps(json_dict, indent=4, sort_keys=True)

    assert json_expected == json_dict, msg


def test_prep_file():
    s_file_prep, _ = gap.Grader.prep_file(file=file_submit, token='token')
    assert s_file_prep == open(file_prep_expect).read()


def test_check_for_syntax_error():
    assert gap.Grader.find_syntax_error(file=file_submit) is None

    assert gap.Grader.find_syntax_error(file=file_submit_err_syntax)


def test_get_json():
    # manually build a "completed" grader
    grader = gap.Grader(afp_list=grader_config.afp_list)
    grader.s_output_list = ['this will be printed in json out', 'another line']
    grader.stderr = 'stderr goes here'

    with open(file_json_expected, 'r') as f:
        json_expected = json.load(f)

    assert json_expected == grader.get_json()


def test_parse_output():
    grader = gap.Grader(afp_list=grader_config.afp_list)

    grader.stdout = open(hw0_folder / 'stdout.txt').read()
    grader.parse_output(token='token')

    score_list = [afp.score for afp in grader.afp_list]
    score_list_expected = [1, 0, 2]
    assert score_list == score_list_expected


def test_grade():
    for case in ['case_typical0', 'case_runtime_error']:
        # prep
        grader = gap.Grader(afp_list=grader_config.afp_list)
        case_folder = hw0_folder / case
        file_run = grader_config.get_file_run(folder_submit=case_folder)

        # grade
        grader.grade(file_run=file_run)

        json_assert_eq(json_dict=grader.get_json(),
                       file_json_expected=case_folder / 'results.json',
                       msg=case)
