from rest_framework.throttling import UserRateThrottle
from datetime import timedelta
from django.utils import timezone
from .models import FriendRequest


class FriendRequestThrottle(UserRateThrottle):
    rate = '3/min'  # Limit to 3 requests per minute

    def allow_request(self, request, view):
        self.user = request.user
        one_min_ago = timezone.now() - timedelta(minutes=1)
        recent_requests = FriendRequest.objects.filter(
            from_user=self.user,
            created_at__gt=one_min_ago
        ).count()
        if recent_requests >= 3:
            return False

        return True

    def wait(self):
        now = timezone.now()
        one_min_ago = now - timedelta(minutes=1)
        recent_requests_count = FriendRequest.objects.filter(
            from_user=self.user,
            created_at__gt=one_min_ago
        ).count()

        if recent_requests_count < 3:
            return 0  # No need to wait if under the limit

        return 60  # Wait for 60 seconds if over the limit
