from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

import baseModels
import models
from dependencies import get_db, oauth2_scheme

routerCity = APIRouter()

@routerCity.post("/cities/", response_model=baseModels.CityCreate)
def create_city(city: baseModels.CityCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    new_city = models.Cities(name=city.name, mayor_name=city.mayor_name, landmark_photo=city.landmark_photo, id_region=city.id_region)
    db.add(new_city)
    db.commit()
    db.refresh(new_city)
    return new_city

@routerCity.get("/cities/", response_model=list[baseModels.CityCreate])
async def get_cities(db: Session = Depends(get_db),
                     skip: int = Query(0, ge=0),
                     limit: int = Query(10, gt=0),
                     name: str = Query(None),
                     mayor_name: str = Query(None),
                     id_region: int = Query(None),
                     sort_by: str = Query("id_region"),
                     sort_order: str = Query("asc"),
                     token: str = Depends(oauth2_scheme)
                     ):
    query = db.query(models.Cities)
    if name:
        query = query.filter(models.Cities.name.ilike(f"%{name}%"))
    if mayor_name:
        query = query.filter(models.Cities.mayor_name.ilike(f"%{mayor_name}%"))
    if id_region:
        query = query.filter(models.Cities.id_region == id_region)

    if sort_order == "desc":
        query = query.order_by(getattr(models.Cities, sort_by).desc())
    else:
        query = query.order_by(getattr(models.Cities, sort_by))
    return query.offset(skip).limit(limit).all()

@routerCity.get("/cities/{city_id}/", response_model=baseModels.CityCreate)
async def get_city(city_id:int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    city = db.query(models.Cities).filter(models.Cities.id == city_id).first()
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return city

@routerCity.delete("/cities/{city_id}/")
async def delete_city(city_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    city = db.query(models.Cities).filter(models.Cities.id == city_id).first()
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    db.delete(city)
    db.commit()
    return {"message":"ok"}

@routerCity.put("/cities/{city_id}/", response_model=baseModels.CityCreate)
async def update_city(city_id:int, city_data: baseModels.CityCreate,
                          db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    city = db.query(models.Cities).filter(models.Cities.id == city_id).first()
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    city.name = city_data.name
    city.mayor_name = city_data.mayor_name
    city.landmark_photo = city_data.landmark_photo
    city.id_region = city_data.id_region
    db.commit()
    return city
