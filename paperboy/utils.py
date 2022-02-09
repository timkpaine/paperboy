def class_to_name(cls):
    return ".".join((cls.__module__, cls.__qualname__))


def name_to_class(name):
    components = name.split(".")
    mod = __import__(components[0])
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod
