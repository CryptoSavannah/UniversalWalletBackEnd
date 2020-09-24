import random

from rest_framework import permissions
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q

from ..models import LoyaltyUserPoints, Partnerships, LoyaltyProgram, LoyaltyProgramTransactions, LoyaltyProgramSubscriptions
from accounts.models import User
from ..serializers.loyalty_serializer import LoyaltyUserCreateSerializer, LoyaltyUserDetailsSerializer, LoyaltyProgramCreateSerializer, PartnershipsCreateSerializer, PartnershipsDetailsSerializer, LoyaltyProgramDetailsSerializer, LoyaltyProgramCreateSerializer, LoyaltyProgramTransactionSerializer, LoyaltyProgramTransactionDetailsSerializer, LoyaltyProgramSubscriptionsDataSerializer, LoyaltyProgramSubscriptionsDetailsSerializer, LoyaltyProgramSubscriptionsCreateSerializer

class LoyaltyUserView(APIView):
    """
    List all loyalty users
    """
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, format=None):
        serializer = LoyaltyUserDetailsSerializer(LoyaltyUserPoints.objects.filter(active=True), many=True)
        return Response({"status":200, "data":serializer.data}, status=status.HTTP_200_OK)


class LoyaltyUserSpecificView(APIView):
    """
    Actions that can be performed on a specific loyalty user
    """
    permission_classes = (permissions.IsAuthenticated, )

    def get_object(self, pk):
        return LoyaltyUserPoints.objects.get(pk=pk)

    def get(self, request, pk):
        serializer = LoyaltyUserDetailsSerializer(self.get_object(pk))
        return Response({"status":200, "data":serializer.data}, status=status.HTTP_200_OK)


    def delete(self, request, pk):
        LoyaltyUserPoints.objects.update_or_create(
            id=pk, defaults={'active':False}
        )
        return Response({"status":200, "data":"Successfull"}, status=status.HTTP_200_OK)


