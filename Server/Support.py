
def SortingListInDict(_list: list, _element: int) -> dict:
    res = {}
    if _list is None:
        return res
    if len(_list) > 1:
        elem = list(zip(*_list))
        for i in elem[_element]:
            reselev = list(filter(lambda x: x[_element] == i, _list))
            reselev.sort(key=lambda tup: tup[0])
            res[i] = reselev
    elif len(_list) == 1:
        res[_list[0][_element]] = _list
    return res
