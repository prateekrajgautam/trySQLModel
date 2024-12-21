import pandas as pd

def readResult(filename):

    dfdict = pd.read_excel(filename,engine="openpyxl",sheet_name=None)

    try:
        ia=dfdict["IA"][["Student Id","IA(100)","IA(50)"]]
        mid=dfdict["MID"][["Student Id","MID(100)","MID(20)"]]
        end=dfdict["END"][["Student Id","END(100)","END(30)"]]
    except Exception as e:
        # print(e)
        pass

    for df in [ia, mid, end]:
            if df.index.name == "Student Id":
                df.reset_index(inplace=True)
    res = pd.merge(mid, ia, on="Student Id", how="outer")
    res = pd.merge(res, end, on="Student Id", how="outer")

    res.fillna(0, inplace=True)
    # print(res)
    # print(res["MID(20),IA(50),END(30)".split(",")])
    res["Total (100)"] = res["MID(20),IA(50),END(30)".split(",")].replace("A",0).sum(axis=1)


    return res

if __name__=="__main__":
    filename="Python Marks.xlsx"
    filename="SoftComputing Marks.xlsx"
    df=readResult(filename)
    # print(df.shape)
    # print(df.head())
    
    df


