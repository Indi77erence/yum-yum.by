from math import pi

col = int(input("Введите кол-во пицц: "))
d = int(input('Введите диаметр пицц: '))
s_1 = (pi * (d/2)*2) * col
d_2 = int(input("Введите диаметр пиццы: "))
s_2 = (pi * (d_2 / 2) * 2)
if s_2 > s_1:
    print(f"Лучше взять {col} пицц(ы) по {d}, чем одну диаметром {d_2}")
else:
    print(f"Лучше взять одну пиццу диаметром {d_2}, чем {col} пицц(ы) диаметром {d}")
