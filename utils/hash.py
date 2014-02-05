class hashabledict(dict):
    # from http://stackoverflow.com/questions/1151658/python-hashable-dicts
    def __hash__(self):
        return hash(tuple(sorted(self.items())))


def hashable_anything(anything):
    if isinstance(anything, dict):
        # turn dict into hashabledict, convert values too
        d = hashabledict()
        for key, value in sorted(anything.items()):
            d[key] = hashable_anything(value)
        return d
    elif isinstance(anything, list):
        # turn list into tuple, convert elements too
        return tuple(hashable_anything(element) for element in anything)
    else:
        # hope for the best
        return anything
