def strip_size(text):
    return text.replace('$o', '').replace('$w', '')


def is_bound(m):
    return hasattr(m, '__self__')
