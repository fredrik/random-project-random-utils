import os
import errno
import re


def mkdir_p(path):
    """
    'mkdir -p' in Python
    """
    # The original was from:
    #   http://stackoverflow.com/questions/600268/mkdir-p-functionality-in-python
    # To guard against the case in Jacob Gabrielson's answer,
    # I added the and clause - DW
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


strip_non_alpha_re = re.compile("\W+")


def strip_non_alpha(s):
    return strip_non_alpha_re.sub('', s)


def dump_file_name(match, type):
    DUMP_FILE_NAME = "%(id)05d-%(kickoff)s-%(home)s-v-%(away)s.%(type)s"
    return DUMP_FILE_NAME % \
            {'id': match.id,
             'kickoff': match.start.strftime("%Y%m%d-%H%M"),
             'home': strip_non_alpha(match.home.display_name),
             'away': strip_non_alpha(match.away.display_name),
             'type': type,
            }
