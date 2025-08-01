from django.db import models
import uuid


class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True, blank=True)
    email = models.EmailField(unique=True)
    age = models.IntegerField()

    def __str__(self):
        return f"{self.name}"

