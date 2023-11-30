import math
import matplotlib.pyplot as plt

def input_initial_values(input_invite, type='float'):
    while True:
        value = input(input_invite)
        try:
            if ',' in value: value = value.replace(',', '.')
            if type == 'int':
                value = int(value)
            else:
                value = float(value)
            break
        except ValueError:
            print('Не понял')
    return value


def change_parameters(i, speed_coeff=1):
    a.append(-g + f_drag(v[i]) / mass)
    v.append(speed_coeff * v[i] + a[i] * dt)
    y.append(y[i] + v[i] * dt + (a[i]) * dt ** 2 / 2)
    t.append(t[i] + dt)


def relative_error(v):
    return abs((v_theoretical - v)) * 100 / v_theoretical


def is_in_peak():
    return (v[-1] == v[0] or v[-1] <= 0) and (y[-1] > 0)


def is_on_the_ground():
    return y[-1] <= 0


def is_at_the_ceiling():
    return ceiling_height != 0 and y[-1] >= ceiling_height


def fall():
    i = len(v) - 1
    while y[i] >= 0:
        change_parameters(i)
        i += 1


def rebound():
    change_parameters(-1, -1)
    i = len(v) - 1

    if ceiling_height != 0:
        while v[i] >= 0 and y[i] <= ceiling_height:
            change_parameters(i)
            i += 1
    else:
        while v[i] >= 0:
            change_parameters(i)
            i += 1


def f_drag(velocity):
    return -rho * C * S * abs(velocity) * velocity / 2

rho = 1.23  # kg / m**3
g = 9.81  # m/s**2
C = 0.4
t = [0]  # s
dt = 0.001  # s

print('Вас приветствует программа, моделирующая падение мяча с опредленной высоты. \nПожалуйста, введите требуемые данные..')
mass = input_initial_values('Масса шара (кг) = ')
radius = input_initial_values('Радиус шара (м) = ')
height = input_initial_values('Высота падения (м) = ')
v_init = input_initial_values('Начальная скорость (м / с) = ')
bounces = input_initial_values('Введите количество рассматриваемых отскоков после падения = ', 'int')
ceiling_height = input_initial_values('На какой высоте расположить потолок (м). (Если потолок не нужен введите 0) = ', 'int')
bounces_count = 0

S = math.pi * radius ** 2
v_theoretical = math.sqrt((2 * mass * g) / (rho * C * S))  # When the gravity force equals to the drag force
v = [-v_init]
y = [height]
a = [-g + f_drag(v[0]) / mass]

while True:
    if is_in_peak():
        fall()

    if bounces != 0 and is_on_the_ground():
        bounces_count += 1
        rebound()
    else:
        break

    if ceiling_height != 0 and is_at_the_ceiling():
        rebound()
    if bounces_count == bounces:
        break

v = list(map(abs, v))
a = list(map(abs, a))

for i in range(1, len(v)):
    if v[i] == v[i - 1] == v[i + 1]:
        print(f'Установившаяся скорость = {v[i]:.4f} м/c')
        print(f'Теоретическая установившаяся скорость = {v_theoretical:.4f} м/c')
        if relative_error(v[i]) <= 0.1:
            print(f'Относительная погрешность меньше 0.1%')
            print(f'Значения совпадают')
            break
        else:
            print(f'Относительная погрешность равна {relative_error(v[i]):.4f} %')
            break
else:
    print('Шар не достиг установившейся скорости')

figure = plt.figure(figsize=(12, 6))
axis = figure.subplots(1, 3)

axis[0].plot(t, v)
axis[0].set_title("v(t)")

axis[1].plot(t, a)
axis[1].set_title("a(t)")

axis[2].plot(t, y)
axis[2].set_title("y(t)")

plt.show()

input()


