from rest_framework.views import APIView
from rest_framework.response import Response


class ChatAPIView(APIView):

    def post(self, request):
        message = request.data.get("message")

        return Response({
            "reply": f"پیامت دریافت شد: {message}"
        })