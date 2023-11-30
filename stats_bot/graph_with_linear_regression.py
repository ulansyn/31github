# Этот код создает график, который может быть полезен для визуализации изменений в весе 
# и выделения тенденций в данных. Линия регрессии помогает увидеть общий тренд в изменении веса,
# а синяя зона подчеркивает разброс между максимальным и минимальным весом. 
import matplotlib.pyplot as plt
import numpy as np
PATH = 'PATH'

arr1 = [] # массив для хранения максимального веса в течение дня
arr2 = [] # массив для хранения минимального веса в течение дня
arr3 = [] 
for i in range(len(arr2)):
    arr3.append((arr1[i]+arr2[i])/2)
indices = np.arange(len(arr3))
coefficients = np.polyfit(indices, arr3, 1)
regression_line = np.polyval(coefficients, indices)
plt.figure(figsize=(12, 7))
plt.plot(indices, regression_line, label='линия регрессии', color='gray', linewidth=1.5, alpha=0.75)
plt.plot(arr1, label='maximum weight', color='blue', linestyle='-', linewidth=1)
plt.plot(arr2, label='minimum weight', color='blue', linestyle='-', linewidth=1)
plt.plot(arr3, label='average weight', color='red', linestyle='--', linewidth=1)
plt.fill_between(range(len(arr1)), arr1, arr2, color='blue', alpha=0.1)

plt.legend()

plt.title('Графики sin(x) и cos(x)')
plt.xlabel('x')
plt.ylabel('y')

plt.grid(True)
plt.savefig(PATH, dpi=250)
