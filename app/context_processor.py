from .settings import URL_PREFIX, API_PREFIX, DEBUG
import json


def global_vars(request):
    type_user = request.user.is_superuser
    user_id = request.user.id
    return {
        "URL_PREFIX": URL_PREFIX,
        "API_PREFIX": API_PREFIX,
        "PRODUCCION": DEBUG,
        "TYPE_USER": type_user,
        "USER_ID": user_id
    }
