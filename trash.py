# Перевод географических координат (широты и долготы) точки в прямоугольные
# координаты проекции Гаусса-Крюгера (на примере координат Москвы).

# Географические координаты точки (в градусах)
dLon = 56.84237923987836  # Долгота (положительная для восточного полушария)
dLat = 60.61476116648328  # Широта (положительная для северного полушария)

# Номер зоны Гаусса-Крюгера (если точка рассматривается в системе
# координат соседней зоны, то номер зоны следует присвоить вручную)
zone = int(dLon / 6.0 + 1)

# Импорт математических функций
from math import sin, cos, tan, pi
import math
import pymap3d as pm

# def convert(dLon, dLat):
#     # Параметры эллипсоида Красовского
#     a = 6378245.0  # Большая (экваториальная) полуось
#     b = 6356863.019  # Малая (полярная) полуось
#     e2 = (a ** 2 - b ** 2) / a ** 2  # Эксцентриситет
#     n = (a - b) / (a + b)  # Приплюснутость
#
#     # Параметры зоны Гаусса-Крюгера
#     F = 1.0  # Масштабный коэффициент
#     Lat0 = 0.0  # Начальная параллель (в радианах)
#     Lon0 = (zone * 6 - 3) * pi / 180  # Центральный меридиан (в радианах)
#     N0 = 0.0  # Условное северное смещение для начальной параллели
#     E0 = zone * 1e6 + 500000.0  # Условное восточное смещение для центрального меридиана
#
#     # Перевод широты и долготы в радианы
#     Lat = dLat * pi / 180.0
#     Lon = dLon * pi / 180.0
#
#     # Вычисление переменных для преобразования
#     v = a * F * (1 - e2 * (sin(Lat) ** 2)) ** -0.5
#     p = a * F * (1 - e2) * (1 - e2 * (sin(Lat) ** 2)) ** -1.5
#     n2 = v / p - 1
#     M1 = (1 + n + 5.0 / 4.0 * n ** 2 + 5.0 / 4.0 * n ** 3) * (Lat - Lat0)
#     M2 = (3 * n + 3 * n ** 2 + 21.0 / 8.0 * n ** 3) * sin(Lat - Lat0) * cos(
#         Lat + Lat0)
#     M3 = (15.0 / 8.0 * n ** 2 + 15.0 / 8.0 * n ** 3) * sin(
#         2 * (Lat - Lat0)) * cos(
#         2 * (Lat + Lat0))
#     M4 = 35.0 / 24.0 * n ** 3 * sin(3 * (Lat - Lat0)) * cos(3 * (Lat + Lat0))
#     M = b * F * (M1 - M2 + M3 - M4)
#     I = M + N0
#     II = v / 2 * sin(Lat) * cos(Lat)
#     III = v / 24 * sin(Lat) * (cos(Lat)) ** 3 * (5 - (tan(Lat) ** 2) + 9 * n2)
#     IIIA = v / 720 * sin(Lat) * (cos(Lat) ** 5) * (
#             61 - 58 * (tan(Lat) ** 2) + (tan(Lat) ** 4))
#     IV = v * cos(Lat)
#     V = v / 6 * (cos(Lat) ** 3) * (v / p - (tan(Lat) ** 2))
#     VI = v / 120 * (cos(Lat) ** 5) * (
#             5 - 18 * (tan(Lat) ** 2) + (tan(Lat) ** 4) + 14 * n2 - 58 * (
#             tan(Lat) ** 2) * n2)
#
#     # Вычисление северного и восточного смещения (в метрах)
#     N = I + II * (Lon - Lon0) ** 2 + III * (Lon - Lon0) ** 4 + IIIA * (
#             Lon - Lon0) ** 6
#     E = E0 + IV * (Lon - Lon0) + V * (Lon - Lon0) ** 3 + VI * (Lon - Lon0) ** 5
#
#     print('Широта:            ', dLat)
#     print('Долгота:           ', dLon)
#     print('Северное смещение: ', N)
#     print('Восточное смещение:', E)
#     return N, E

fLon = 56.84197506786994
fLan = 60.583945999999976
sLon = 56.841679067869194
sLan = 60.6149465
a = pm.geodetic2enu(fLon, fLan, 0, sLon, sLan, 0)
print(math.sqrt(a[0] ** 2 + a[1] ** 2))
