from django.urls import path
from . import views

app_name = "customer"

urlpatterns = [
  path("", views.ListeCustomerView.as_view(), name="home"),
  path("create/", views.CreateCustomerView.as_view(), name="create"),
  path("update/<int:pk>/", views.UpdateCustomerView.as_view(), name="update"),
  path("delete/<int:pk>/", views.DeleteCustomerView.as_view(), name="delete"),
  path("detail/<int:pk>/", views.customer_detail, name="detail"),
  # path("tableau-de-bord/", views.try_dashboad, name="dashboard"),
]
