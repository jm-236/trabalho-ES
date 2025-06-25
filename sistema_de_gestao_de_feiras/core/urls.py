# core/urls.py

from django.urls import path
from . import views  # Importa as views do app core
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Quando a URL for vazia (''), chame a view 'pagina_inicial'
    path('', views.pagina_inicial, name='inicio'),
	path('feira/<int:feira_id>', views.detalhes_feira, name='detalhes_feira'),
    path('expositor/<int:expositor_id>/', views.detalhes_expositor, name='detalhes_expositor'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('cadastro/', views.cadastro, name='cadastro'),
]
