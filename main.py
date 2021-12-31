from fastapi import FastAPI
from app.v1 import routes

app = FastAPI(title="Sistema Dominical",description="API para igrejas")


    
@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(routes.api_router)