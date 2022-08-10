from rest_framework.authentication import TokenAuthentication as BaseAuthToken
from rest_framework.authtoken.models import Token

class TokenAuthentication(BaseAuthToken):
    keyword = 'Bearer'