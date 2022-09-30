from rest_framework.authentication import get_authorization_header
from rest_framework.exceptions import ValidationError


def get_header(request):
    header = get_authorization_header(request)
    if header == b'':
        return None
    try:
        return header.decode()
    except UnicodeError:
        raise ValidationError("Неверная кодировка заголовка с токеном")
