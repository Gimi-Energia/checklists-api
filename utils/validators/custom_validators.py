from datetime import date

from validate_docbr import CNPJ


def retroactive_date(input_date: date) -> bool:
    if input_date < date.today():
        return False

    return True


def valid_cnpj(cnpj: str) -> bool:
    return CNPJ().validate(cnpj)
