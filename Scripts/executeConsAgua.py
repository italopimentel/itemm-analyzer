from Scripts.getCapacidadeNominal import capacidadeNominal
import os
import pandas as pd


class ResultadoDF():

    def __init__(self):
        self.dataFramepd = {}
        self.dataFramepd['Consumo de água 60°C'] = ["Peso Inicial (g)", "Fase (0d - 21d)", "Peso (g)", "Wc 21d [g/Ah]"]
        self.dataProt = [[0.7680,0.762],[0.7770,0.770],[0.7700,0.764],[0.7600,0.754]]

    #adiciona um protótipo no data frame
    def addToDataFrame(self, protName, pesoInicial, peso, cpValue):
        self.dataFramepd[protName] = [pesoInicial, '+21dias', peso, round(((pesoInicial-peso)/cpValue)*1000, 3)]

    def calculateCP(self, planilha_path):
        return capacidadeNominal(planilha_path)

    def getDataframeValue(self):
        return self.dataFramepd
