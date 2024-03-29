from rest_framework import serializers
from ..models import Kyc, Orders, EmailLogs, TelegramLogs, PasswordResets, OrderCompletions
from ..serializers.account_serializer import UserDetailSerializer


class KycSerializer(serializers.ModelSerializer):
    """
    Model Serializer for the Kyc Model
    """
    class Meta:
        model = Kyc
        fields = ('id', 'first_name', 'last_name' ,'phone_number', 'email_address', 'password','nin_number', 'date_submitted')

    def validate_nin_number(self, value):
        """
        Validate nin_number
        """
        if len(value) == 14 and value.startswith(("CM", "CF", "PM", "PF")):
            return value
        raise serializers.ValidationError("Invalid Nin Number")


class KycUserSerializer(serializers.ModelSerializer):
    """
    Short serializer for kyc model user
    """
    class Meta:
        model = Kyc
        fields = ('id', 'first_name', 'last_name', 'email_address', 'phone_number', 'date_submitted')

class KycConfirmSerializer(serializers.Serializer):
    """
    Serializer for kyc confirmation
    """
    email_address   = serializers.CharField(max_length=250)
    password        = serializers.CharField(max_length=250)

class PasswordResetSerializer(serializers.Serializer):
    email_address = serializers.CharField(max_length=250)

class PasswordResetCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PasswordResets
        fields = ('related_account', 'reset_token')

class PasswordConfirmSerializer(serializers.Serializer):
    token           =   serializers.CharField(max_length=250)
    new_password    =   serializers.CharField(max_length=250)

class OrderReceiverSerializer(serializers.Serializer):
    """
    Serializer for receiving orders
    """
    related_kyc             =   serializers.IntegerField()
    order_type              =   serializers.CharField(max_length=250)
    crypto_type             =   serializers.CharField(max_length=250)
    fiat_type               =   serializers.CharField(max_length=250)
    order_amount_crypto     =   serializers.DecimalField(max_digits=20, decimal_places=15)
    order_amount_fiat       =   serializers.DecimalField(max_digits=20, decimal_places=2)
    crypto_unit_price       =   serializers.DecimalField(max_digits=20, decimal_places=2)
    crypto_address          =   serializers.CharField(default=0)
    crypto_fees             =   serializers.DecimalField(max_digits=20, decimal_places=2, default=0)
    crypto_fees_type           =   serializers.CharField(max_length=6, default="MEDIUM")
    total_payable_amount_fiat   =  serializers.DecimalField(max_digits=20, decimal_places=2, default=0)
    warning                 = serializers.IntegerField(default=0)

class TenantOrderReceiverSerializer(serializers.Serializer):
    """
    Serializer for receiving tenant orders
    """
    related_kyc             =   serializers.IntegerField()
    order_type              =   serializers.CharField(max_length=250)
    crypto_type             =   serializers.CharField(max_length=250)
    fiat_type               =   serializers.CharField(max_length=250)
    order_amount            =   serializers.DecimalField(max_digits=15, decimal_places=6)
    crypto_address          =   serializers.CharField(default=0)


class OrdersSerializer(serializers.ModelSerializer):
    """
    Model Serializer for the Orders
    """
    class Meta:
        model = Orders
        fields = ('id', 'related_kyc', 'order_number', 'order_type', 'crypto_type', 'fiat_type', 'order_amount_crypto', 'order_amount_fiat', 'order_status', 'crypto_unit_price', 'crypto_address', 'crypto_fees', 'total_payable_amount_fiat', 'warning', 'tenant_id')

class ClientOrderSerializer(serializers.Serializer):
    """
    Serializer for returning orders
    """
    related_kyc             =   serializers.IntegerField()
    status                  =   serializers.CharField(max_length=30)


class OrdersDetailSerializer(serializers.ModelSerializer):
    """
    Model serializer for order details
    """
    related_kyc = KycUserSerializer(read_only=True)
    fullfilled_by = UserDetailSerializer(read_only=True)

    class Meta:
        model = Orders
        fields = ('id', 'related_kyc', 'order_number', 'order_type', 'crypto_type', 'fiat_type', 'order_amount_crypto', 'order_amount_fiat', 'order_status', 'crypto_unit_price', 'fullfilled_by', 'total_payable_amount_fiat', 'crypto_fees', 'date_ordered')

class OrdersUpdateSerializer(serializers.Serializer):
    """
    Serializer for orders update
    """
    order_number    = serializers.CharField(max_length=250)
    user_id         = serializers.IntegerField()
    status          = serializers.CharField(max_length=20)

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
        fields = ('related_order_telegram', 'telegeam_message', 'status', 'date_dispatched')

class OrderCompletionsCreateSerializer(serializers.ModelSerializer):
    """
    Model serializer for Order Completions
    """
    class Meta:
        model = OrderCompletions
        fields = ('related_order', 'currency', 'amount', 'invoice_number', 'pay_id')

class OrderCompletionsDetailSerializer(serializers.ModelSerializer):
    """
    Model serializer for Order Completions Details
    """
    related_order = OrdersDetailSerializer(read_only=True)
    class Meta:
        model = OrderCompletions
        fields = ('related_order', 'currency', 'amount', 'invoice_number', 'pay_id', 'completion_status', 'time_completed', 'disbursement_status', 'time_disbursed', 'callback_response')


class OrderCompletionSerializer(serializers.Serializer):
    """
    Serializer for returning orders
    """
    related_order             =   serializers.IntegerField()


class OrderCompletionUpdateSerializer(serializers.Serializer):
    """
    Serializer for order updates
    """
    pay_id      =  serializers.CharField(max_length=250)
    errorCode   =  serializers.IntegerField() 
    status      =  serializers.IntegerField()  
    data        =  serializers.JSONField()

class OrderCompletionUpdateSerializerTwo(serializers.Serializer):
    """
    Serializer for order updates 2
    """ 
    Response        =  serializers.JSONField()
