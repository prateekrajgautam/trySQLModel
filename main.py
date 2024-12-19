import os
import subprocess
from sqlmodel import Session, select
from db import engine, SQLModel
from models import *
from readexcel import readstudnts
from readfacultycsv import readFaculty

import pandas as pd
import uvicorn
from fastapi import FastAPI,Request,Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import HTTPException,Header

from readResult import readResult
PORT = 9001
templates = Jinja2Templates(directory="./templates")
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
SQLModel.metadata.create_all(engine)
def createTable():
    pass
    
    
softdf = readResult("./SoftComputing Marks.xlsx")
pydf = readResult("./Python Marks.xlsx")
print(softdf)  
print(pydf)
# input("")




def readandupdatestudents():
    studentDataList,groups = readstudnts()  
    with Session(engine) as session:
        for s in studentDataList:
            print(s)
            try:
                session.add(Student(**s))
                session.commit()
            except Exception as e:
                # print(e)
                session.rollback()
                
def updateGroups():
    studentDataList,groups = readstudnts()  
    with Session(engine) as session:
        for g in groups:
            print(g)
            try:
                session.add(Group(**g))
                session.commit()
            except Exception as e:
                # print(e)
                session.rollback()
    
    
def updatestudentgrouplink():
    with Session(engine) as session:
    
        queryres = session.exec(select(Group))
        
        for g in queryres:
            
            
            queryres2 = session.exec(select(Student).where(Student.groupno == g.id))
            for res in queryres2:
                print(res)
                studentgrouplink = dict(student_id = res.id, group_id = g.id)
                
                try:
                    session.add(StudentGroupLink(**studentgrouplink))
                    session.commit()
                except Exception as e:
                    print(e)
                    session.rollback()
                # session.refresh(Student)
                # session.refresh(Group)
    
def readandupdatefaculty():
    facultDataList = readFaculty()
    with Session(engine) as session:
        for f in facultDataList:
            print(f)
            try:
                session.add(Faculty(**f))
                session.commit()
            except Exception as e:
                # print(e)
                session.rollback()
                
            
            
    

            
        
def getacdata(sapid):
    print(sapid)
    with Session(engine) as session:
        query = select(Student,Group).join(StudentGroupLink, StudentGroupLink.student_id == Student.id).join(Group, Group.id == StudentGroupLink.group_id).where(Student.sapid == sapid)
        G=""
        S,G= session.exec(query).one()
        # print(S.groups)
        print(G.students)
        # groups = session.exec(select(Student)) 
        # print(groups)
    # print(queryres)
    return S,G
        
        
        
def readData():
    readandupdatefaculty()
    readandupdatestudents()
    updateGroups()
    updatestudentgrouplink()
        
        
        
        
@app.get("/")
def getroot():
    return dict(hi="hi")


@app.get("/id")
def getroot():
    return HTMLResponse("HTMLResponse")


@app.get("/ac/", response_class=HTMLResponse)
def getdetails(request:Request):
    rend = templates.TemplateResponse(
        "index.html", {"request": request, "title": "Home", "content": "Welcome to FastAPI with Jinja2 Templates!"}
    )
    return rend

@app.get("/ac/{sapid}")
def getdetails(sapid:int):
    print(sapid)
    S,G = getacdata(sapid)
    
    return dict(Student=S,Group=G,Team=G.students)    

@app.get("/api/marks/{subject}/{sapid}")
def getmarks(subject:str, sapid:int):
    print(type(sapid))
    
    if "python" in subject.lower():
        print("python")
        df = pydf
    if "soft" in subject.lower():
        print("soft")
        df = softdf
    try:
        row = df[df["Student Id"]==sapid]
    # print(df["Student Id"])
    except:
        row={"not found"}
    
    print(subject,sapid)
    return dict(res=row)



if __name__ == "__main__":
    createTable()
    readData()
    # os.system(f"tailscale funnel {PORT}")
    uvicorn.run("main:app", host='0.0.0.0',port=PORT, reload=True)
    
    
    