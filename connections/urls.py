from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ListFriendsView, ListPendingRequestsView, FriendRequestViewSet

router = DefaultRouter()
router.register(r'requests', FriendRequestViewSet, basename='friend-request')

urlpatterns = [
    path('friends/', ListFriendsView.as_view(), name='list-friends'),
    path('friends/pending-requests/', ListPendingRequestsView.as_view(), name='list-pending-requests'),
    path('friends/', include(router.urls)),
]
