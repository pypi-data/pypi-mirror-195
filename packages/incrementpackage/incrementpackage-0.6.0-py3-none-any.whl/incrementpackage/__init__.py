from typing import List


def increment(data:List, multiple:int):
    d = []
    for x in data:
        d.append(x * multiple)
    return d

