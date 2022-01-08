from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Optional
import datetime
from enum import Enum

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

class Classes(str, Enum):
    crianças='crianças'
    juniores='juniores'
    adolescentes='adolescentes'
    adultos='adultos'

class EBD(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id')
    usuario: str
    id_membro: str
    presenca: bool = True
    data_escola : str = 'yyyy-mm-dd'
    numero_biblia : Optional[int]
    turma: Classes

    class Config:
        arbitrary_types_allowed = True
        use_enum_values = True
        json_encoders = {
            ObjectId: str
        }

class EBDUpdate(BaseModel):
    usuario: Optional[str]
    id_membro: Optional[str]
    presenca: Optional[bool]
    data_escola : Optional[str]
    numero_biblia : Optional[int]
    turma: Optional[Classes]
    class Config:
        arbitrary_types_allowed = True
        use_enum_values = True
        json_encoders = {
            ObjectId: str
        }
