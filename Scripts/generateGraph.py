protValues_V = [1.421, 1.272, 1.272, 1.325]
protNames_V = ['Am 03', 'Am 05', 'Am 07', 'Am 08']

def generateComparationGraph (protValues, protNames):
    import matplotlib.pyplot as plt
    import numpy as np
    import os

    path = os.getcwd() + '/Results/plot_comparacao.png'

    bars_width = 0.5
    pos_bars = range(len(protValues))
    bars_color = ['red', 'blue', 'green', 'orange']

    plt.bar(pos_bars, protValues, bars_width, color=bars_color)
    plt.ylabel('Valores WC')
    plt.title('Gráfico de comparação entre valores de WC')

    plt.xticks(pos_bars, protNames)
    ytick = np.arange(0, max(protValues) + 0.4, 0.2)
    plt.yticks(ytick)

    for i, valor in enumerate(protValues):
        plt.text(i, valor + 0.05, str(valor), ha='center')

    plt.savefig(path)
