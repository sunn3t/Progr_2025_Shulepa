import math

def ln1p_series_epsilon(x: float, eps: float) -> float:
    """
    Повертає суму членів розкладення ln(1+x)
    y = sum_{n=1..N} (-1)^{n-1} * x^n / n!,
    поки абсолютне значення наступного члена > eps.
    """
    if abs(x) >= 1:
        raise ValueError("|x| повинно бути менше 1 для збіжності розкладу")
    n = 1
    term = x
    total = 0.0
    while abs(term) > eps:
        total += term
        n += 1
        term = ((-1)**(n-1)) * (x**n) / math.factorial(n)
    return total


def test_series():
    tests = [
        (0.5, 1e-3),
        (0.5, 1e-6),
        (0.9, 1e-4),
        (0.9, 1e-6),
        (0.2, 1e-5),
    ]
    print("Тестування ln1p_series_epsilon:")
    for x, eps in tests:
        approx = ln1p_series_epsilon(x, eps)
        exact = math.log1p(x)
        err = approx - exact
        print(f"x={x:.2f}, eps={eps:.0e}: approx={approx:.8f}, exact={exact:.8f}, err={err:.2e}")

if __name__ == '__main__':
    test_series()
