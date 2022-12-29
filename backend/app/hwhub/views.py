from rest_framework.views import APIView
from rest_framework.response import Response

class UserAPIView(APIView):
    def get(self, request, id):
        return Response({'message': 'Hello, world!'})

