
from datetime import timedelta
from fastapi import APIRouter,Body,Depends,HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.v1.db import db
from app.v1.usuarios.usuarioModel import Usuario, UsuarioLogin,UsuarioUpdate,UsuarioEmBanco,Token
from app.v1.usuarios.usuarioController import ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user, create_access_token, get_current_active_user, get_password_hash, tem_permissao, verify_password
from bson.objectid import ObjectId
from typing import Optional


router = APIRouter(prefix="/usuarios",tags=["Usuarios"])


@router.get('')
async def listar_usuarios(*, offset: int = 1, limit: int = 100,email:Optional[str]=None,ativo:bool = None,current_user: Usuario = Depends(get_current_active_user)):

    await tem_permissao(current_user,"usuarios:listar")
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
async def inserir_usuario(usuario: Usuario,current_user: Usuario = Depends(get_current_active_user)):
    await tem_permissao(current_user,"usuarios:criar")
    if hasattr(usuario, 'id'):
        delattr(usuario, 'id')
    usuario.senha = get_password_hash(usuario.senha)
    ret = db.usuarios.insert_one(usuario.dict(by_alias=True))
    usuario.id = ret.inserted_id
    return {'usuario': usuario}


@router.post("/login",response_model=Token,include_in_schema=False)
def login_documentacao(
    usuario: OAuth2PasswordRequestForm = Depends()
    # current_user: DBUser = Depends(get_current_active_superuser),
    ):
    """
    Autenticação pela documentação
    """
    
    user = authenticate_user(email=usuario.username,password=usuario.password)
    if not user:
        raise HTTPException(401,"Email ou senha incorreta!")

    print(user)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"email": user.email},expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/token",response_model=Token)
def token(
    usuario: UsuarioLogin
    ):
    """
    Autenticar com email e senha
    """
    user = authenticate_user(email=usuario.email,password=usuario.senha)
    if not user:
        raise HTTPException(401,"Email ou senha incorreta!")
    
    access_token = create_access_token(
        data={"email": user.email}
    )

    return {"access_token": access_token, "token_type": "bearer"}