from django.db import models
from django.contrib.auth.models import User
import uuid
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    auth_token = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    active = models.BooleanField(default=False)