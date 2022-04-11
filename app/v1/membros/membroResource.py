
from fastapi import APIRouter,Body, Depends
from app.v1.db import db
from app.v1.membros.membroModel import Membro, MembroUpdate
from app.v1.usuarios.usuarioController import get_current_active_user, tem_permissao
from app.v1.usuarios.usuarioModel import Usuario
from bson.objectid import ObjectId
from typing import Optional

router = APIRouter(prefix="/membros",tags=["Membros"])


@router.get('')
async def listar_membros(*, offset: int = 1, limit: int = 100,email:Optional[str]=None,turma:Optional[str]=None,matriculado:bool = None,membro:bool=None,current_user: Usuario = Depends(get_current_active_user)):
    await tem_permissao(current_user,"membros:listar")
    membros = []
    offset = (offset-1) * limit
    filters = dict()
    if(email): filters.update({"email":email})
    if(matriculado is not None): filters.update({"ebd":matriculado})
    if(membro is not None): filters.update({"membro":membro})
    if(turma): filters.update({"turma":turma})

        
    query = db.membros.find(filters).skip(offset).limit(limit)
    for membro in query:
        membros.append(Membro(**membro))
    return {'membros': membros}

@router.post('/add')
async def inserir_membro(membro: Membro,current_user: Usuario = Depends(get_current_active_user)):
    '''
        Descrição: Endpoint responsável por inserir membro 
        turma = descrita por 4 tipos: \n
        -crianças
        -juniores
        -adolescentes
        -adultos
    '''
    await tem_permissao(current_user,"membros:adicionar")
    if hasattr(membro, 'id'):
        delattr(membro, 'id')
    ret = db.membros.insert_one(membro.dict(by_alias=True))
    membro.id = ret.inserted_id
    return {'membro': membro}


@router.put("/{id}")
async def atualizar_membro(id: str, membro: MembroUpdate=Body(...),current_user: Usuario = Depends(get_current_active_user)):

    '''
    Descrição: Endpoint responsável por atualizar membro por meio do ID
    turma = descrita por 4 tipos: \n
    -crianças
    -juniores
    -adolescentes
    -adultos
    '''
    await tem_permissao(current_user,"membros:atualizar")
    membro_update = dict()
    if membro.email : membro_update['email'] = membro.email
    if membro.nome_completo : membro_update['nome_completo'] = membro.nome_completo
    if membro.usuario : membro_update['usuario'] = membro.usuario
    if membro.data_de_nascimento : membro_update['data_de_nascimento'] = membro.data_de_nascimento
    if membro.cpf : membro_update['cpf'] = membro.cpf
    if membro.nacionalidade : membro_update['nacionalidade'] = membro.nacionalidade
    if membro.natural : membro_update['natural'] = membro.natural
    if membro.estado_civil : membro_update['estado_civil'] = membro.estado_civil
    if membro.filiacao_pai : membro_update['filiacao_pai'] = membro.filiacao_pai
    if membro.filiacao_mae : membro_update['filiacao_mae'] = membro.filiacao_mae
    if membro.igreja : membro_update['igreja'] = membro.igreja
    if membro.data_conversao : membro_update['data_conversao'] = membro.data_conversao
    if membro.data_batismo : membro_update['data_batismo'] = membro.data_batismo
    if membro.ebd : membro_update['ebd'] = membro.ebd
    if membro.membro : membro_update['membro'] = membro.membro
    if membro.ministerio : membro_update['ministerio'] = membro.ministerio
    if membro.tipo_sanguineo : membro_update['tipo_sanguineo'] = membro.tipo_sanguineo
    if membro.turma : membro_update['turma'] = membro.turma



    find_membro =  db.membros.find_one({"_id": ObjectId(id)})
    if find_membro:
        updated_membro = db.membros.update_one(
            {"_id": ObjectId(id)}, {"$set": membro_update}
        
        )
        
        if updated_membro:
            return {"membro":membro_update}
        return {"message":"Erro ao inserir"}
    else:
        return {"message":"Não existe este membro"}
