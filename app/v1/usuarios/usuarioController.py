


from datetime import datetime, timedelta
import email
from typing import List, Optional
from app.v1.usuarios.usuarioModel import Usuario, UsuarioEmBanco,TokenData
from fastapi import Depends, FastAPI, HTTPException, Security, status
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    SecurityScopes,
)
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, ValidationError
import os
from app.v1.db import db
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 30



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/v1/usuarios/login"
)



def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(email: str):
    user_dict = db.usuarios.find_one({"email":email})
    if user_dict and 'email' in user_dict:
        return UsuarioEmBanco(**user_dict)
    return False



def authenticate_user(email: str, password: str):
    user = get_user(email)
    if not user:
        return False
    if not verify_password(password, user.senha):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais Inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("email")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    
    user = get_user(email=token_data.email)
    if user is None:
        raise credentials_exception
    return user
        

async def get_current_active_user(current_user: Usuario = Depends(get_current_user)):
    if current_user.ativo==False:
        raise HTTPException(status_code=400, detail="Usuario Inativo")
    
    return current_user

async def tem_permissao(current_user:Usuario,permissao:str=None):
    if(current_user.admin==True):
        return True
    elif(permissao not in current_user.escopos):
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Não tem permissão"
                )
    
    
