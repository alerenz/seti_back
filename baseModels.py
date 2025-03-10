from pydantic import BaseModel, conint, constr, confloat, field_validator


class DistrictCreate(BaseModel):
    name: constr(min_length=1, max_length=100)

    @field_validator('name', mode='before')
    def validate_name(cls, v):
        if isinstance(v, int):
            return str(v)
        elif isinstance(v, str):
            return v
        else:
            raise ValueError("Название должно быть строкой")

class RegionCreate(BaseModel):
    name: constr(min_length=1, max_length=100)
    number: conint(ge=1, le=100)
    id_district: conint(ge=1)

    @field_validator('name', mode='before')
    def validate_name(cls, v):
        if isinstance(v, int):
            return str(v)
        elif isinstance(v, str):
            return v
        else:
            raise ValueError("Название должно быть строкой")

class CityCreate(BaseModel):
    name: constr(min_length=1, max_length=100)
    mayor_name: constr(min_length=1, max_length=100)
    landmark_photo: constr(min_length=1, max_length=255)
    id_region: conint(ge=1)

    @field_validator('name', mode='before')
    def validate_name(cls, v):
        if isinstance(v, int):
            return str(v)
        elif isinstance(v, str):
            return v
        else:
            raise ValueError("Название должно быть строкой")

class DemographicCreate(BaseModel):
    birth_rate: confloat(ge=0.01)
    death_rate: confloat(ge=0.01)
    population: conint(ge=1)
    id_city: conint(ge=1)

class PopulationCreate(BaseModel):
    year: conint(ge=1, le=2100)
    population: conint(ge=1)
    id_city: conint(ge=1)

class AppUserCreate(BaseModel):
    username: constr(min_length=1, max_length=100)
    password: constr(min_length=1, max_length=255)

    @field_validator('username', mode='before')
    def validate_name(cls, v):
        if isinstance(v, int):
            return str(v)
        elif isinstance(v, str):
            return v
        else:
            raise ValueError("Логин должен быть строкой")


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        from_attributes = True

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True