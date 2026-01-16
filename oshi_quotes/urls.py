from django.urls import path
from . import views

urlpatterns = [
    path('', views.QuoteListView.as_view(), name='quote_list'),
    path('add/', views.QuoteCreateView.as_view(), name='quote_add'), 
]