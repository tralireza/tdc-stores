from lib import (gcd)


def test_gcd():
    pairs = [[(0, 0), (0, 1)], [(51, 0), (51, 1)], [(23, 34), (-23, 34)], [(0, 90), (90, 0)], [(45, 45), (0, 90)]]
    distance = [111, 70, 5115, 10008, 6672]

    for i, pair in enumerate(pairs):
        d = gcd.gcd(pair[0], pair[1])
        print(pair[0], pair[1], ':', distance[i], '~', d, '->', round(d))

        assert distance[i] == round(d)
