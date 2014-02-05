import os
from subprocess import Popen, PIPE


def _exec_git(git_cmd, project_root=None):
    if isinstance(git_cmd, basestring):
        git_cmd = git_cmd.split()
    if project_root:
        git = ['git',
               '--git-dir=%s' % os.path.join(project_root, '.git'),
               '--work-tree=%s' % project_root]
    else:
        git = ['git']
    p = Popen(git + git_cmd, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    if stderr:
        raise Exception("Error getting versioning info from git.\n" + \
                        "Executed: %s\n" % ' '.join(git + git_cmd) + \
                        "stderr: %s" % stderr + \
                        "stdout: %s" % stdout)
    else:
        return stdout.split('\n')[:-1]


class GitVersion(object):
    def __init__(self, project_root=None):
        self.project_root = project_root

    def hash_of_head(self):
        hash, _, _ = _exec_git('log -1 --format=%H%n%ci%n%s', self.project_root)
        return hash

    def __str__(self):
        hash, date, subject = _exec_git('log -1 --format=%H%n%ci%n%s', self.project_root)
        tags = _exec_git('describe --tags', self.project_root)
        changes = _exec_git('status --porcelain', self.project_root)
        return  'hash: %s\n' % hash + \
                'date: %s\n' % date + \
                'subject: %s\n' % subject + \
                'tags: %s\n' % ', '.join(tags) + \
                ('changes: %s\n' % ', \n         '.join(changes) if len(changes) else '')
