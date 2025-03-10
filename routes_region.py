from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

import baseModels
import models
from dependencies import get_db, oauth2_scheme

routerReg = APIRouter()

@routerReg.post("/regions/", response_model=baseModels.RegionCreate)
def create_region(region: baseModels.RegionCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    new_region = models.Regions(name=region.name, number=region.number, id_district=region.id_district)
    db.add(new_region)
    db.commit()
    db.refresh(new_region)
    return new_region

@routerReg.get("/regions/", response_model=list[baseModels.RegionCreate])
async def get_regions(db: Session = Depends(get_db),
                      skip: int = Query(0, ge=0),
                      limit: int = Query(10, gt=0),
                      name: str = Query(None),
                      number: int = Query(None),
                      id_district: int = Query(None),
                      sort_by: str = Query("number"),
                      sort_order: str = Query("asc"),
                      token: str = Depends(oauth2_scheme)
                      ):
    query = db.query(models.Regions)
    if name:
        query = query.filter(models.Regions.name.ilike(f"%{name}%"))
    if number:
        query = query.filter(models.Regions.number == number)
    if id_district:
        query = query.filter(models.Regions.id_district == id_district)

    if sort_order == "desc":
        query = query.order_by(getattr(models.Regions, sort_by).desc())
    else:
        query = query.order_by(getattr(models.Regions, sort_by))
    return query.offset(skip).limit(limit).all()

@routerReg.get("/regions/{region_id}/", response_model=baseModels.RegionCreate)
async def get_region(region_id:int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    region = db.query(models.Regions).filter(models.Regions.id == region_id).first()
    if region is None:
        raise HTTPException(status_code=404, detail="Region not found")
    return region

@routerReg.delete("/regions/{regions_id}/")
async def delete_region(region_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    region = db.query(models.Regions).filter(models.Regions.id == region_id).first()
    if region is None:
        raise HTTPException(status_code=404, detail="Region not found")
    db.delete(region)
    db.commit()
    return {"message":"ok"}

@routerReg.put("/regions/{region_id}/", response_model=baseModels.RegionCreate)
async def update_region(region_id:int, region_data: baseModels.RegionCreate,
                          db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    region = db.query(models.Regions).filter(models.Regions.id == region_id).first()
    if region is None:
        raise HTTPException(status_code=404, detail="Region not found")
    region.name = region_data.name
    region.number = region_data.number
    region.id_district = region_data.id_district
    db.commit()
    return region