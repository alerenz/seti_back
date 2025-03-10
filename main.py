from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse

from routes import router as auth_router
import uvicorn

from routes_city import routerCity
from routes_demographic import routerDemo
from routes_district import routerDis
from routes_population import routerPop
from routes_region import routerReg

app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(routerDis, tags=["district"])
app.include_router(routerReg, tags=["region"])
app.include_router(routerCity, tags=["city"])
app.include_router(routerDemo, tags=["demographic"])
app.include_router(routerPop, tags=["population"])


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": exc.body},
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)