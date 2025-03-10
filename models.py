from sqlalchemy import Column, ForeignKey, Integer, String, Float, Boolean
from database import Base

class Districts(Base):
    __tablename__ = "districts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

class Regions(Base):
    __tablename__ = "regions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    number = Column(Integer, index=True)
    id_district = Column(Integer, ForeignKey("districts.id"))

class Cities(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    mayor_name = Column(String, index=True)
    landmark_photo = Column(String, index=True)
    id_region = Column(Integer, ForeignKey("regions.id"))

class Demographic(Base):
    __tablename__ = "demographic"

    id = Column(Integer, primary_key=True, index=True)
    birth_rate = Column(Float)
    death_rate = Column(Float)
    population = Column(Integer, index=True)
    id_city = Column(Integer, ForeignKey("cities.id"))

class Population(Base):
    __tablename__ = "population"

    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, index=True)
    population = Column(Integer, index=True)
    id_city = Column(Integer, ForeignKey("cities.id"))

class AppUsers(Base):
    __tablename__ = "appusers"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hash_password = Column(String)