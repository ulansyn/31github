import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d
from time import time
NAME = str(int(time()))
def is_valid_number(text):
    text = text.replace(',', '.')
    try:
        number = float(text)
        if 60 <= number <= 85:
            return True
    except ValueError:
        pass
    return False

def send_graph():
    arr = []
    with open('МОЙВЕС.txt', 'r') as file:
        for line in file:
            if is_valid_number(line):
                arr.append(float(line))
    x = np.arange(len(arr))
    arr1 = arr
    y2 = arr1
    f2 = interp1d(x, y2, )
    x_new = np.linspace(0, len(arr) - 1, 1000)
    y2_smooth = f2(x_new)
    plt.plot(x_new, y2_smooth, color='blue')
    plt.xlabel('Дни')
    plt.ylabel('Вес')

    plt.savefig(f'{NAME}.jpg', dpi=450)

if __name__ == "__main__":
    send_graph()
