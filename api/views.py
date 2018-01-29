# Authors: Hyunwoo Lee <hyunwoo9301@naver.com>
# Released under the MIT license.

from rest_framework import status
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from api.models import MessageModel
from api.handler import message

class DialogSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageModel
        fields = '__all__'

class MessageAPI(APIView):
    serializer_class = DialogSerializer

    def post(self, request, format=None):
        serializer = DialogSerializer(data=request.data)
        if serializer.is_valid():
            return Response(message(serializer.data), status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)