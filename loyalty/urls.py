from django.urls import path, include
from .views.loyalty_view import LoyaltyUserView, LoyaltyUserSpecificView, PartnershipsListView, PartnershipsSpecificView, LoyaltyProgramListView, LoyaltyProgramSpecificView, LoyaltyProgramTransactionListView, LoyaltyProgramSubscriptionListView, LoyaltyProgramSubscriptionDetailView

urlpatterns = [
    path('loyalty/users', LoyaltyUserView.as_view(), name="loyalty-users"),
    path('loyalty/users/<int:pk>', LoyaltyUserSpecificView.as_view(), name="loyalty-user-specific"),
    path('loyalty/partnerships', PartnershipsListView.as_view(), name="loyalty-partnerships"),
    path('loyalty/partnerships/<int:pk>', PartnershipsSpecificView.as_view(), name="loyalty-partnerships-detail"),
    path('loyalty/programs', LoyaltyProgramListView.as_view(), name="loyalty-programs"),
    path('loyalty/programs', LoyaltyProgramListView.as_view(), name="loyalty-programs"),
    path('loyalty/programs/subscriptions', LoyaltyProgramSubscriptionListView.as_view(), name="loyalty-programs-subscriptions"),
    path('loyalty/programs/subscriptions/<int:pk>', LoyaltyProgramSubscriptionDetailView.as_view(), name="loyalty-programs-subscriptions-detail"),
    path('loyalty/transactions', LoyaltyProgramTransactionListView.as_view(), name="loyalty-programs-transactions"),
]