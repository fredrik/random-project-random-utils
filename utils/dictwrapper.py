class Dict(dict):
    def __getattr__(self, name):
        if name in self:
            return self.__getitem__(name)
        raise AttributeError(name)


def dictify(obj):
    if isinstance(obj, dict):
        for k, v in obj.items():
            obj[k] = dictify(v)
        return Dict(obj)
    elif isinstance(obj, (list, tuple)):
        return [dictify(v) for v in obj]
    else:
        return obj
