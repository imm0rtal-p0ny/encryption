from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('encryption/', views.EncryptionView.as_view(), name='encryption'),
    path('decryption/', views.DecryptionView.as_view(), name='decryption'),
]
