from django.urls import path, include
from .views.binusu_view import KycListView, OrdersView, ConfirmKyc

urlpatterns = [
    path('binusu/kyc', KycListView.as_view(), name="binusu-kyc"),
    path('binusu/verify_kyc', ConfirmKyc.as_view(), name="binusu-verify-kyc"),
    path('binusu/orders', OrdersView.as_view(), name="binusu-orders"),
]