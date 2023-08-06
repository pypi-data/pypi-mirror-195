import ast
import re

from gradescope_auto_py.visibility import Visibility


class NoPointsInAssert(Exception):
    pass


class GradescopePointItem:
    """ a gradescope point item, awards (or penalizes) points to student

    Attributes:
        score (float): points earned.  None if the assert hasn't been run yet
        score_max (float): number of points assert is worth (not a particular
            student pts earned)
        name (str): string of assert statement
        viz (Visibility): visibility setting (see Visibility)
    """

    def __init__(self, pts_max, name, viz=None, pts=None):
        self.score = pts
        self.score_max = pts_max
        self.name = name
        self.viz = viz

        if self.viz is None:
            # default to visible
            self.viz = Visibility.VISIBLE

    def record(self, passes):
        """ observe if assert passes (update pts)
        Args:
            passes (bool): assert passes, give full score
        """
        if self.score is None:
            self.score = 0
        self.score = max(self.score, self.score_max * bool(passes))

    def get_json_dict(self, **kwargs):
        """ builds dict of a single `test` (see key "tests" in link)

        note that by default the test will fail (score=0), be sure to pass
        score (and any other relevant keys) to overwrite these defaults

        https://gradescope-autograders.readthedocs.io/en/latest/specs/#output-format

        Args:
            kwargs: added (overwritten) values
        """
        json_dict = {'score': self.score,
                     'max_score': self.score_max,
                     'name': self.name,
                     'visibility': self.viz.value}
        json_dict.update(kwargs)
        return json_dict

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return isinstance(other, type(self)) and self.name == other.name


class AssertForPoints(GradescopePointItem):
    """ an assertion to be evaluated for points

    Attributes:
        ast_assert (ast.Assert): Assert statement

    >>> afp = AssertForPoints.from_string(s="assert 3+2==5, 'addition fail (3 pts)'")
    >>> afp.name
    "assert 3 + 2 == 5, 'addition fail (3 pts)'"
    >>> afp.score_max
    3.0
    >>> AssertForPoints.from_string(s="assert 3+2==5, 'addition fail'")
    Traceback (most recent call last):
     ...
    assert_for_pts.NoPointsInAssert: assert 3 + 2 == 5, 'addition fail'
    """

    @classmethod
    def iter_assert_for_pts(cls, file):
        """ iterates through all assert_for_pts instances in a file

        Yields:
            assert_for_pts (AssertForPoints):
        """
        with open(str(file), 'r') as f:
            s_file = f.read()

        ast_root = ast.parse(s_file)
        for ast_assert in ast.walk(ast_root):
            if not isinstance(ast_assert, ast.Assert):
                continue

            try:
                yield AssertForPoints.from_ast_assert(ast_assert)
            except NoPointsInAssert:
                continue

    @classmethod
    def from_string(cls, s):
        ast_assert = ast.parse(s).body[0]
        return cls.from_ast_assert(ast_assert)

    @classmethod
    def from_ast_assert(cls, ast_assert):
        assert isinstance(ast_assert, ast.Assert)

        # normalize string (spaces between operators etc removed via unparse)
        s = ast.unparse(ast_assert)

        # get points
        if ast_assert.msg is None:
            # no string in assert
            raise NoPointsInAssert(s)
        msg = ast.unparse(ast_assert.msg)
        match_list = re.findall(r'\d*\.?\d+ pts?', msg)
        if not len(match_list) == 1:
            raise NoPointsInAssert(s)
        s_pts = match_list[0]
        pts_max = float(s_pts.split(' ')[0])

        # parse visibility setting
        s_viz = ast_assert.msg.s.split(s_pts)[1]
        viz = Visibility.parse(s_viz)

        return AssertForPoints(name=s, pts_max=pts_max, viz=viz,
                               ast_assert=ast_assert)

    def __init__(self, *args, ast_assert=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.ast_assert = ast_assert

    def get_print_ast(self, token):
        # build new node which prints afp.s, token, whether test passed
        s_grader_assert = f'print(1, 2)'
        new_node = ast.parse(s_grader_assert).body[0]
        new_node.value.args = [ast.Constant(self.name),
                               ast.Constant(token),
                               self.ast_assert.test]
        return new_node
