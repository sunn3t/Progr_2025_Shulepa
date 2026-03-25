def find_left_bound(arr, target):
    left, right = 0, len(arr) - 1
    result = -1
    
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            result = mid
            right = mid - 1
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return result

def find_right_bound(arr, target):
    left, right = 0, len(arr) - 1
    result = -1
    
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            result = mid
            left = mid + 1
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
            
    return result

n = int(input())

if n > 0:
    animals = list(map(int, input().split()))
else:
    animals = []
    try:
        input() 
    except EOFError:
        pass

m = int(input())
req = list(map(int, input().split()))
for q in req:
    left_idx = find_left_bound(animals, q)
    
    if left_idx == -1:
        print(0)
    else:
        right_idx = find_right_bound(animals, q)
        print(right_idx - left_idx + 1)
