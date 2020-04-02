import math
import numpy as np
A = 0
#P0 = 0


def Loading(time, E_infinity, E1, lambda1):
    time = np.array(time)
    p1 = 0.5 * E_infinity * time ** 2
    p2 = (E1 / lambda1) * (time - (1 / lambda1))
    p3 = (E1 / (lambda1 ** 2)) * (math.e ** (-lambda1 * time))
    return A * (p1 + p2 + p3)


Loading.__setattr__("bounds", ([0, 0, 0], [np.inf, np.inf, np.inf]))


def Loading_2(time, E_infinity, E1, lambda1, E2, lambda2):
    p1 = 0.5 * E_infinity * time ** 2
    p2 = (E1 / lambda1) * (time - (1/lambda1))
    p3 = (E1 / (lambda1 ** 2)) * (math.e ** (-lambda1 * time))
    p4 = (E2 / lambda2) * (time - (1/lambda2))
    p5 = (E2 / (lambda2 ** 2)) * (math.e ** (-lambda2 * time))
    return A * (p1 + p2 + p3 + p4 + p5)


Loading_2.__setattr__("bounds", ([0, 0, 0, -np.inf, 0], [np.inf]*5))
#Loading_2.__setattr__("p0", [10000, 10000, 10000, 10000, 10000])


def Loading_3(time, E_infinity, E1, lambda1, E2, lambda2, E3, lambda3):
    p = 0.5 * E_infinity * time ** 2
    p += (E1 / lambda1) * (time - (1/lambda1))
    p += (E1 / (lambda1 ** 2)) * (math.e ** (-lambda1 * time))
    p += (E2 / lambda2) * (time - (1/lambda2))
    p += (E2 / (lambda2 ** 2)) * (math.e ** (-lambda2 * time))
    p += (E3 / lambda3) * (time - (1/lambda3))
    p += (E3 / (lambda3 ** 2)) * (math.e ** (-lambda3 * time))
    return A * p


#Loading_3.__setattr__("bounds", ([0]*7, [np.inf]*7))


def Holding(time, P0, tao, b):
    time = np.array(time)
    time = time - time[0]
    return P0 * (math.e ** (-(time / tao) ** b))


Holding.__setattr__("bounds", ([0, 0, 0], [np.inf, np.inf, np.inf]))


def Linear(time, m, b):
    return m * np.array(time) + b


def Holding_2_Exp(time, P0, tao_0, P1, tao_1):
    time = np.array(time)
    time = time - time[0]
    return P0 * (math.e**(-time/tao_0)) + P1 * (math.e**(-time/tao_1))


Holding_2_Exp.__setattr__("bounds", ([0, 0, 0, 0], [np.inf, np.inf, np.inf, np.inf]))


def Holding_1_Exp(time, P0, tao_0):
    time = time - time[0]
    return P0 * (math.e**(-time/tao_0))


Holding_1_Exp.__setattr__("bounds", ([0, 0], [np.inf, np.inf]))