class PartnershipsListView(APIView):
    """
    List all partnerships and create a new partnership.
    """
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, format=None):
        serializer = PartnershipsDetailsSerializer(Partnerships.objects.filter(status=True), many=True)
        return Response({"status":200, "data":serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = PartnershipsCreateSerializer(data=request.data)
        if serializer.is_valid():
            
            serializer.save()
            return Response({"status":201, "data":serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class PartnershipsSpecificView(APIView):
    """
    Actions that can be performed on a specific partnership
    """
    permission_classes = (permissions.IsAuthenticated, )

    def get_object(self, pk):
        return Partnerships.objects.get(pk=pk)

    def get(self, request, pk):
        serializer = PartnershipsDetailsSerializer(self.get_object(pk))
        return Response({"status":200, "data":serializer.data}, status=status.HTTP_200_OK)


    def patch(self, request, pk):
        partnership_object = self.get_object(pk)
        serializer = PartnershipsDetailsSerializer(partnership_object, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status":201, "data":serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        Partnerships.objects.update_or_create(
            id=pk, defaults={'status':False}
        )
        return Response({"status":200, "data":"Successfull"}, status=status.HTTP_200_OK)


class LoyaltyProgramListView(APIView):
    """
    List all loyalty programs and create a new loyalty program.
    """
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, format=None):
        serializer = LoyaltyProgramDetailsSerializer(LoyaltyProgram.objects.filter(status=True), many=True)
        return Response({"status":200, "data":serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = LoyaltyProgramCreateSerializer(data=request.data)
        if serializer.is_valid():
            
            serializer.save()
            return Response({"status":201, "data":serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LoyaltyProgramSpecificView(APIView):
    """
    Actions that can be performed on a specific loyalty program
    """
    permission_classes = (permissions.IsAuthenticated, )

    def get_object(self, pk):
        return LoyaltyProgram.objects.get(pk=pk)

    def get(self, request, pk):
        serializer = LoyaltyProgramDetailsSerializer(self.get_object(pk))
        return Response({"status":200, "data":serializer.data}, status=status.HTTP_200_OK)


    def patch(self, request, pk):
        loyalty_program_object = self.get_object(pk)
        serializer = LoyaltyProgramDetailsSerializer(loyalty_program_object, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status":201, "data":serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        LoyaltyProgram.objects.update_or_create(
            id=pk, defaults={'status':False}
        )
        return Response({"status":200, "data":"Successfull"}, status=status.HTTP_200_OK)



class LoyaltyProgramSubscriptionListView(APIView):
    """
    List all loyalty program subscriptions and create a new loyalty program subscription.
    """
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, format=None):
        serializer = LoyaltyProgramSubscriptionsDetailsSerializer(LoyaltyProgramSubscriptions.objects.filter(related_user=request.query_params.get("id", None)).filter(status=True), many=True)
        return Response({"status":200, "data":serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = LoyaltyProgramSubscriptionsDataSerializer(data=request.data)
        if serializer.is_valid():
            try:
                existing_subscription = LoyaltyProgramSubscriptions.objects.get(Q(related_loyalty_program=serializer.data['related_program']), Q(related_user=serializer.data['related_user']))

                if existing_subscription:
                    return Response({"status":400, "error":"User already subscribed to program"}, status=status.HTTP_400_BAD_REQUEST)

            except:
                try:
                    program_check = LoyaltyProgramSubscriptions.objects.get(pk=int(serializer.data['related_program']))
                    user_check = User.objects.get(pk=int(serializer.data['related_user']))

                    card_number = random.randint(10000000, 99999999) 

                    subscription_data = {
                        "related_loyalty_program":serializer.data['related_program'],
                        "related_user":serializer.data['related_user'],
                        "card_number":'CPS{}XXMWQ'.format(card_number)
                    }

                    loyalty_subscription = LoyaltyProgramSubscriptionsCreateSerializer(data=subscription_data)
                    loyalty_subscription.is_valid(raise_exception=True)
                    loyalty_subscription.save()

                    return Response({"status":201, "data":loyalty_subscription.data}, status=status.HTTP_201_CREATED)
                except:
                    return Response({"status":400, "error":"Invalid user or program id"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoyaltyProgramSubscriptionDetailView(APIView):
    """
    Actions that can be performed on a specific loyalty program subscription
    """
    permission_classes = (permissions.IsAuthenticated, )

    def get_object(self, pk):
        return LoyaltyProgramSubscriptions.objects.get(pk=pk)

    def get(self, request, pk):
        serializer = LoyaltyProgramSubscriptionsDetailsSerializer(self.get_object(pk))
        return Response({"status":200, "data":serializer.data}, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        LoyaltyProgramSubscriptions.objects.update_or_create(
            id=pk, defaults={'status':False}
        )
        return Response({"status":200, "data":"Successfull"}, status=status.HTTP_200_OK)


class LoyaltyProgramTransactionListView(APIView):
    """
    List all loyalty program transactions and create a new loyalty program transaction.
    """
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, pk, format=None):
        serializer = LoyaltyProgramTransactionDetailsSerializer(LoyaltyProgramTransactions.objects.filter(related_program=pk), many=True)
        return Response({"status":200, "data":serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, pk, format=None):
        serializer = LoyaltyProgramCreateSerializer(data=request.data)
        if serializer.is_valid():

            transaction_data = {
                "related_program":serializer.data["related_program"],
                "related_user":serializer.data["related_user"],
                "transaction_amount":serializer.data["transaction_amount"],
                "receipt_number":serializer.data["receipt_number"],
                "payment_mode":serializer.data["payment_mode"],
                "transaction_date":serializer.data["transaction_date"],
                "points_awarded":0.03*float(serializer.data["transaction_amount"])
            }

            loyalty_transaction = LoyaltyProgramTransactionSerializer(data=transaction_data)
            loyalty_transaction.is_valid(raise_exception=True)
            loyalty_transaction.save()

            current_points = LoyaltyUserPoints.objects.get(id=serializer.data["related_user"])
            current_points_serialized = LoyaltyUserDetailsSerializer(current_points)
            new_points = float(current_points_serialized.data["points_accrued"]) + float(loyalty_transaction.data['points_awarded'])

            LoyaltyUserPoints.objects.update_or_create(
            id=serializer.data["related_user"], defaults={'points_accrued':new_points}
            )
            
            return Response({"status":201, "data":loyalty_transaction.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)