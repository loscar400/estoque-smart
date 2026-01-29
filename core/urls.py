from django.urls import path
from . import views

urlpatterns = [

    path('', views.dashboard, name='dashboard'),

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('produtos/', views.produto_list, name='produto_list'),
    path('produtos/novo/', views.produto_create, name='produto_create'),

    path('movimentos/', views.movimento_list, name='movimento_list'),
    path('movimentos/novo/', views.movimento_create, name='movimento_create'),

]
