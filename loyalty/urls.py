from django.urls import path, include
from .views.loyalty_view import LoyaltyUserView, LoyaltyUserSpecificView, PartnershipsListView, PartnershipsSpecificView, LoyaltyProgramListView, LoyaltyProgramSpecificView, LoyaltyProgramTransactionListView, LoyaltyProgramSubscriptionListView, LoyaltyProgramSubscriptionDetailView, LoyaltyMiniTransactionListView, LoyaltyProgramTenantSubscriptionListView, LoyaltyProgramTransactionDetailsList, LoyaltyProgramBalanceListView, LoyaltyProgramBranchListView

urlpatterns = [
    path('loyalty/users', LoyaltyUserView.as_view(), name="loyalty-users"),
    path('loyalty/users/<int:pk>', LoyaltyUserSpecificView.as_view(), name="loyalty-user-specific"),
    path('loyalty/partnerships', PartnershipsListView.as_view(), name="loyalty-partnerships"),
    path('loyalty/partnerships/<int:pk>', PartnershipsSpecificView.as_view(), name="loyalty-partnerships-detail"),
    path('loyalty/<int:pk>/programs', LoyaltyProgramListView.as_view(), name="loyalty-programs"),
    path('loyalty/<int:pk>/programs/branches', LoyaltyProgramBranchListView.as_view(), name="loyalty-programs-branches"),
    path('loyalty/<int:pk>/programs/balances', LoyaltyProgramBalanceListView.as_view(), name="loyalty-programs-balances"),
    path('loyalty/programs/<int:pk>', LoyaltyProgramSpecificView.as_view(), name="loyalty-program-specific"),
    path('loyalty/programs/subscriptions', LoyaltyProgramSubscriptionListView.as_view(), name="loyalty-programs-subscriptions"),
    path('tenant/loyalty/programs/subscriptions', LoyaltyProgramTenantSubscriptionListView.as_view(), name="loyalty-programs-subscriptions-tenant"),
    path('loyalty/programs/subscriptions/<int:pk>', LoyaltyProgramSubscriptionDetailView.as_view(), name="loyalty-programs-subscriptions-detail"),
    path('loyalty/transactions', LoyaltyProgramTransactionListView.as_view(), name="loyalty-programs-transactions"),
    path('loyalty/<int:pk>/transactions', LoyaltyProgramTransactionDetailsList.as_view(), name="loyalty-programs-transactions-details"),
    path('loyalty/transactions/cards', LoyaltyMiniTransactionListView.as_view(), name="loyalty-programs-transactions-cards"),
]