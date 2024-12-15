from typing import Optional

from sqlmodel import SQLModel, Field, Column, Relationship, col

class StudentGroupLink(SQLModel, table= True):
    __tablename__ = "studentgrouplink"
    student_id: int = Field(default=None, foreign_key="student.id", primary_key=True)
    group_id: int = Field(default=None, foreign_key="group.id", primary_key=True)

# class AcGroupLink(SQLModel, table= True):
#     __tablename__ = "acgrouplink"
#     ac_id: int = Field(default=None, foreign_key="faculty.id", primary_key=True)
#     group_id: int = Field(default=None, foreign_key="group.id", primary_key=True)

# class MentorGroupLink(SQLModel, table= True):
#     __tablename__ = "mentorgrouplink"
#     mentor_id: int = Field(default=None, foreign_key="faculty.id", primary_key=True)
#     group_id: int = Field(default=None, foreign_key="group.id", primary_key=True)

# class PanelGroupLink(SQLModel, table= True):
#     __tablename__ = "panelgrouplink"
#     panel_id: int = Field(default=None, foreign_key="faculty.id", primary_key=True)
#     group_id: int = Field(default=None, foreign_key="group.id", primary_key=True)


class Student(SQLModel, table=True):
    __tablename__ = "student"
    id: Optional[int] = Field(default=None, primary_key=True)
    sapid: Optional[int] = Field(default=None, unique=True, index=True)
    name: str
    fname: str
    lname: Optional[str] = None
    batch: Optional[str] = None
    email: Optional[str] = None
    contact: Optional[int] = None
    groupno: Optional[int] =Field(default=None)
    groups: list["Group"] = Relationship(back_populates="students", link_model=StudentGroupLink)
    

class Group(SQLModel, table=True):
    __tablename__ = "group"
    id: Optional[int] = Field(default=None, primary_key=True)
    no: int = Field(index=True,unique=True)
    title: str
    students: list[Student] = Relationship(back_populates="groups", link_model=StudentGroupLink)
    # acs: Optional[int] = Relationship(back_populates="groups", link_model=AcGroupLink)
    # mentors: Optional[int] = Relationship( back_populates="groups", link_model=MentorGroupLink)
    # panels: Optional[list] = Relationship( back_populates="groups", link_model=PanelGroupLink)
    
    
class Faculty(SQLModel, table = True):
    __tablename__ = "faculty"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    fname: Optional[str] = None
    email: Optional[str] =  Field(unique=True)
    contact: Optional[int] = None
    # mentors: Optional[list] = Relationship(back_populates="faculty", link_model=MentorGroupLink)
    # panels: Optional[list] = Relationship(back_populates="faculty", link_model=PanelGroupLink)
    # acs: Optional[list] = Relationship(back_populates="faculty", link_model=AcGroupLink)
    
    

    