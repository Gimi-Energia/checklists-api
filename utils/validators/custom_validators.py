from datetime import date

import brazilcep
from validate_docbr import CNPJ


def retroactive_date(input_date: date) -> bool:
    if input_date < date.today():
        return False

    return True


def valid_cnpj(cnpj: str) -> bool:
    return CNPJ().validate(cnpj)


def valid_cep(cep: str) -> bool:
    try:
        brazilcep.get_address_from_cep(cep)
        return True
    except Exception:
        return False
