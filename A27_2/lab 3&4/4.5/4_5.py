import math

def solve_task_4_5():
    print("--- Задача 4.5 ---")
    print("Рівняння: x^3 + 4x^2 + x - 6 = 0 на відрізку [0, 2]")
    
    left = 0.0
    right = 2.0
    
    for _ in range(100):
        mid = (left + right) / 2.0
        val = mid**3 + 4 * mid**2 + mid - 6.0
        if val < 0:
            left = mid
        else:
            right = mid
            
    print(f"Корінь рівняння x ≈ {left:.6f}")
