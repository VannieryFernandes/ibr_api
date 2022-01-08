
from fastapi import APIRouter,Body
from starlette.types import Message
from app.v1.db import db
from app.v1.ebd.ebdModel import EBD, EBDUpdate
from bson.objectid import ObjectId
import json

router = APIRouter(prefix="/ebd",tags=["EBD"])


@router.get('')
async def listar_leituras(*, offset: int = 1, limit: int = 100):
    ''' Descrição: Endpoint responsável por listar a leitura bíblica de cada membro por data \n'''
    offset = (offset-1) * limit
    leituras = []
    for membro in db.escola_biblica.find().skip(offset).limit(limit):
        leituras.append(EBD(**membro))
    return {'leituras': leituras}

@router.post('/add')
async def inserir_leituras(membro: EBD):
    '''
    Descrição: Endpoint responsável por cadastrar a leitura bíblica semanal de cada membro \n
    Observações:\n
    id_membros = é o _id do membro \n
    usuario = apelido do aluno \n
    turma = descrita por 3 tipos: \n
        -crianças
        -juniores
        -adolescentes
        -adultos
    '''
    if hasattr(membro, 'id'):
        delattr(membro, 'id')
    ret = db.escola_biblica.insert_one(membro.dict(by_alias=True))
    membro.id = ret.inserted_id
    return {'leituras': membro}

@router.put("/{id}")
async def atualizar_leitura(id: str, membro: EBDUpdate=Body(...)):
    membro_update = dict()
    if membro.turma : membro_update['turma'] = membro.turma
    if membro.presenca : membro_update['presenca'] = membro.presenca
    if membro.id_membro : membro_update['id_membro'] = membro.id_membro
    if membro.usuario : membro_update['usuario'] = membro.usuario
    if membro.data_escola : membro_update['data_escola'] = membro.data_escola
    if membro.numero_biblia : membro_update['numero_biblia'] = membro.numero_biblia


    find_leitura_membro =  db.escola_biblica.find_one({"_id": ObjectId(id)})
    if find_leitura_membro:
        updated_leitura_membro = db.escola_biblica.update_one(
            {"_id": ObjectId(id)}, {"$set": membro_update}
        )
        if updated_leitura_membro:
            return {"leitura":membro_update}
        return {"message":"Erro ao inserir"}
    else:
        return {"message":"Não existe essa leitura"}

