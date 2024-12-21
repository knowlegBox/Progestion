from django.urls import path
from . import views

app_name = "account"

urlpatterns = [
    path("", views.CreateViewUser.as_view(), name="create"),
    # path("", views.create_user, name="create"),
    path("<int:pk>/", views.DetailViewUser.as_view(), name="profile"),
    path("<int:pk>/", views.DeleteViewUser.as_view(), name="delete"),
    path("<int:pk>/", views.UpdateViewUser.as_view(), name="update"),
]
