#!/usr/bin/env python3
# CLI for grading a single submission from the zip file
import argparse
import pathlib
import shutil
import tempfile
import zipfile

import pandas as pd
import yaml
from tqdm import tqdm

import gradescope_auto_py as gap


def load_metadata(file_meta, folder_submit_dict):
    with open(file_meta) as f:
        try:
            # load student metadata
            yaml_dict = yaml.safe_load(f)

            # rename folders to include student names & emails
            for folder, row in yaml_dict.items():
                if folder in folder_submit_dict:
                    stud_list = list()
                    for d in row[':submitters']:
                        s = f'{d[":name"]} ({d[":email"]})'
                        stud_list.append(s)

                    new_name = f'{folder} {",".join(stud_list)}'

                    # rename
                    folder_submit_dict[new_name] = folder_submit_dict[folder]
                    del folder_submit_dict[folder]
        except yaml.YAMLError as exc:
            print(exc)

    return folder_submit_dict


def main(*args, **kwargs):
    parser = argparse.ArgumentParser(
        description='grades a single submission, displays results as table.'
                    '(see doc at: https://github.com/matthigger/gradescope_auto_py/)')
    parser.add_argument('-z', '--zip', dest='file_zip',
                        help='autograder zip file')
    parser.add_argument('-s', '--submit', dest='submit',
                        help='submitted file (or folder).  to grade multiple '
                             'submissions use wildcard *.  (e.g. the default'
                             'gradescope export submissions yields many '
                             'folders which match "submission_*")')
    parser.add_argument('-c', '--csv', dest='file_csv', default=None,
                        help='filename to write csv output')
    parser.add_argument('-q', '--quiet', dest='quiet', default=False,
                        help='silences output')
    parser.add_argument('--skip_yaml', dest='skip_yaml', action='store_true',
                        help='if a gradescope yaml file of student names / '
                             'emails is found in multiple submission mode, '
                             'script will load it (looks in gradescope '
                             'default location). this option disables the '
                             'feature')
    args = parser.parse_args(*args, **kwargs)

    # setup autograder zip
    folder = pathlib.Path(tempfile.TemporaryDirectory().name)
    folder_src = folder / 'src'
    with zipfile.ZipFile(args.file_zip, 'r') as zip_ref:
        zip_ref.extractall(folder_src)

    folder_submit_dict = dict()
    if '*' in args.submit:
        # grade all submission folders which match pattern
        for folder_submit in pathlib.Path('.').glob(args.submit):
            if folder_submit.is_dir():
                folder_submit_dict[folder_submit.name] = folder_submit

        file_meta = folder_submit.parent / 'submission_metadata.yml'
        if not args.skip_yaml and file_meta.exists():
            if not args.quiet:
                print('loading student email / names (can take ~3 seconds)')

            # rename keys to include student & email from metadata
            folder_submit_dict = load_metadata(file_meta, folder_submit_dict)

    else:
        # if submit is a single file, copy into its own folder
        folder_submit = pathlib.Path(args.submit)
        if not folder_submit.is_dir():
            # if an individual file is passed (rather than folder) move to tmp dir
            folder_submit = folder / 'submit'
            folder_submit.mkdir(parents=True)
            file_src = pathlib.Path(args.submit)
            shutil.copyfile(file_src, folder_submit / file_src.name)

        folder_submit_dict[args.submit] = folder_submit

    # load config
    grader_config = gap.GraderConfig.from_json(folder_src / 'config.json')
    score_max = sum(afp.score_max for afp in grader_config.afp_list)

    # grade
    tqdm_dict = {'disable': args.quiet, 'desc': 'grading submission',
                 'total': len(folder_submit_dict)}
    series_list = list()
    for name, folder_submit in tqdm(folder_submit_dict.items(), **tqdm_dict):
        try:
            grader = grader_config.grade(folder_submit=folder_submit,
                                         folder_source=folder_src)
        except UnicodeDecodeError as e:
            print(f'skipping: {name} / {folder_submit}:')
            print(e)
        except Exception as e:
            print(f'error encounted on submission: {name} / {folder_submit}:')
            raise e

        json_dict = grader.get_json()
        score_total = sum(afp.score for afp in grader.afp_list
                          if afp.score is not None)
        row_dict = {'output': json_dict['output'],
                    'score_max': score_max,
                    'score_total': score_total,
                    'perc': score_total / score_max}
        row_dict.update({afp.name: afp.score for afp in grader.afp_list})
        series_list.append(pd.Series(row_dict, name=name))

    df = pd.DataFrame(series_list)
    if args.file_csv is not None:
        # print csv file
        df.to_csv(args.file_csv)

    if not args.quiet:
        for name, row in df.iterrows():
            print('-' * 30 + '\n' + name)

            # autograder feedback (to student via gradescope)
            print('output: ' + row['output'])

            # local feedback
            s = '{score_total} pts of {score_max} total = {perc:.4f}'
            print(s.format(**row))

            if row['perc'] < 1:
                print('the following assert-for-points failed:')
                for col, x in row.items():
                    if 'assert' in col and x == 0:
                        print(col)


if __name__ == '__main__':
    main()
