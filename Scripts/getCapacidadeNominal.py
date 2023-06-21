import os
import pandas as pd

__path = os.getcwd()

def capacidadeNominal(arqName):
    try:    
        CSV_Equalizacao = pd.read_csv(__path + "/Sheets/" + arqName, sep=";", on_bad_lines='skip', encoding='utf')
    except UnicodeDecodeError:
        CSV_Equalizacao = pd.read_csv(__path + "/Sheets/" + arqName, sep=";", on_bad_lines='skip', encoding= "ISO-8859-1")

    lastStepValues = {}

    for line in range(0, len(CSV_Equalizacao['Step'])):
        try:
            currentStepLine = CSV_Equalizacao['Step'][line]
            nextStepLine = CSV_Equalizacao['Step'][line + 1]
            try:
                if nextStepLine != currentStepLine:
                    if  str(CSV_Equalizacao['AhAccu'][line]) == 'nan':
                        lineDesired = line - 1
                        while str(CSV_Equalizacao['AhAccu'][lineDesired]) == 'nan':
                            lineDesired -= 1   
                        lastStepValues[f'{currentStepLine}'] = abs(float(str(CSV_Equalizacao['AhAccu'][lineDesired]).replace(',','.')))
                    else:
                        lastStepValues[f'{currentStepLine}'] = abs(float(str(CSV_Equalizacao['AhAccu'][line]).replace(',','.')))
            except:
                pass
        except KeyError: 2902

    valueDesired = max(lastStepValues.values())
    prototypeName = arqName.replace("Equalização_C20_", "")
    prototypeName = prototypeName.replace(".csv", "")
    
    return prototypeName, valueDesired