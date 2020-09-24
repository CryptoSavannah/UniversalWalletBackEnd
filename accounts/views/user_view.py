from accounts.models import User
from django.contrib.auth import authenticate, login
from rest_framework_jwt.settings import api_settings
from rest_framework import permissions
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from ..serializers.user_serializer import UserSerializer, TokenSerializer, UserSaveSerializer
from loyalty.serializers.loyalty_serializer import LoyaltyUserCreateSerializer, LoyaltyTenantsDetailsSerializer

from loyalty.models import LoyaltyUserPoints, LoyaltyTenants

# Get the JWT settings, add these lines after the import/from lines
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class LoginView(APIView):
    """
    POST authorization/
    """
    # This permission class will overide the global permission
    # class setting
    permission_classes = (permissions.AllowAny,)


    def post(self, request, *args, **kwargs):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        user_type  = request.data.get("type", "")

        # try:
        user = authenticate(request, username=username, password=password)

        if user is not None:
            
            login(request, user)
            token_serializer = TokenSerializer(data={
                # using drf jwt utility functions to generate a token
                "token": jwt_encode_handler(
                    jwt_payload_handler(user)
                )})
            token_serializer.is_valid()
            user_serializer = UserSerializer(user)

            try:
                if user_type == "0":
                    login_data = {"user_data":user_serializer.data, "token_data":token_serializer.data}
                    return Response(login_data)

                else:
                    tenant = LoyaltyTenants.objects.get(related_user_account=user_serializer.data['id'])
                    tenant_serializer = LoyaltyTenantsDetailsSerializer(tenant)
                    login_data = {"user_data":user_serializer.data, "tenant_data":tenant_serializer.data, "token_data":token_serializer.data}
                    return Response(login_data)
            except:
                return Response({"error": "Contact support and stop being silly"})

        return Response({"error": "invalid username or password"}, status=status.HTTP_404_NOT_FOUND)
        # except:
        #     return Response({"error": "User doesnot exist"}, status=status.HTTP_404_NOT_FOUND)


class UserListView(APIView):
    """
    List all users and create a new user.
    """
    # permission_classes = (permissions.IsAuthenticated, )

    # def get(self, request, format=None):
    #     serializer = UserSerializer(User.objects.filter(active=True), many=True)
    #     return Response({"status":200, "data":serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            
            serializer.save()

            #create loyalty account
            # loyalty_account_creation = LoyaltyUserCreateSerializer(data={'related_user':serializer.data['id']})
            # loyalty_account_creation.is_valid(raise_exception=True)
            # loyalty_account_creation.save()
            return Response({"status":201, "data":serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserSpecificView(APIView):
    """
    Actions that can be performed on a specific user account
    """
    permission_classes = (permissions.IsAuthenticated, )

    def get_object(self, pk):
        return User.objects.get(pk=pk)

    def get(self, request, pk):
        serializer = UserSaveSerializer(self.get_object(pk))
        return Response({"status":200, "data":serializer.data}, status=status.HTTP_200_OK)


    def patch(self, request, pk):
        user_object = self.get_object(pk)
        serializer = UserSaveSerializer(user_object, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status":201, "data":serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        User.objects.update_or_create(
            id=pk, defaults={'active':False}
        )
        return Response({"status":200, "data":"Successfull"}, status=status.HTTP_200_OK)
