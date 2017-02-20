from main.models import KnowledgeArea
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from .serializers import KnowledgeAreaSerializer


class KnowledgeAreaList(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        user = request.user
        items = KnowledgeArea.objects.filter(person__pk=user.pk)
        serializer = KnowledgeAreaSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, ):
        pass
