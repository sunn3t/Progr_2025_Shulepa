import math

def solve():
    c = float(input())
    # Оскільки f(0) = 0, а f(10^5) > 10^10, корінь точно лежить у межах [0, 10^5]
    left = 0.0
    right = 100000.0
    for _ in range(100):
        mid = (left + right) / 2.0
        value = mid**2 + math.sqrt(mid)
        if value < c:
            left = mid
        else:
            right = mid         
    print(f"{left:.10f}")

if __name__ == '__main__':
    solve()
