from django.urls import path

from .views import hamburgueria, home, pedido

urlpatterns = [
    path('', home, name='home'),
    path('pedido/', pedido, name='pedido'),
    path('hamburgueria/', hamburgueria, name='hamburgueria'),
]