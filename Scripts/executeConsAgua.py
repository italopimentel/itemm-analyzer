from Scripts.getCapacidadeNominal import capacidadeNominal
import os
import pandas as pd

__path = os.getcwd()

#Os dados de peso não são oferecidos no arquivo CSV, por isso criei um array para especificar esse valor para cada protótipo
dataFramepd = {}
dataFramepd['Consumo de água 60°C'] = ["Peso Inicial (g)", "Fase (0d - 21d)", "Peso (g)", "Wc 21d [g/Ah]"]
dataProt = [[0.7680,0.762],[0.7770,0.770],[0.7700,0.764],[0.7600,0.754]]

#adiciona um protótipo no data frame
def addToDataFrame(dataFrame,protName, pesoInicial, peso, cpValue):
    dataFrame[protName] = [pesoInicial, '+21dias', peso, round(((pesoInicial-peso)/cpValue)*1000, 3)]

#adiciona valores no dataFrame
i = 0
for planilha in os.listdir(__path + "/Sheets/"):
    if planilha.endswith(".csv") == True:
        prototypeName, cpValue = capacidadeNominal(planilha)
        addToDataFrame(dataFrame=dataFramepd, protName=prototypeName, pesoInicial=dataProt[i][0], 
                       peso=dataProt[i][1], cpValue=cpValue)
        i += 1

def getDataframeValue():
    return dataFramepd
