from typing import List


class VectorUnit:

    @staticmethod
    def slice(vec: List):
        return vec[0], vec[1], vec[2], vec[3]

    @staticmethod
    def compound(a, b, c, d):
        return [a, b, c, d]
