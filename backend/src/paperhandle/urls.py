from django.urls import path

from paperhandle import views

app_name = "pdf"

urlpatterns = [
    # path('', views.pdf_generator, name='generate_pdf'),
    path('rapport/mois/', views.sold_per_month, name='rapport_mois'),
    path('', views.ventes_par_mois_pandas, name='rapport_mois_pandas'),
    path('excel/data/', views.file_data, name='file_data'),
]
