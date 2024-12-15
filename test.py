from sqlmodel import Session, select
from db import engine, SQLModel
from models import *
from readexcel import readstudnts
from readfacultycsv import readFaculty



SQLModel.metadata.create_all(engine)

            
            
            
    
# with Session(engine) as session:
#     query = select(Group).where(Group.no == 1)
#     queryres = session.exec(query)
        
#     for res in queryres:       
#         for s in res.students: 
#             print(f"\n{s}\n")

with Session(engine) as session:
    
    # query = select(Student,Group)
    query = select(Student,Group).join(StudentGroupLink, StudentGroupLink.student_id == Student.id).join(Group, Group.id == StudentGroupLink.group_id)
    queryres = session.exec(query)    
    # queryres.S
    i=0
    for S,G in queryres:       
        i+=1
        print(f"\n{i}\n{S}\t{G}\n")
        # for s in res.students: 
        #     print(f"\n{s}\n")
    