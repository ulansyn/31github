def adder(message):
    with open('МОЙВЕС.txt', 'a') as file:
       file.write(f'\n{message}')

def remover():
    with open('МОЙВЕС.txt', 'r') as file:
        lines = file.readlines()
    if lines:
        lines.pop()
        with open('МОЙВЕС.txt', 'w') as file:
            file.writelines(lines)

def last_value():
    with open('МОЙВЕС.txt', 'r') as file:
        lines = file.readlines()
    if lines:
        last_line = lines[-1]
        return last_line.strip()

def is_valid_number(text):
    text = text.replace(',', '.')
    try:
        number = float(text)
        if 60 <= number <= 85:
            return True
    except ValueError:
        pass
    return False
def get_all_values():
    with open('МОЙВЕС.txt', 'r') as file:
        lines = file.readlines()

    values = []
    for line in lines:
        value = line.strip()
        if is_valid_number(value):
            values.append(float(value))
    new_s = ""
    for i in range(len(values)):
        new_s += str(i + 1) + '. ' + str(values[i]) + '\n'
    return new_s
