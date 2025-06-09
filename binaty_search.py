def binary_search(arr, x):
    low = 0
    high = len(arr) - 1
    iterations = 0
    
    while low <= high:
        iterations += 1
        mid = (high + low) // 2
        
        if arr[mid] < x:
            low = mid + 1
        elif arr[mid] > x:
            high = mid - 1
        else:
            return (mid, iterations)
    
    return (-1, iterations)

sorted_array = [1.2, 2.5, 3.7, 4.1, 5.9, 7.3, 8.6, 9.4, 10.8, 12.1]

x = 7.3
result_index, num_iterations = binary_search(sorted_array, x)

if result_index != -1:
    print(f"Елемент {x} знайдено на позиції {result_index}")
else:
    print(f"Елемент {x} не знайдено в масиві")

print(f"Кількість ітерацій: {num_iterations}")

x2 = 6.0
result_index2, num_iterations2 = binary_search(sorted_array, x2)

if result_index2 != -1:
    print(f"Елемент {x2} знайдено на позиції {result_index2}")
else:
    print(f"Елемент {x2} не знайдено в масиві")

print(f"Кількість ітерацій: {num_iterations2}")

x3 = 1.2
result_index3, num_iterations3 = binary_search(sorted_array, x3)

if result_index3 != -1:
    print(f"Елемент {x3} знайдено на позиції {result_index3}")
else:
    print(f"Елемент {x3} не знайдено в масиві")

print(f"Кількість ітерацій: {num_iterations3}")