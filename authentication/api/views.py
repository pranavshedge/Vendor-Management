# views.py

from rest_framework.decorators import api_view
from rest_framework.response import Response
from authentication.models import CustomToken

@api_view(['POST'])
def generate_token(request):
    token_instance = CustomToken.create_token()
    return Response({"token": token_instance.token})
