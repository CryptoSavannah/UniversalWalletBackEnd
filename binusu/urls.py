from django.urls import path, include
from .views.binusu_view import KycListView, OrdersView, ConfirmKyc, ResetPassword, ConfirmPasswordReset, GetCurrentRates, OrdersStatistics, UpdateOrderDetails
from .views.account_view import UserListView, UserLoginView, UserConfirmAccount

urlpatterns = [
    path('binusu/kyc', KycListView.as_view(), name="binusu-kyc"),
    path('binusu/verify_kyc', ConfirmKyc.as_view(), name="binusu-verify-kyc"),
    path('binusu/orders', OrdersView.as_view(), name="binusu-orders"),
    path('binusu/orders/stats', OrdersStatistics.as_view(), name="binusu-orders-stats"),
    path('binusu/orders/update', UpdateOrderDetails.as_view(), name="binusu-orders-update"),
    path('binusu/password_reset', ResetPassword.as_view(), name="binusu_password_reset"),
    path('binusu/confirm_reset', ConfirmPasswordReset.as_view(), name="binusu_confirm_reset"),
    path('binusu/rates', GetCurrentRates.as_view(), name="binusu_rates"),
    path('binusu/accounts', UserListView.as_view(), name="binusu_accounts"),
    path('binusu/accounts/login', UserLoginView.as_view(), name="binusu_login"),
    path('binusu/accounts/activate', UserConfirmAccount.as_view(), name="binusu_account_activate"),
]