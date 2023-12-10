import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
import json
PATH = 'PATH'

def fuller(json_data):
    def full_date(data):
        # Преобразуем даты в формат datetime
        date_format = "%d.%m.%y"
        dates = [datetime.strptime(date, date_format) for date in data.keys()]

        # Найдем минимальную и максимальную даты
        min_date = min(dates)
        max_date = max(dates)

        # Создадим пустые массивы для недостающих дат
        current_date = min_date
        while current_date <= max_date:
            formatted_date = current_date.strftime(date_format)
            if formatted_date not in data:
                data[formatted_date] = []
            current_date += timedelta(days=1)
        return data

    def fill_empty_arrays(data):
        for i in range(1, len(sorted_dates)):
            current_date = sorted_dates[i].strftime(date_format)
            if not data[current_date]:
                prev_non_empty = None
                for j in range(i - 1, -1, -1):
                    if data[sorted_dates[j].strftime(date_format)]:
                        prev_non_empty = sorted_dates[j]
                        break

                next_non_empty = None
                for j in range(i + 1, len(sorted_dates)):
                    if data[sorted_dates[j].strftime(date_format)]:
                        next_non_empty = sorted_dates[j]
                        break

                if prev_non_empty and next_non_empty:
                    delta = (data[next_non_empty.strftime(date_format)][0] - data[prev_non_empty.strftime(date_format)][0]) / (
                            (next_non_empty - prev_non_empty).days or 1)
                    data[current_date] = [
                        data[prev_non_empty.strftime(date_format)][0] + delta * (sorted_dates[i] - prev_non_empty).days]

    json_data = full_date(json_data)
    date_format = "%d.%m.%y"
    dates = [datetime.strptime(date, date_format) for date in json_data.keys()]

    sorted_dates = sorted(dates)

    sorted_data = {date.strftime(date_format): json_data[date.strftime(date_format)] for date in sorted_dates}

    fill_empty_arrays(sorted_data)

    return sorted_data

with open('json', 'r', encoding='utf-8') as file:
    json_data = fuller(json.load(file))

print(json_data)
arr = [] 
for i in json_data:
    arr.append(json_data[i][0])

indices = np.arange(len(arr))
coefficients = np.polyfit(indices, arr, 1)
regression_line = np.polyval(coefficients, indices)
plt.figure(figsize=(12, 7))
plt.plot(indices, regression_line, label='линия регрессии', color='gray', linewidth=1.5, alpha=0.75)
plt.plot(arr, label='average weight', color='red', linestyle='--', linewidth=1)

plt.legend()

plt.title('Графики sin(x) и cos(x)')
plt.xlabel('x')
plt.ylabel('y')

plt.grid(True)
plt.savefig(PATH, dpi=250)
plt.show()
