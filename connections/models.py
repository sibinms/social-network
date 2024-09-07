from django.contrib.auth.models import User
from django.db import models

FRIENDSHIP_STATUSES = [
    ('accepted', 'Accepted'),
    ('rejected', 'Rejected'),
    ('pending', 'Pending')
]


class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=FRIENDSHIP_STATUSES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_user', 'to_user')
