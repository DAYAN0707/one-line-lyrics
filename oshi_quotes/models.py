from django.db import models
from django.contrib.auth.models import User  # Django標準のユーザー機能を使う

#Quote モデルに ForeignKey を持たせ、投稿とユーザーを1対多で関連付け
class Quote(models.Model):
    # User と Quote（ER図の1/N）、誰の投稿かをDBレベルで持てる
    # 誰の投稿か（ユーザーが削除されたら、その人の投稿も消える設定）
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # 保存したい項目
    text = models.TextField(verbose_name="フレーズ")
    artist = models.CharField(max_length=100, verbose_name="アーティスト名")
    song_title = models.CharField(max_length=100, verbose_name="曲名")
    
    # 自動で登録日時を入れる
    created_at = models.DateTimeField(auto_now_add=True)

    #__str__ メソッドを定義し、管理画面上「どのアーティストのどのフレーズか」一目で判別
    def __str__(self):
        return f"{self.artist} - {self.text[:10]}..."