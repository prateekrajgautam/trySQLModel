import pandas as pd 
import numpy as np
def readFaculty():

    facultydf = pd.read_csv("./facultycontacts.csv")
    facultyDataList = []
    for i in range(0,facultydf.shape[0]):
        fseries = facultydf.loc[i]
        contact2 = [c for c in [fseries.at["Home Phone"],fseries.at["Mobile Phone"],fseries.at["Business Phone"]] if not np.isnan(c) ]
        contact = None if len(contact2) == 0 else int(contact2[0])

        print(contact)
        faculty = {
            # "name" : fseries.at["First Name"] + " " if fseries.at["Middle Name"] == "" else f" {fseries.at['Middle Name']} "  + fseries.at["Last Name"] ,
            "name" : f'{fseries.at["First Name"]} {fseries.at["Middle Name"] if fseries.at["Middle Name"] != "" else "" }{fseries.at["Last Name"]}' ,
            "fname" : fseries.at["First Name"],
            "email" : fseries.at["E-mail Address"],
            "contact" : contact    
        }
        facultyDataList.append(faculty)
    return facultyDataList
        
if __name__ == "__main__":
    facultyDataList= readFaculty()