
from fastapi import APIRouter
from app.v1.db import db
from app.v1.membros.membroModel import Membro
from typing import List

router = APIRouter(prefix="/membros",tags=["Membros"])


@router.get('')
async def listar_membros(*, offset: int = 1, limit: int = 100):

    membros = []
    offset = (offset-1) * limit

    for membro in db.membros.find().skip(offset).limit(limit):
        membros.append(Membro(**membro))
    return {'membros': membros}

@router.post('/add')
async def inserir_membro(membro: Membro):
    if hasattr(membro, 'id'):
        delattr(membro, 'id')
    ret = db.membros.insert_one(membro.dict(by_alias=True))
    membro.id = ret.inserted_id
    return {'membro': membro}