import os
from git_version import GitVersion


# This duplicates the line from settings, but running settings to get it
# would execute the code unde test
PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__))).replace(os.sep, '/')


class TestGitVersion():
    def test_git_version_has_all_the_bits(self):
        gv = GitVersion(PROJECT_ROOT)
        string_representation = str(gv)
        assert 'hash' in string_representation
        assert 'tags' in string_representation
