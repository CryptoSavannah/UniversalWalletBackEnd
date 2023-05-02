from accounts.models import User, Otp
from django.contrib.auth import authenticate, login
from rest_framework_jwt.settings import api_settings
from rest_framework import permissions
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from ..serializers.user_serializer import UserSerializer, TokenSerializer, UserSaveSerializer, UserCreateSerializer, OtpVerificationSerializer
from loyalty.serializers.loyalty_serializer import LoyaltyUserCreateSerializer, LoyaltyTenantsDetailsSerializer

from loyalty.models import LoyaltyUserPoints, LoyaltyTenants
# from ..helpers.accounts import send_otp

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
        print(user)
        if user is not None:   
            if user.active:
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
            return Response({"status": 403, "error":"User not activated, Please contact support"})
        return Response({"error": "invalid username or password"}, status=status.HTTP_404_NOT_FOUND)



class UserListView(APIView):
    """
    Create a new user.
    """
    def post(self, request, format=None):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user_data = {
                    "first_name":serializer.data["first_name"],
                    "last_name":serializer.data["last_name"],
                    "username":serializer.data["phone_number"],
                    "email":serializer.data["email"],
                    "password":serializer.data["pin_code"],
                    "prefix":serializer.data["phone_prefix"],
                    "location":serializer.data["location"]
                }

        
                user_data_serialized = UserSerializer(data=user_data) 
                user_data_serialized.is_valid(raise_exception=True)
                user_data_serialized.save()

                phone_number = "{}{}".format(user_data_serialized.data["prefix"], user_data_serialized.data["username"])

                send_otp(user_data_serialized.data['id'], phone_number, user_data_serialized.data["first_name"])
                return Response({"status":201, "data":user_data_serialized.data}, status=status.HTTP_201_CREATED)
            except:
                return Response({"status":500, "error":"User account already exists, Please use another username"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyUserOtp(APIView):
    """
    Verify a user's otp and activate their account
    """
    def post(self, request, format=None):
        serializer = OtpVerificationSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.data["phone_number"]
            user = User.objects.get(username=phone_number)
           
            otp_object = Otp.objects.get(user=user)

            if not user.active:
                if int(otp_object.otp_code) == serializer.data["otp"]:
                    
                    User.objects.update_or_create(
                    id=user.id, defaults={'active':True}
                    )

                    token_serializer = TokenSerializer(data={
                    # using drf jwt utility functions to generate a token
                    "token": jwt_encode_handler(
                        jwt_payload_handler(user)
                    )})
                    token_serializer.is_valid()
                    user_serializer = UserSerializer(user)

                    login_data = {"user_data":user_serializer.data, "token_data":token_serializer.data}

                    return Response({"status":200, "data": login_data}, status=status.HTTP_200_OK)
                
                return Response({"status":400, "error":"Bad Otp code"})
            return Response({"status":200, "message":"User already activated"}, status=status.HTTP_200_OK)
        
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
