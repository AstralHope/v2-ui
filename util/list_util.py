def get_index(l, key, value):
    i = 0
    for x in l:
        if x.get(key) == value:
            return i
        i += 1
    return -1


def get(l, key, value):
    index = get_index(l, key, value)
    if index < 0:
        return None
    return l[index]


def exist(l, key, value):
    return get_index(l, key, value) >= 0


def pop(l, key, value):
    index = get_index(l, key, value)
    if index >= 0:
        return l.pop(index)
    return None
