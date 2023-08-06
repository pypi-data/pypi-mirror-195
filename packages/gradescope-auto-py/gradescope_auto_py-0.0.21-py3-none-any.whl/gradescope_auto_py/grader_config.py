import json
import pathlib
import shutil
import subprocess
from copy import deepcopy

from .assert_for_pts import AssertForPoints, GradescopePointItem
from .folder import to_temp_folder
from .grader import Grader
from .gradescope import file_run_auto, file_setup_sh


class GraderConfig:
    """ builds autograder zip, prepares files

    Attributes:
        afp_list (list): a list of assert for points expected
        pattern_run_tup (tuple): tuple of strings to search for a file to run.
            strings can contain wildcard *.  if a match is found on the first
            item in the tuple, then search stops.  found ipynb converted to py
        file_add_tup (tuple): additional files to be included in the
            autograder and copied adjacent to student submission
        folder_local (pathlib.Path): root folder of all additional files.
            the full additional file path, as in file_add_tup, is replicated in
            gradescope's submitted folder.  this folder allows for flexibility
            locally
        file_validate_dict (dict): keys are strings of unique file names to
            search for (may include wildcard *), values are point penalties if
            not found (or None if file is mandatory and autograder should stop
            without it)
        s_requirements (str): contents of a requirements.txt file, necessary
            to run autograder
        ipynb_flag (bool): convert all ipynb to py files
    """

    @classmethod
    def from_py(cls, file_afp_tup, file_add_tup=tuple(), folder_local=None,
                **kwargs):
        """ builds configuration from a template assignment

        Args:
            file_afp_tup (tuple):  see Attributes above
            file_add_tup (tuple):  see Attributes above
            folder_local (str): see Attributes above

        Returns:
            grader_config (GraderConfig):
        """
        file_add_tup = tuple(file_add_tup)

        file_afp_tup = tuple(file_afp_tup)

        # default folder local
        if folder_local is None:
            folder_local = '.'
        folder_local = pathlib.Path(folder_local)

        # build file_afp_dict
        afp_list = list()
        for file in file_afp_tup:
            # get list of afp in this file
            file_local = folder_local / file
            afp_list += list(AssertForPoints.iter_assert_for_pts(file_local))

        assert len(afp_list) == len(set(afp_list)), \
            'non-unique assert-for-points detected'

        # get list of required modules to run autograder
        file_tup = tuple(folder_local / file
                         for file in file_add_tup + file_afp_tup)
        with to_temp_folder(file_tup) as folder:
            # build requirements.txt
            process = subprocess.run(['pipreqs', folder])
            assert process.returncode == 0, 'problem building requirements.txt'

            # read in s_requirements
            file_require = folder / 'requirements.txt'
            with open(file_require, 'r') as f:
                s_requirements = f.read()

        return GraderConfig(afp_list=afp_list,
                            file_add_tup=file_add_tup,
                            s_requirements=s_requirements,
                            folder_local=folder_local, **kwargs)

    def __init__(self, afp_list, pattern_run_tup=None, file_add_tup=tuple(),
                 file_validate_dict=dict(), s_requirements=None,
                 folder_local='.', ipynb_flag=False):
        if pattern_run_tup is None:
            pattern_run_tup = '*.py',
        self.pattern_run_tup = tuple(str(f) for f in pattern_run_tup)
        self.afp_list = afp_list
        self.file_add_tup = tuple(str(file) for file in file_add_tup)
        self.file_validate_dict = {str(f): p
                                   for f, p in file_validate_dict.items()}
        self.s_requirements = s_requirements
        self.folder_local = pathlib.Path(folder_local)
        self.ipynb_flag = ipynb_flag

        # warn user if they pass negative point penalty
        for file, pt_penalty in file_validate_dict.items():
            if pt_penalty is None or pt_penalty >= 0:
                continue
            print('validate "penalty" will add pts if missing, pass as '
                  f'positive value to change: {file} {pt_penalty}')

    def build_zip(self, file_zip='auto.zip'):
        """ builds a gradescope autograder zip

        Args:
            file_zip (str): name of zip to create

        Returns:
            file_zip_out (pathlib.Path): zip file created
        """
        file_tup = (file_setup_sh, file_run_auto) + self.file_add_tup
        folder = pathlib.Path(self.folder_local)
        file_tup = tuple(folder / file for file in file_tup)

        # ensure no syntax errors in autograder files
        py_file_tup = tuple(file for file in file_tup if file.suffix == '.py')
        error = Grader.find_syntax_error(file_list=py_file_tup)
        if error is not None:
            s = 'Syntax error found:'
            s = '\n'.join([s, str(error), error.text])
            raise AssertionError(s)

        file_str_dict = {'requirements.txt': self.s_requirements}
        with to_temp_folder(file_tup=file_tup,
                            file_str_dict=file_str_dict) as folder:
            # build config.json in folder
            self.to_json(folder / 'config.json')

            # zip it up
            file_zip = pathlib.Path(file_zip)
            shutil.make_archive(file_zip.with_suffix(''), 'zip', folder)

        return file_zip

    def grade(self, folder_submit='submission', folder_source='source'):
        """ preps & validates files, returns a grader ready to output json

        Args:
             folder_submit (str): submission folder
             folder_source (str): source folder (contains unzipped autograder,
                see build_autograder() for detail)

        Returns:
            grader (Grader): a grader object which has been run on submission
        """
        folder_submit = pathlib.Path(folder_submit)
        folder_source = pathlib.Path(folder_source)

        # initialize grader
        grader = Grader(afp_list=self.afp_list)

        # check if syntax error found in any py file in submission folder
        file_list = list(folder_submit.rglob('*.py'))
        error = Grader.find_syntax_error(file_list=file_list)

        if error:
            # print message about syntax error
            s = 'Syntax error found (no points awarded by autograder):'
            s = '\n'.join([s, str(error), error.text])
            grader.print(s)
            return grader

        for file, pt_penalty in self.file_validate_dict.items():
            # ensure student has submitted files properly
            file_list = [file.name for file in folder_submit.glob(file)]
            if len(file_list) == 1:
                # unique submission found, validation complete
                continue

            # get message
            if len(file_list) > 1:
                msg = f'no unique file for {file} found: {file_list}'
            else:
                msg = f'no file found for pattern: {file}'

            if pt_penalty is None:
                # stop grading, write message
                grader.print('grading stopped: ' + msg)
                return grader
            else:
                # assign penalty
                grader.afp_list.append(GradescopePointItem(name=msg,
                                                           pts=-pt_penalty,
                                                           pts_max=0))

        with to_temp_folder(folder_src=folder_submit) as _folder_submit:
            if self.ipynb_flag:
                for file in _folder_submit.glob('*.ipynb'):
                    if file.with_suffix('.py').exists():
                        continue

                    # convert from ipynb to py
                    cmd = f'jupyter-nbconvert {file} --to script --log-level WARN'
                    subprocess.call(cmd.split(' '))

            # copy supplement files into submit
            for file in self.file_add_tup:
                file_src = folder_source / file
                file_dst = _folder_submit / file

                if file_dst.exists():
                    # student submitted file has same name as supplemental file
                    grader.print(f'overwriting with autograder copy: {file}')

                shutil.copy(file_src, file_dst)

            # get file to run
            file_run = self.get_file_run(_folder_submit,
                                         print_fnc=grader.print)
            if file_run is None:
                return grader

            # run autograder
            grader.grade(file_run=file_run, overwrite=True)

        return grader

    def get_file_run(self, folder_submit, print_fnc=None):
        """ gets file to run, attempts from config, else uses unique py

        Args:
            folder_submit (Path): submission folder
            print_fnc (fnc): accepts a string, will be shown to student

        Returns:
            file_run (Path): .py file to run
        """
        if print_fnc is None:
            print_fnc = print

        for pattern in self.pattern_run_tup:
            # file run should be unique match to pattern
            set_py = set(folder_submit.glob(pattern))

            if len(set_py) == 1:
                # unique file found
                return set_py.pop()
            elif len(set_py) > 1:
                # no unique file submitted
                file_list = sorted(f.name for f in folder_submit.iterdir())
                print_fnc(f'duplicate run file: {pattern} in {file_list}')
                return None

        # no run file found
        print_fnc(f'no run file matches pattern(s): {self.pattern_run_tup}')
        return None

    def to_json(self, file):
        """ writes config to txt file (string of each assert on each line)

        Args:
            file (str): file to write configuration to
        """
        d = deepcopy(self.__dict__)
        # afps are serialized as strings, we rebuild them as afp objects
        d['afp_list'] = [afp.name for afp in d['afp_list']]

        # Path not serializable
        d['folder_local'] = str(d['folder_local'])

        with open(file, 'w') as f:
            json.dump(d, f, sort_keys=True, indent=4)

    @classmethod
    def from_json(cls, file):
        """ reads GraderConfig from txt file

        Args:
            file (str): file to write configuration to
        """
        # load json
        with open(file) as f:
            d = json.load(f)

        # afps are serialized as strings, we rebuild them as afp objects
        d['afp_list'] = [AssertForPoints.from_string(s=s) for s in
                         d['afp_list']]

        # path not serializable
        if 'folder_local' in d:
            d['folder_local'] = pathlib.Path(d['folder_local'])

        return GraderConfig(**d)
