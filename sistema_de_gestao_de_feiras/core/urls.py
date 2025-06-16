# core/urls.py

from django.urls import path
from . import views  # Importa as views do app core

urlpatterns = [
    # Quando a URL for vazia (''), chame a view 'pagina_inicial'
    path('', views.pagina_inicial, name='inicio'),
	path('feira/<int:feira_id>', views.detalhes_feira, name='detalhes_feira'),
]
