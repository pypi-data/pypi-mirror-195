import os
from typing import Dict, List


def model() -> Dict[str, List[float]]:
    vectors = {}
    file = open(os.path.join(os.path.dirname(__file__), "data/glove-wiki-gigaword-50"), "r")
    file.readline()
    for line in file:
        values = line.split()
        key = values[0]
        vector = [float(x) for x in values[1:]]
        vectors[key] = vector
    file.close()
    return vectors
