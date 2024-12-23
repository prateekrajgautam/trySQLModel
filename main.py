import os
import subprocess
# from sqlmodel import Session, select
# from db import engine, SQLModel
# from models import *
from readexcel import readstudnts
from readfacultycsv import readFaculty
from multiprocessing import Process


import pandas as pd
import uvicorn
from fastapi import FastAPI,Request,Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import HTTPException,Header


from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8001",
    "https://dell-i7.tail9f300.ts.net",
    "http://dell-i7.tail9f300.ts.net",
    "upessocs.github.io",
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import logging
from logging.config import dictConfig

# Create and configure logger
logging.basicConfig(filename="newfile.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')

# Creating an object
logger = logging.getLogger()

# Setting the threshold of logger to DEBUG
logger.setLevel(logging.DEBUG)

# Test messages
logger.debug("Harmless debug Message")

PORT = 10000

# Define logging configuration
dictConfig({
    "version": 1,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        }
    },
    "handlers": {
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": os.path.join(os.getcwd(), "log.txt"),
            "formatter": "default",
        },
    },
    "root": {
        "level": "DEBUG",
        "handlers": ["file"],
    },
})


from readResult import readResult
from readAC import readAC
PORT = 8000

templates = Jinja2Templates(directory="./templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
# SQLModel.metadata.create_all(engine)
# def createTable():
#     pass
    
    
softdf = readResult("./SoftComputing Marks.xlsx")
pydf = readResult("./Python Marks.xlsx")

majordf = readAC("./001 AC Summary SheetCCVT B4,5,6.xlsx")
# print(softdf)  
# print(pydf)
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
    logger.debug(f"{subject} {sapid}")
    
    if "python" in subject.lower():
        print("python")
        df = pydf
    if "soft" in subject.lower():
        print("soft")
        df = softdf
    if "major" in subject.lower():
        print("Major")
        df = majordf
    
    try:
        row = df[df["Student Id"]==sapid]
    # print(df["Student Id"])
    except:
        row = df[df["SapID"]==sapid]
    else:
        row={"not found"}
    
    print(subject,sapid)
    resp = row.to_dict(orient="records")[0]
    print(resp)
    return resp


def startTailscaleFunnel():
    subprocess.run(["tailscale", "funnel", f"{PORT}"])

def startServer():
    uvicorn.run("main:app", host='127.0.0.1',port=PORT, reload=True,log_config=None)    

    
if __name__ == "__main__":
    logfile = os.path.join(os.path.dirname(os.getcwd()),"log.txt")
    p1 = Process(target=startTailscaleFunnel)
    p2 = Process(target=startServer)
    # readData()
    p1.start()
    # p1.join()
    p2.start()
    # p2.join()
    
    
    