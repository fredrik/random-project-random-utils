import unicodedata


# from http://stackoverflow.com/a/518232/1442289
def normalise_accented_name(s):
    return ''.join((c for c in unicodedata.normalize('NFD', unicode(s)) if unicodedata.category(c) != 'Mn'))
