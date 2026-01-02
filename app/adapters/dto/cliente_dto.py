from pydantic import BaseModel, EmailStr, constr, field_validator
from typing import Optional

class ClienteCreateSchema(BaseModel):
    nome: constr(min_length=3, max_length=100)
    email: EmailStr
    telefone: Optional[constr(min_length=10, max_length=11, pattern=r'^\d{10,11}$')] = None  # Ex: 11912345678
    cpf: constr(min_length=11, max_length=11, pattern=r'^\d{11}$')

    @field_validator("nome")
    def nome_nao_pode_conter_tags(cls, v):
        if "<" in v or ">" in v:
            raise ValueError("Nome não pode conter caracteres inválidos como '<' ou '>'.")
        return v