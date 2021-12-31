
from fastapi import APIRouter
from app.v1.db import db
from app.v1.ebd.ebdModel import EBD

router = APIRouter(prefix="/ebd",tags=["EBD"])


@router.get('')
async def listar_leituras():
    membros = []
    for membro in db.escola_biblica.find():
        membros.append(EBD(**membro))
    return {'leituras': membros}

@router.post('/add')
async def inserir_leituras(membro: EBD):
    if hasattr(membro, 'id'):
        delattr(membro, 'id')
    ret = db.escola_biblica.insert_one(membro.dict(by_alias=True))
    membro.id = ret.inserted_id
    return {'leituras': membro}