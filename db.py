# from typing import Optional
from sqlmodel import  SQLModel, create_engine


DATABASE_FILENAME = "./CCVT.db"
sqlite_url = f"sqlite:///{DATABASE_FILENAME}"

# engine = create_engine(sqlite_url, echo=True)
engine = create_engine(sqlite_url)


