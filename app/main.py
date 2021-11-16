from fastapi import FastAPI, status, Depends, HTTPException

from . import models
from . import schemas

from .database import engine, get_db
from sqlalchemy.orm import Session


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def read_root():
  return {"Welcome to Medicine Intake API. Visit '/docs' for more info on api"}


# Get all med info
@app.get("/medInfo")
def get_medInfo(db: Session = Depends(get_db)):
  meds = db.query(models.MedInfo).all()
  return {"result": meds}


# add meds
@app.post("/medInfo", status_code=status.HTTP_201_CREATED)
def post_medInfo(info:schemas.MedInfo, db: Session = Depends(get_db)):
  new_med =  models.MedInfo(
    name= info.name.lower(),
    time= info.time,
    start_date= info.start_date,
    end_date= info.end_date,
    quantity= info.quantity,
    medType= info.medType
  )

  db.add(new_med)
  db.commit()
  db.refresh(new_med)

  return {"med info": new_med}


# Get med info by date
@app.get('/medInfo/date/{date}')
def get_medInfoByDate(date, db: Session = Depends(get_db)):
    med = db.query(models.MedInfo).filter(models.MedInfo.start_date <= date, models.MedInfo.end_date >= date).all()

    name=[]

    for m in med:
      name.append(m.name)

    taken = db.query(models.MedsTaken).all()
    taken_meds = [m for m in taken if m.name in name]

    if not med:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Medicines with date: {date} were not found')
    return {"meds": med, "meds_taken": taken_meds}


# get med info by name
@app.get("/medInfo/name/{name}")
def get_medInfoById(name, db: Session = Depends(get_db)):
    med = db.query(models.MedInfo).filter(models.MedInfo.name == name).first()

    if not med:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Medicine with name: {name} were not found')
    return med


# add the mades taken
@app.post('/medInfo/taken')
def post_medTaken(info:schemas.MedTaken, db: Session = Depends(get_db)):
  medTaken = models.IntakeSchedule(
    name = info.name.lower(),
    date_taken = info.date_taken
  )

  db.add(medTaken)
  db.commit()
  db.refresh(medTaken)

  return medTaken
