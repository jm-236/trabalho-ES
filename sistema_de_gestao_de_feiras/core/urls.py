# core/urls.py

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Rotas existentes
    path('', views.pagina_inicial, name='inicio'),
    path('feira/<int:feira_id>/', views.detalhes_feira, name='detalhes_feira'),
    path('expositor/<int:expositor_id>/', views.detalhes_expositor, name='detalhes_expositor'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('cadastro/', views.cadastro, name='cadastro'),

    # NOVAS ROTAS para Ingressos
    path('ingresso/emitir/<int:feira_id>/', views.emitir_ingresso, name='emitir_ingresso'),
    path('ingresso/excluir/<int:ingresso_id>/', views.excluir_ingresso, name='excluir_ingresso'),
]