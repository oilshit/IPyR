import math

from .equations import *

def PowerRegression(data_x, data_y):
    """
    y = a * x^b
    
    ln (y) = ln (a) + b ln (x)
    
    ln (y) = b ln (x) + ln (a)

    ln (q) = n ln (p_res^2 - p^2) + ln (C)
    
    y = bx + a // y = b1 (x) + b0
    """

    n = len(data_x)

    x = [math.log(i) for i in data_x]
    y = [math.log(i) for i in data_y]
    xy = [x[i] * y[i] for i in range(n)]
    x_squared = [i**2 for i in x]
    y_squared = [i**2 for i in y]

    sums = {
        "x": sum(x),
        "y": sum(y),
        "xy": sum(xy),
        "x_squared": sum(x_squared),
        "y_squared": sum(y_squared),
    }

    b1 = ((n * sums["xy"]) - (sums["x"] * sums["y"])) / \
        ((n * sums["x_squared"] - sums["x"]**2))
    
    b0 = (sums["y"] - b1 * sums["x"]) / n
    b0 = math.exp(b0)

    return (b0, 1 / b1)
