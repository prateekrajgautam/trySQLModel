import pandas as pd

def readResult(filename):

    pydfdict = pd.read_excel(filename,engine="openpyxl",sheet_name=None)

    # pyia=pydfdict["PythonIA"][["Student Id","IA(100)"]].reset_index(drop=True).set_index("Student Id")
    # pymid=pydfdict["PythonMID"][["Student Id","Mid(100)"]].reset_index(drop=True).set_index("Student Id")
    # pyend=pydfdict["PythonEND"][["Student Id","END(100)"]].reset_index(drop=True).set_index("Student Id")


    pyia=pydfdict["PythonIA"][["Student Id","IA(100)"]].reset_index(drop=True)
    pymid=pydfdict["PythonMID"][["Student Id","Mid(100)"]].reset_index(drop=True)
    pyend=pydfdict["PythonEND"][["Student Id","END(100)"]].reset_index(drop=True)



    pyres=pd.concat([pymid,pyia,pyend],axis=1)

    pyres
    return pyres

if __name__=="__main__":
    filename="Python Marks.xlsx"
    df=readResult(filename)
    print(df.head())

