import filecmp
import pathlib
import tempfile
import zipfile

import gradescope_auto_py as gap
from gradescope_auto_py.grader_config import GraderConfig
from test_grader import json_assert_eq

ex_folder = pathlib.Path(gap.__file__).parents[1] / 'test' / 'ex'

hw0_folder = ex_folder / 'hw0'

grader_config_list = [GraderConfig.from_py(folder_local=ex_folder / 'hw0',
                                           file_afp_tup=('hw0.py',),
                                           ipynb_flag=True,
                                           pattern_run_tup=('hw0_stud.py',
                                                            '*.py')),
                      GraderConfig.from_py(folder_local=ex_folder / 'hw1',
                                           file_afp_tup=('hw1.py', 'test.py'),
                                           file_validate_dict={'hw1.py': None},
                                           file_add_tup=('test.py',),
                                           pattern_run_tup=('test.py',)),
                      GraderConfig.from_py(folder_local=ex_folder / 'hw2',
                                           file_afp_tup=('hw2.py',),
                                           file_validate_dict={'*.py': 10},
                                           file_add_tup=('nothing.py',))]


def test_all_cases():
    """ grades every case in every hw, checks that results.json are valid """
    for grader_config in grader_config_list:
        folder = pathlib.Path(grader_config.folder_local)
        for case_folder in sorted(folder.glob('case*')):
            grader = grader_config.grade(folder_submit=case_folder,
                                         folder_source=folder)

            json_assert_eq(json_dict=grader.get_json(),
                           file_json_expected=case_folder / 'results.json',
                           msg=case_folder)


def zip_to_tempdir(file_zip):
    folder = pathlib.Path(tempfile.TemporaryDirectory().name)
    folder.mkdir()

    with zipfile.ZipFile(file_zip, 'r') as zip_ref:
        zip_ref.extractall(folder)

    return folder


def test_grader_config():
    # test __init__ & from_py()
    grader_config = grader_config_list[0]

    # test make_autograder()
    file_zip = tempfile.NamedTemporaryFile(suffix='auto.zip').name
    grader_config.build_zip(file_zip=file_zip)

    # unzip to compare (zip includes timestamp metadata, hashes won't quite do)
    folder = zip_to_tempdir(file_zip)
    folder_exp = zip_to_tempdir(hw0_folder / 'hw0_auto.zip')
    _, mismatch, _ = filecmp.cmpfiles(folder, folder_exp,
                                      common=folder.iterdir())
    assert not mismatch, 'zip file generation error'

    # swaps install specific hw0_folder for 'hw0_folder' (makes json load /
    # save expectation standard across installations)
    grader_config.folder_local = pathlib.Path('hw0_folder_placeholder')

    # test from_json()
    file_config_json = hw0_folder / 'hw0_grader_config.json'
    grader_config_exp = GraderConfig.from_json(file_config_json)
    assert grader_config.__dict__ == grader_config_exp.__dict__

    # test to_json()
    file = tempfile.NamedTemporaryFile(suffix='.json').name
    grader_config.to_json(file=file)
    grader_config2 = GraderConfig.from_json(file=file)
    assert grader_config2.__dict__ == grader_config.__dict__
