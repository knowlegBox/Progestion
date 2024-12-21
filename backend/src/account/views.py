from django.contrib.auth import authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic


# from account.form.userforms import UserFormCreate


class UserCreate(UserCreationForm):
    pass


class CreateViewUser(generic.CreateView):
    model = User
    fields = (
        "username",
        "first_name",
        "last_name",
        "email",
    )
    template_name = "account/create.html"
    # success_url = reverse_lazy("myhome")
    success_url = reverse_lazy("myhome")


class DetailViewUser(generic.DetailView):
    # model = UsersBase
    template_name = "account/profile.html"
    context_object_name = "user"


class DeleteViewUser(generic.DeleteView):
    # model = UsersBase
    pass


class UpdateViewUser(generic.UpdateView):
    #     model = UsersBase
    #     form_class = UserFormCreate
    template_name = "account/profile.html"


# def create_user(request):
#     if request.method == "POST":
# #         form = UserFormCreate(request.POST)
# #         if form.is_valid():
# #             form.save()
#             return redirect("home")
#     else:
#          # form = UserFormCreate()
#         pass
#     return render(request, "account/create.html", context={"form": form})

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        authenticate(request, username, email)


def user_logout(request):
    logout(request.user)
