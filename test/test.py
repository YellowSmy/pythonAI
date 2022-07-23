import pandas as pd
import numpy as np
import matplotlib

excel_url = 'C:/Users/user/Desktop/pythonAI/waferFail/excelFile/wafer_test_sheet_test.xlsx'

DF = pd.read_excel(excel_url, sheet_name=None);

sheetName = list(DF.keys()); #dict(keys) to list
sheetSize = len(sheetName);

yieldLimit = float(input()); #pass limitation set

#최종 결과물 save array
waferResult = np.zeros((sheetSize, 2));
waferYield = np.zeros(sheetSize)

#시트 수만큼 데이터 후처리
for sheetCount in range(sheetSize):
    selectDF = DF[sheetName[sheetCount]];


    #빈도수 data import
    processData = pd.Series(selectDF.values.flatten());
    waferSize = processData.count(); #wafer Size check

    valueCount = processData.value_counts();
    indexLen= len(valueCount); #valueCount size check for create list


    #list transport 
    valueList = np.zeros((2, indexLen), dtype=float); 

    index = valueCount.index.tolist();
    values = valueCount.values.tolist();

    for countI in range(indexLen):
        valueList[0, countI] = index[countI];
        valueList[1, countI] = values[countI];


    #수율 기준 pass/fail chip indicate
    passChip=0; failChip = 0;
    for countJ in range(indexLen):
        if(valueList[0, countJ] >= yieldLimit): 
            passChip += valueList[1, countJ]; 
        else:
            failChip += valueList[1, countJ];

    waferResult[sheetCount, 0] = passChip;
    waferResult[sheetCount, 1] = failChip;
    
    #yield caculate
    waferYield[sheetCount] = round((passChip / waferSize) * 100) # yield 공식, 소수점 첫째자리 반올림


#graph
print(waferResult)
print(waferYield);
print(type(waferSize))
#valueList = [[0 for countX in range(indexLen)] for countY in range(2)] #classical python list 
