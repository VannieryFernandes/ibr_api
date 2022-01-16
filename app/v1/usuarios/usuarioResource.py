
from fastapi import APIRouter,Body,HTTPException,Security
from app.v1.db import db
from app.v1.usuarios.usuarioModel import Usuario,UsuarioUpdate,UsuarioEmBanco
from app.v1.usuarios.usuarioController import get_current_active_user
from bson.objectid import ObjectId
from typing import Optional


router = APIRouter(prefix="/usuarios",tags=["Usuarios"])


@router.get('')
async def listar_usuarios(*, offset: int = 1, limit: int = 100,email:Optional[str]=None,ativo:bool = None,current_user: Usuario = Security(get_current_active_user, scopes=["usuarios"])):

    usuarios = []
    offset = (offset-1) * limit
    filters = dict()
    if(email): filters.update({"email":email})
    if(ativo is not None): filters.update({"ativo":ativo})
    
    query = db.usuarios.find(filters).skip(offset).limit(limit)
    for user in query:
        usuarios.append(Usuario(**user))
    return {'usuarios': usuarios}

@router.post('/add')
async def inserir_usuario(usuario: Usuario):
    if hasattr(usuario, 'id'):
        delattr(usuario, 'id')

    ret = db.usuarios.insert_one(usuario.dict(by_alias=True))
    usuario.id = ret.inserted_id
    return {'usuario': usuario}


# @router.put("/{id}")
# async def atualizar_membro(id: str, membro: MembroUpdate=Body(...)):
#     membro_update = dict()
#     if membro.email : membro_update['email'] = membro.email
#     if membro.nome_completo : membro_update['nome_completo'] = membro.nome_completo
#     if membro.usuario : membro_update['usuario'] = membro.usuario
#     if membro.data_de_nascimento : membro_update['data_de_nascimento'] = membro.data_de_nascimento
#     if membro.cpf : membro_update['cpf'] = membro.cpf
#     if membro.nacionalidade : membro_update['nacionalidade'] = membro.nacionalidade
#     if membro.natural : membro_update['natural'] = membro.natural
#     if membro.estado_civil : membro_update['estado_civil'] = membro.estado_civil
#     if membro.filiacao_pai : membro_update['filiacao_pai'] = membro.filiacao_pai
#     if membro.filiacao_mae : membro_update['filiacao_mae'] = membro.filiacao_mae
#     if membro.igreja : membro_update['igreja'] = membro.igreja
#     if membro.data_conversao : membro_update['data_conversao'] = membro.data_conversao
#     if membro.data_batismo : membro_update['data_batismo'] = membro.data_batismo
#     if membro.ebd : membro_update['ebd'] = membro.ebd
#     if membro.membro : membro_update['membro'] = membro.membro
#     if membro.ministerio : membro_update['ministerio'] = membro.ministerio


#     find_membro =  db.membros.find_one({"_id": ObjectId(id)})
#     if find_membro:
#         updated_membro = db.membros.update_one(
#             {"_id": ObjectId(id)}, {"$set": membro_update}
        
#         )
        
#         if updated_membro:
#             return {"membro":membro_update}
#         return {"message":"Erro ao inserir"}
#     else:
#         return {"message":"Não existe este membro"}

