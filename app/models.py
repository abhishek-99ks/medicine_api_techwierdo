from sqlalchemy import Column, Integer,String, Date, Time
from .database import Base


class MedInfo(Base):
  __tablename__ = "medInfo"

  id = Column(Integer, primary_key=True, nullable=False)
  name = Column(String, nullable=False)
  time = Column(Time, nullable=False)
  start_date = Column(Date, nullable=False)
  end_date = Column(Date, nullable=False)
  quantity = Column(Integer, nullable=False)
  medType = Column(String, nullable=False)

class MedsTaken(Base):
  __tablename__ = "medsTaken"
  id = Column(Integer, primary_key=True, nullable=False)
  name = Column(String, nullable=False)
  date_taken = Column(Date, nullable=False)
  