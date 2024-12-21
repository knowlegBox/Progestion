"""from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from account.models import UsersBase


class UserFormCreate(UserCreationForm):
    class Meta:
        model = UsersBase
        # fields = UserCreationForm.Meta.fields
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
        )
"""