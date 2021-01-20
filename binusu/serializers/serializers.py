from rest_framework import serializers
from ..models import Kyc, Orders, EmailLogs, TelegramLogs

class KycSerializer(serializers.ModelSerializer):
    """
    Model Serializer for the Kyc Model
    """
    class Meta:
        model = Kyc
        fields = ('id', 'first_name', 'last_name' ,'phone_number', 'email_address', 'password','nin_number', 'date_submitted')

class KycUserSerializer(serializers.ModelSerializer):
    """
    Short serializer for kyc model user
    """
    class Meta:
        model = Kyc
        fields = ('id', 'first_name', 'last_name', 'email_address')

class KycConfirmSerializer(serializers.Serializer):
    """
    Serializer for kyc confirmation
    """
    email_address   = serializers.CharField(max_length=250)
    password        = serializers.CharField(max_length=10)

class OrderReceiverSerializer(serializers.Serializer):
    """
    Serializer for receiving orders
    """
    related_kyc             =   serializers.IntegerField()
    order_type              =   serializers.CharField(max_length=250)
    crypto_type             =   serializers.CharField(max_length=250)
    fiat_type               =   serializers.CharField(max_length=250)
    order_amount_crypto     =   serializers.DecimalField(max_digits=20, decimal_places=6)
    order_amount_fiat       =   serializers.DecimalField(max_digits=20, decimal_places=2)
    crypto_unit_price       =   serializers.DecimalField(max_digits=20, decimal_places=2)

class OrdersSerializer(serializers.ModelSerializer):
    """
    Model Serializer for the Orders
    """
    class Meta:
        model = Orders
        fields = ('id', 'related_kyc', 'order_number', 'order_type', 'crypto_type', 'fiat_type', 'order_amount_crypto', 'order_amount_fiat', 'order_status', 'crypto_unit_price')

class EmailLogsSerializer(serializers.ModelSerializer):
    """
    Model Serializer for Email Logs
    """
    class Meta:
        model = EmailLogs
        fields = ('related_order_email', 'support_email', 'client_email', 'email_message', 'status', 'date_dispatched')


class TelegramLogsSerializer(serializers.ModelSerializer):
    """
    Model Serializer for Telegram Logs
    """
    class Meta:
        model = TelegramLogs
        fields = ('releated_order_telegram', 'telegeam_message', 'status', 'date_dispatched')