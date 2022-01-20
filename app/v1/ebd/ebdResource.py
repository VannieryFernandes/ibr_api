
from fastapi import APIRouter,Body
from typing import Optional
from app.v1.db import db
from app.v1.ebd.ebdModel import EBD, EBDUpdate
from bson.objectid import ObjectId


router = APIRouter(prefix="/ebd",tags=["EBD"])


@router.get('')
async def listar_leituras(*, offset: int = 1, limit: int = 100,data_ebd:Optional[str]=None):
    ''' Descrição: Endpoint responsável por listar a leitura bíblica de cada membro por data \n'''
    offset = (offset-1) * limit
    leituras = []
    filters = dict()
    if(data_ebd):filters.update({"data_escola":data_ebd})

    query = db.escola_biblica.find(filters).skip(offset).limit(limit)
    for membro in query:
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

@router.get('/leituras-sumarizadas')
async def listar_sumarizado(*,data_ebd:Optional[str]=None,turma:Optional[str]=None):
    ''' Descrição: Endpoint responsável por relatório da EBD por data \n'''


    filters = dict()
    if(data_ebd):filters.update({"data_escola":data_ebd})
    if(turma):filters.update({"turma":turma})
    matriculados = db.escola_biblica.count_documents(filters)
    filters.update({'presenca':False})
    ausentes = db.escola_biblica.count_documents(filters)
    filters.update({'presenca':True})
    presentes = db.escola_biblica.count_documents(filters)
    # filters.update({ 'numero_biblia': { '$gt': 0 } })
    # capitulos_lidos = db.escola_biblica.find(filters)
    # print(query)
    # for membro in query:
    #     leituras.append(EBD(**membro))
    return {'matriculados': matriculados,'presentes':presentes,'ausentes':ausentes}
