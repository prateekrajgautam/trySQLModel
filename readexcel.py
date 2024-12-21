import pandas as pd
from models import *


# print(dataDict)
def readstudnts():
    df = 0
    for sheetname,df in dataDict.items():
        print(sheetname)
        if sheetname == "Total":
            break
            
            

    print(df.head())    

    studentDataList = []
    groups=[]
    for i in range(0,df.shape[0]):
        series = df.loc[i]
        # print(series.at["SAP ID"])
        group = dict(no = series.at["Group No"],title= series.at["Group Title"])
        student = {
            "sapid" : int(series.at["SAP ID"]),
            "name" : series.at["Name"],
            "fname":  series.at["Name"].split(" ")[0],
            "lname": series.at["Name"].split(" ")[-1] if len(series.at["Name"].split(" "))>1   else None,
            "batch": series.at["Batch Number"],
            "email": series.at["Email ID"],
            "groupno": series.at["Group No"]
            # "grouptitle": series.at["Group Title"]
        }
        
        group = dict(no = series.at["Group No"],title= series.at["Group Title"])
        groups.append(group)
        studentDataList.append(student)
        # print(student)
        
    return studentDataList,groups
    
if __name__ == "__main__":
    filename = "./data.xlsx"
    dataDict = pd.read_excel(filename, engine="openpyxl",sheet_name=None)

    studentDataList = readstudnts()


