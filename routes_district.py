from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

import baseModels
import models
from dependencies import get_db, oauth2_scheme

routerDis = APIRouter()

@routerDis.post("/districts/", response_model=baseModels.DistrictCreate)
def create_district(district: baseModels.DistrictCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    new_district = models.Districts(name=district.name)
    db.add(new_district)
    db.commit()
    db.refresh(new_district)
    return new_district

@routerDis.get("/districts/", response_model=list[baseModels.DistrictCreate])
async def get_districts(db: Session = Depends(get_db),
                        skip: int = Query(0, ge=0),
                        limit: int = Query(10, gt=0),
                        name: str = Query(None),
                        token: str = Depends(oauth2_scheme)
                        ):
    query = db.query(models.Districts)
    if name:
        query = query.filter(models.Districts.name.ilike(f"%{name}%"))
    return query.offset(skip).limit(limit).all()

@routerDis.get("/districts/{district_id}/", response_model=baseModels.DistrictCreate)
def get_district(district_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    district = db.query(models.Districts).filter(models.Districts.id == district_id).first()
    if district is None:
        raise HTTPException(status_code=404, detail="District not found")
    return district

@routerDis.put("/districts/{district_id}/", response_model=baseModels.DistrictCreate)
async def update_district(district_id:int, district_data: baseModels.DistrictCreate,
                          db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    district = db.query(models.Districts).filter(models.Districts.id == district_id).first()
    if district is None:
        raise HTTPException(status_code=404, detail="District not found")
    district.name = district_data.name
    db.commit()
    return district

@routerDis.delete("/districts/{district_id}/")
async def delete_district(district_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    district = db.query(models.Districts).filter(models.Districts.id == district_id).first()
    if district is None:
        raise HTTPException(status_code=404, detail="District not found")
    db.delete(district)
    db.commit()
    return {"message":"ok"}

