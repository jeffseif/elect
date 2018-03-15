#! /usr/bin/env python3


def factorial(n):
    result = 1
    while n >= 2:
        result *= n
        n -= 1
    return result


def stirling(n):
    return (
        (2 * pi * n) ** 0.5
        * (n / e) ** n
    )


def choose(n, k):
    ratio = 1.
    stop = (n - k + 1)
    while n >= stop or k > 1:
        if n >= stop:
            ratio *= n
            n-= 1
        if k > 1:
            ratio /= k
            k -= 1
    return ratio


def bernoulli(trials, successes, p):
    return (
        choose(trials, successes)
        * p ** successes
        * (1 - p) ** (trials - successes)
    )


def bernoulli_extreme(trials, successes, p):
    return sum(
        bernoulli(trials, successes + excess, p)
        for excess in range(trials - successes + 1)
    )


def erf(x):
    sign = (-1) ** (x < 0)
    x = abs(x)

    # A&S formula 7.1.26
    p  =  0.3275911
    t = 1.0/(1.0 + p*x)
    constants = [
        1.061405429,
        -1.453152027,
        1.421413741,
        -0.284496736,
        0.254829592,
    ]

    temporary = 0
    for constant in constants:
        temporary *= t
        temporary += constant

    from math import exp

    return sign * (1.0 - temporary * t * exp(-x * x))


def normal_extreme(trials, successes, p):
    if trials == 0:
        return 0

    expected = trials *  p
    desired = successes - 0.5
    std = (expected * (1 - p)) ** 0.5

    return 1 - 0.5 * (1 + erf((desired - expected) / std / 2 ** 0.5))


def flip_outcome(winning, losing, reporting):
    winning, losing = max(winning, losing), min(winning, losing)

    reported = (winning + losing)
    difference = abs(winning - losing)

    total = int(reported / reporting)
    remaining = total - reported
    
    trials = remaining
    successes = int((remaining + difference) / 2)
    p = losing / reported

    if remaining * p < 30:
        print(bernoulli_extreme(trials, successes, p))
    else:
        print(normal_extreme(trials, successes, p))


def main():
    dems = 1010
    reps = 990
    reporting = 0.5
    flip_outcome(dems, reps, reporting)


if __name__ == '__main__':
    main()
