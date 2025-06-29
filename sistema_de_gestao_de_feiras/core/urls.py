from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Rotas Públicas
    path('', views.pagina_inicial, name='inicio'),
    path('feira/<int:feira_id>/', views.detalhes_feira, name='detalhes_feira'),
    path('expositor/<int:expositor_id>/', views.detalhes_expositor, name='detalhes_expositor'),

    # Autenticação e Cadastro
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Dashboards
    path('dashboard/', views.dashboard, name='dashboard'),

    # Funcionalidades do Visitante
    path('ingresso/emitir/<int:feira_id>/', views.emitir_ingresso, name='emitir_ingresso'),
    path('ingresso/excluir/<int:ingresso_id>/', views.excluir_ingresso, name='excluir_ingresso'),

    # Funcionalidades do Organizador
    path('organizador/feira/criar/', views.feira_criar, name='feira_criar'),
    path('organizador/feira/editar/<int:feira_id>/', views.feira_editar, name='feira_editar'),
    path('organizador/feira/excluir/<int:feira_id>/', views.feira_excluir, name='feira_excluir'),

    # Funcionalidades do Expositor
    path('expositor/produto/criar/', views.produto_criar, name='produto_criar'),
    path('expositor/produto/editar/<int:produto_id>/', views.produto_editar, name='produto_editar'),
    path('expositor/produto/excluir/<int:produto_id>/', views.produto_excluir, name='produto_excluir'),
    path('expositor/feiras/', views.expositor_gerenciar_feiras, name='expositor_gerenciar_feiras'),

    # TElas de edição de perfil
    path('perfil/', views.editar_perfil, name='editar_perfil'),
    path('perfil/expositor/', views.editar_perfil_expositor, name='editar_perfil_expositor'),
]