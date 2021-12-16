from fastapi import FastAPI,Response,Request


app = FastAPI(title="Sistema IBR",description="API para igrejas")


@app.get("/")
async def root():
    return {"message": "Hello World"}