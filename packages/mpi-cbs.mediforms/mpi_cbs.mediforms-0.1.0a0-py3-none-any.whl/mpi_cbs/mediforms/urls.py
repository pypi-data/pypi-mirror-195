from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from mpi_cbs.mediforms import views


urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('login/', LoginView.as_view(template_name='mediforms/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('form/<uuid:token>/', views.FormView.as_view(), name='form'),
]
