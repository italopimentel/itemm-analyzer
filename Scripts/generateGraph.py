protValues_V = [1.421, 1.272, 1.272, 1.325]
protNames_V = ['Am 03', 'Am 05', 'Am 07', 'Am 08']

def generateComparationGraph (protValues, protNames):
    import matplotlib.pyplot as plt
    import numpy as np
    import os

    path = os.getcwd() + '/static/plot_comparacao.png'

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
    plt.cla()
    plt.clf()

def generateErrorGraph(protValues):
    import matplotlib.pyplot as plt
    import numpy as np
    import os

    arrayResults = np.array(protValues)
    media = np.mean(arrayResults)
    variancia = np.var(arrayResults)
    path = os.getcwd() + '/static/plot_erro.png'

    ytick = np.arange(min(protValues) - 0.02, max(protValues) + 0.02, 0.05)
    plt.boxplot(arrayResults, patch_artist=True, boxprops={'facecolor': 'green'}, medianprops={'color': 'blue'})
    plt.title('Gráfico de vela WC')
    plt.ylabel('Valores WC')
    plt.yticks(ytick)
    plt.savefig(path)

    plt.cla()
    plt.clf()

    return media, variancia
