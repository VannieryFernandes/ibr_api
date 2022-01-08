from fastapi import FastAPI
from app.v1 import routes
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Sistema Dominical",description="API para EBD")

origins = [
    "*",
    "http://ibdominical.herokuapp.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


    
@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(routes.api_router)