from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import RegisterSerializer, UserSerializer
from .tasks import send_email
from rest_framework import status


class RegisterApi(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)

        if serializer.is_valid(raise_exception = True):
            user = serializer.save()
            send_email.delay("Thank you for registering", request.data["email"], f"Thank you {request.data['username']}"
                                                                                 f"for registering in our chat app")
            return Response({"user": UserSerializer(user, context = self.get_serializer_context()).data,
                             "message": "User Created Successfully."})

        return Response({"Message": "Couldnt register the user"},status = status.HTTP_400_BAD_REQUEST)
