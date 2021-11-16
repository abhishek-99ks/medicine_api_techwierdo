from pydantic import BaseModel
from datetime import date, time


class MedInfo(BaseModel):
  name: str
  time: time
  start_date: date
  end_date: date
  quantity: int
  medType: str

class MedTaken(BaseModel):
  name: str
  date_taken: date