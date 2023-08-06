#!/usr/bin/env python3
# CLI for grading a single submission from the zip file
import argparse
import pathlib
import shutil
import tempfile
import zipfile

import pandas as pd
from tqdm import tqdm

import gradescope_auto_py as gap


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
        grader = grader_config.grade(folder_submit=folder_submit,
                                     folder_source=folder_src)

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
            print(f'{name}:')

            # autograder feedback (to student via gradescope)
            print(df['output'])

            # local feedback
            print('{score_total} / {score_max} = {perc:.4f}'.format(**row))

            if row['perc'] < 1:
                print('the following assert-for-points failed:')
                for col, x in row.items():
                    if 'assert' in col and x == 0:
                        print(col)


if __name__ == '__main__':
    main()
