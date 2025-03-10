from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

import baseModels
import models
from dependencies import get_db, oauth2_scheme

routerPop = APIRouter()

@routerPop.post("/populations/", response_model=baseModels.PopulationCreate)
def create_population(population: baseModels.PopulationCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    new_population = models.Population(year=population.year, population=population.population, id_city=population.id_city)
    db.add(new_population)
    db.commit()
    db.refresh(new_population)
    return new_population

@routerPop.get("/populations/", response_model=list[baseModels.PopulationCreate])
async def get_populations(db: Session = Depends(get_db),
                          skip: int = Query(0, ge=0),
                          limit: int = Query(10, gt=0),
                          id_city: int = Query(None),
                          sort_by: str = Query("year"),
                          sort_order: str = Query("asc"),
                          token: str = Depends(oauth2_scheme)
                          ):
    query = db.query(models.Population)

    if id_city:
        query = query.filter(models.Population.id_city == id_city)

    if sort_order == "desc":
        query = query.order_by(getattr(models.Population, sort_by).desc())
    else:
        query = query.order_by(getattr(models.Population, sort_by))

    return query.offset(skip).limit(limit).all()

@routerPop.get("/populations/{population_id}/", response_model=baseModels.PopulationCreate)
async def get_population(population_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    population = db.query(models.Population).filter(models.Population.id == population_id).first()
    if population is None:
        raise HTTPException(status_code=404, detail="Population not found")
    return population

@routerPop.delete("/populations/{population_id}/")
async def delete_population(population_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    population = db.query(models.Population).filter(models.Population.id == population_id).first()
    if population is None:
        raise HTTPException(status_code=404, detail="Population not found")
    db.delete(population)
    db.commit()
    return {"message":"ok"}

@routerPop.put("/populations/{population_id}/", response_model=baseModels.PopulationCreate)
async def update_population(population_id:int, population_data: baseModels.PopulationCreate,
                          db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    population = db.query(models.Population).filter(models.Population.id == population_id).first()
    if population is None:
        raise HTTPException(status_code=404, detail="Population not found")
    population.year = population_data.year
    population.population = population_data.population
    population.id_city = population_data.id_city
    db.commit()
    return population

