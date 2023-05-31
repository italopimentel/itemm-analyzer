#script dedicada a geração das estatisticas da página showresults

import pandas as pd
from os import getcwd as path

class DataAnalist():

    def __init__(self, planilha):
        self.__dataDF = pd.read_excel(path + "/Results/" + planilha)
    
    def processData(self):
        print(self.__dataDF)
