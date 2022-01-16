from pydantic import BaseModel, Field
from pydantic.networks import EmailStr
from bson import ObjectId
from typing import Optional,List
from datetime import date, datetime

class PyObjectId(ObjectId):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid objectid')
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')

class Usuario(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id')
    email: EmailStr
    nome_completo: str
    senha:str
    data_criacao:Optional[datetime] 
    ativo: bool = False
    admin:bool = False
    escopos:List[str]
    disabilitado:bool=False
    


    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }

class UsuarioUpdate(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id')
    email: Optional[EmailStr]
    nome_completo: Optional[str]
    senha:Optional[str]
    data_criacao:Optional[datetime] 
    ativo: Optional[bool]
    admin: Optional[bool]
    disabilitado: Optional[bool]
    escopos:Optional[List[str]]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }

#Relativo a autenticação

class UsuarioEmBanco(Usuario):
    senha: str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(Usuario):
    email: Optional[str] = None
    escopos: List[str] = []



class UsuarioNoBanco(Usuario):
    senha: str
