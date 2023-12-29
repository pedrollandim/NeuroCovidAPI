import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

# Lista de offsets
offsets = [
    [(196.0, 83.0), (240.0, 162.0), (188.0, 203.0), (160.0, 139.0)],
    [(37.0, 156.0), (129.0, 185.0), (81.0, 258.0), (31.0, 220.0), (32.0, 185.0)]
]

# Criar uma figura
fig, ax = plt.subplots()

# Desenhar os polígonos com base nos offsets
for offset_list in offsets:
    polygon = Polygon(offset_list, closed=True, edgecolor='b', fill=None)
    ax.add_patch(polygon)

# Ajustar os limites do eixo para mostrar todos os polígonos
ax.autoscale()

# Exibir o gráfico
plt.show()
