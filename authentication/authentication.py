from rest_framework.authentication import BaseAuthentication
from authentication.models import CustomToken
from rest_framework.exceptions import AuthenticationFailed


class CustomTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')

        if not token:
            raise AuthenticationFailed('Please provide token')  # Authentication failed
        
        if token:
            token = token.split(' ')[1]  # Assuming token is sent as 'Token <token>'
            if CustomToken.objects.filter(token=token).exists():
                return (None, None)  # Authentication successful
            
        raise AuthenticationFailed('You do not have permission to access this endpoint')  # Authentication failed

