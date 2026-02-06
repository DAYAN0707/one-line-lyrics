from django.contrib import admin
from .models import Quote  # 自分のモデルをインポート

admin.site.register(Quote) # 管理画面や入力フォームのラベルを日本語化
