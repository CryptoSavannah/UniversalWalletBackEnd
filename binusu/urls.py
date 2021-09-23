from django.urls import path, include
from .views.binusu_view import KycListView, OrdersView, ConfirmKyc, ResetPassword, ConfirmPasswordReset, GetCurrentRates, OrdersStatistics, UpdateOrderDetails, ClientOrdersView, OrderCompletionCollection, GetSpecificOrderDetails, UpdateOrderCompletionStatus, ClientOrderCompletionView
from .views.account_view import UserListView, UserLoginView, UserConfirmAccount

urlpatterns = [
    path('binusu/kyc', KycListView.as_view(), name="binusu-kyc"),
    path('binusu/verify_kyc', ConfirmKyc.as_view(), name="binusu-verify-kyc"),
    path('binusu/orders', OrdersView.as_view(), name="binusu-orders"),
    path('binusu/orders/collection', OrderCompletionCollection.as_view(), name="binusu-orders-collection"),
    path('binusu/orders/collection/update', UpdateOrderCompletionStatus.as_view(), name="binusu-orders-collection-update"),
    path('binusu/orders/specific', GetSpecificOrderDetails.as_view(), name="binusu-orders-specific"),
    path('binusu/orders/stats', OrdersStatistics.as_view(), name="binusu-orders-stats"),
    path('binusu/orders/clients', ClientOrdersView.as_view(), name="binusu-clients-orders"),
    path('binusu/orders/completion', ClientOrderCompletionView.as_view(), name="binusu-clients-orders-completion"),
    path('binusu/orders/update', UpdateOrderDetails.as_view(), name="binusu-orders-update"),
    path('binusu/password_reset', ResetPassword.as_view(), name="binusu_password_reset"),
    path('binusu/confirm_reset', ConfirmPasswordReset.as_view(), name="binusu_confirm_reset"),
    path('binusu/rates', GetCurrentRates.as_view(), name="binusu_rates"),
    path('binusu/accounts', UserListView.as_view(), name="binusu_accounts"),
    path('binusu/accounts/login', UserLoginView.as_view(), name="binusu_login"),
    path('binusu/accounts/activate', UserConfirmAccount.as_view(), name="binusu_account_activate"),
]