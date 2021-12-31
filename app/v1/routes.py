from fastapi import APIRouter
from app.v1.membros import membroResource
from app.v1.ebd import ebdResource


prefix = '/v1'
api_router = APIRouter()
# api_router.include_router(router=authResource.router)
api_router.include_router(router=membroResource.router, prefix=prefix)
api_router.include_router(router=ebdResource.router, prefix=prefix)

