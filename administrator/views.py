from rest_framework.response import Response
from rest_framework.views import APIView

from common.serializers import UserSerializer
from core.models import User

# Create your views here.
class AmbassadorsAPIView(APIView):
    def get(self, _):
        ambassadors = User.objects.filter(is_ambassador=True)
        
        return Response(UserSerializer(ambassadors, many=True).data)