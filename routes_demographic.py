from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

import baseModels
import models
from dependencies import get_db, oauth2_scheme

routerDemo = APIRouter()

@routerDemo.post("/demographics/", response_model=baseModels.DemographicCreate)
def create_demographic(demographic: baseModels.DemographicCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    new_demographic = models.Demographic(birth_rate=demographic.birth_rate, death_rate=demographic.death_rate, population=demographic.population, id_city=demographic.id_city)
    db.add(new_demographic)
    db.commit()
    db.refresh(new_demographic)
    return new_demographic

@routerDemo.get("/demographics/", response_model=list[baseModels.DemographicCreate])
async def get_demographics(db: Session = Depends(get_db),
                           skip: int = Query(0, ge=0),
                           limit: int = Query(10, gt=0),
                           id_city: int = Query(None),
                           sort_by: str = Query("population"),
                           sort_order: str = Query("asc"),
                           token: str = Depends(oauth2_scheme)
                           ):
    query = db.query(models.Demographic)

    if id_city:
        query = query.filter(models.Demographic.id_city == id_city)

    if sort_order == "desc":
        query = query.order_by(getattr(models.Demographic, sort_by).desc())
    else:
        query = query.order_by(getattr(models.Demographic, sort_by))

    return query.offset(skip).limit(limit).all()

@routerDemo.get("/demographics/{demographic_id}/", response_model=baseModels.DemographicCreate)
async def get_demographic(demographic_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    demographic = db.query(models.Demographic).filter(models.Demographic.id == demographic_id).first()
    if demographic is None:
        raise HTTPException(status_code=404, detail="Demographic not found")
    return demographic

@routerDemo.delete("/demographics/{demographic_id}/")
async def delete_demographic(demographic_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    demographic = db.query(models.Demographic).filter(models.Demographic.id == demographic_id).first()
    if demographic is None:
        raise HTTPException(status_code=404, detail="Demographic not found")
    db.delete(demographic)
    db.commit()
    return {"message":"ok"}

@routerDemo.put("/demographics/{demographic_id}/", response_model=baseModels.DemographicCreate)
async def update_demographic(demographic_id:int, demographic_data: baseModels.DemographicCreate,
                          db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    demographic = db.query(models.Demographic).filter(models.Demographic.id == demographic_id).first()
    if demographic is None:
        raise HTTPException(status_code=404, detail="Demographic not found")
    demographic.birth_rate = demographic_data.birth_rate
    demographic.death_rate = demographic_data.death_rate
    demographic.population = demographic_data.population
    demographic.id_city = demographic_data.id_city
    db.commit()
    return demographic