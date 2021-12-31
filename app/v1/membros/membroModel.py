from pydantic import BaseModel, Field
from pydantic.networks import EmailStr
from bson import ObjectId
from typing import Optional
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

class Membro(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id')
    email: EmailStr
    nome_completo: str
    usuario: str
    data_de_nascimento: datetime
    cpf: Optional[str]
    nacionalidade: Optional[str]
    natural: Optional[str]
    estado_civil: Optional[str]
    filiacao_pai:Optional[str]
    filiacao_mae:Optional[str]
    #dados cristao
    igreja:Optional[str]
    data_conversao:Optional[datetime]
    data_batismo:Optional[datetime]
    ebd: bool = False
    membro: bool = False
    ministerio: Optional[str]


    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }
