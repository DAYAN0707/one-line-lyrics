from django.urls import path
from . import views

urlpatterns = [
    path('', views.QuoteListView.as_view(), name='quote_list'), # 一覧表示用のURLパターンを追加
    path('add/', views.QuoteCreateView.as_view(), name='quote_add'), # 新規投稿用のURLパターンを追加
    path('quote/<int:pk>/edit/', views.QuoteUpdateView.as_view(), name='quote_edit'), # 編集用のURLパターンを追加
    path('quote/<int:pk>/delete/', views.QuoteDeleteView.as_view(), name='quote_delete'), # 削除用のURLパターンを追加
]
