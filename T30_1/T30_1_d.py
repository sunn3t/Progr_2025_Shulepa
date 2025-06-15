import math

def inv3_series_epsilon(x: float, eps: float) -> float:
    """
    Обчислює суму членів ряду 1/(1+x)^3 = sum_{n=0..N} (-1)^n * (n+1)(n+2)/2 * x^n
    додаючи члени, поки |term| > eps.
    """
    if abs(x) >= 1:
        raise ValueError("|x| повинно бути менше 1 для збіжності ряду")
    total = 0.0
    n = 0
    term = 1.0
    while abs(term) > eps:
        total += term
        n += 1
        coef = (n+1)*(n+2)/2
        term = ((-1)**n) * coef * (x**n)
    return total


def test_inv3():
    tests = [
        (0.1, 1e-3),
        (0.1, 1e-6),
        (0.5, 1e-4),
        (0.5, 1e-6),
        (0.8, 1e-5),
    ]
    print("Тестування inv3_series_epsilon:")
    for x, eps in tests:
        approx = inv3_series_epsilon(x, eps)
        exact = 1.0 / ((1 + x)**3)
        err = approx - exact
        print(f"x={x:.2f}, eps={eps:.0e}: approx={approx:.8f}, exact={exact:.8f}, err={err:.2e}")

if __name__ == '__main__':
    test_inv3()
