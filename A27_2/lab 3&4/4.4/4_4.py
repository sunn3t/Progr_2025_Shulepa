import math

def solve_task_4_4():
    print("--- Задача 4.4 ---")
    print("Рівняння: sin(x) = x / 3 на відрізку [1.6, 3]")
    left = 1.6
    right = 3.0
    for _ in range(100):
        mid = (left + right) / 2.0
        val = math.sin(mid) - mid / 3.0
        if val > 0:
            left = mid
        else:
            right = mid
            
    print(f"Корінь рівняння x ≈ {left:.6f}\n")

if __name__ == '__main__':
    solve_task_4_4()
