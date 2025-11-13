from enum import Enum

class PagamentoStatusEnum(int, Enum):
    Aprovado = 1
    Reprovado = 2
    EmAndamento = 3
    Cancelado = 4
    