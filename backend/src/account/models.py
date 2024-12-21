"""from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


# Create your models here.
class UsersBase(AbstractUser):
    numbers = models.CharField(max_length=15,verbose_name="Numero",blank=True)

    class Meta:
        permissions = [
            ("change_task_status", "Can change the status of tasks"),
            ("close_task", "Can remove a task by setting its status as closed"),
        ]

    def get_absolute_url(self):
        return reverse('account:profile', kwargs={"pk": self.pk})
"""

