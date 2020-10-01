from rest_framework import serializers
from accounts.serializers.user_serializer import UserShortDetailsSerializer
from ..models import LoyaltyUserPoints, Partnerships, LoyaltyProgram, LoyaltyProgramTransactions, LoyaltyTenants, LoyaltyProgramSubscriptions


class LoyaltyTenantsCreateSerializer(serializers.ModelSerializer):
    """
    Model serializer for creating loyalty tenants
    """
    class Meta:
        model = LoyaltyTenants
        fields = ('tenant_name', 'related_user_account', 'tenant_desctiption', 'tenant_contact', 'due_date')

class LoyaltyTenantsDetailsSerializer(serializers.ModelSerializer):
    """
    Model serializer for loyalty tenants
    """
    class Meta:
        model = LoyaltyTenants
        fields = '__all__'

class LoyaltyUserCreateSerializer(serializers.ModelSerializer):
    """
    Model serializer for creating a loyalty user
    """
    class Meta:
        model = LoyaltyUserPoints
        fields = ('id', 'related_user')

class LoyaltyUserDetailsSerializer(serializers.ModelSerializer):
    """
    Model serializer for loyalty user details
    """
    related_user = UserShortDetailsSerializer(read_only=True)
    class Meta:
        model = LoyaltyUserPoints
        fields = '__all__'

class PartnershipsCreateSerializer(serializers.ModelSerializer):
    """
    Model serializer for creating a partnership
    """
    class Meta:
        model = Partnerships
        fields = ('partner_name', 'partner_product', 'partner_contact', 'percentage_points')

class PartnershipsDetailsSerializer(serializers.ModelSerializer):
    """
    Model serializer for partner details
    """
    class Meta:
        model = Partnerships
        fields = '__all__'

class LoyaltyProgramCreateSerializer(serializers.ModelSerializer):
    """
    Model serializer for creating loyalty programs
    """
    class Meta:
        model = LoyaltyProgram
        fields = ('program_name', 'products_attached', 'program_percentage', 'start_date', 'due_date')

class LoyaltyProgramDetailsSerializer(serializers.ModelSerializer):
    """
    Model serializer loyalty program details
    """
    class Meta:
        model = LoyaltyProgram
        fields = '__all__'


class LoyaltyProgramSubscriptionsDataSerializer(serializers.Serializer):
    """
    Model serializer for creating loyalty program subscriptions
    """
    related_program     = serializers.IntegerField()
    related_user        = serializers.IntegerField()


class LoyaltyProgramSubscriptionsCreateSerializer(serializers.ModelSerializer):
    """
    Model serializer for saving loyalty program subscriptions
    """
    class Meta:
        model = LoyaltyProgramSubscriptions
        fields = ('related_loyalty_program', 'related_user', 'status', 'card_number')


class LoyaltyProgramSubscriptionsDetailsSerializer(serializers.ModelSerializer):
    """
    Model serializer loyalty program subscription details
    """
    related_loyalty_program = LoyaltyProgramDetailsSerializer(read_only=True)
    related_user    = UserShortDetailsSerializer(read_only=True)
    class Meta:
        model = LoyaltyProgramSubscriptions
        fields = ('id', 'related_loyalty_program', 'related_user', 'status', 'card_number', 'points_earned', 'rating')


class LoyaltyProgramTransactionSerializer(serializers.ModelSerializer):
    """
    Model Serializer for creating Loyalty Transactions
    """
    class Meta:
        model = LoyaltyProgramTransactions
        fields = ("related_program", "related_user", "transaction_amount", "receipt_number", "payment_mode", "transaction_date", "points_awarded")

class LoyaltyProgramTransactionDetailsSerializer(serializers.ModelSerializer):
    """
    Model serializer for transaction details
    """
    class Meta:
        model = LoyaltyProgramTransactions
        fields = "__all__"

class LoyaltyProgramCreateSerializer(serializers.Serializer):
    card_number         = serializers.CharField(max_length=40)
    transaction_amount  = serializers.DecimalField(max_digits=20, decimal_places=2)
    receipt_number      = serializers.CharField(max_length=25)
    payment_mode        = serializers.CharField(max_length=25)
    transaction_date    = serializers.DateField()

class LoyaltyProgramSpendSerializer(serializers.Serializer):
    card_number         = serializers.CharField(max_length=40)
    amount  = serializers.DecimalField(max_digits=20, decimal_places=2)

class LoyaltyProgramMiniStatementSerializer(serializers.Serializer):
    card_number         = serializers.CharField(max_length=40)
