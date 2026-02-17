from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Quote

class QuoteListViewTests(TestCase):
    def test_quote_list_page_returns_200(self):
        # トップページが正常に表示されるか確認
        url = reverse('quote_list')  # urls.py で付けた名前(quote_list)を使いトップページのURL取得
        response = self.client.get(url)  # テスト用クライアントでトップページにGETリクエストを送る(アクセスシミュレーション)
        self.assertEqual(response.status_code, 200)  # レスポンスのステータスコードが200(成功)かどうか確認

    def test_quote_list_page_uses_correct_template(self):
        # トップページが正しいテンプレートを使用しているか確認
        url = reverse('quote_list')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'oshi_quotes/quote_list.html')  # レスポンスが正しいテンプレートか確認


    def test_quote_list_displays_posted_quote(self):
        # 一覧ページに投稿済みの歌詞が表示されることを確認
        user = get_user_model().objects.create_user(username='testuser', password='password123') # テスト用ユーザー作成
        Quote.objects.create(text="テストの歌詞です", artist="テスト歌手", song_title="テスト曲", author=user) # テスト用フレーズをDB保存
        response = self.client.get(reverse('quote_list')) # トップページにアクセスしてレスポンスを取得
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "テストの歌詞です") # レスポンス内容に投稿した歌詞が含まれているか確認

    def test_quote_add_page_redirects_unlogged_in_user(self):
        # ログインしていないユーザーが投稿ページにアクセス時、ログインページにリダイレクトされることを確認
        url = reverse('quote_add') # urls.py で付けた名前(quote_add)を使い投稿ページのURL取得 
        response = self.client.get(url)
        self.assertRedirects(response,f"{reverse('login')}?next={url}") # next=パラメータも検証、ログイン後に元のページへ戻れる導線も壊れていないか確認

    
    def test_cannot_edit_other_user_quote(self):
        # 他のユーザーの投稿編集ページにアクセスした際、403 Forbidden か 404 Not Found のどちらかが返ることを確認
        # ユーザーAとユーザーBを作成
        user_a = get_user_model().objects.create_user(username='user_a',password='password123')
        user_b = get_user_model().objects.create_user(username='user_b',password='password123')

        # ユーザーAでログインして投稿を一つ作成
        quote_a = Quote.objects.create(text="Aさんの歌詞",artist="歌手A",song_title="曲A",author=user_a)
        # ユーザーBでログイン
        self.client.login(username='user_b', password='password123')
        # ユーザーAの投稿編集ページのURLを取得してアクセスしてみる
        url = reverse('quote_edit', kwargs={'pk': quote_a.pk})
        response = self.client.get(url)
        # 403 か 404(セキュリティ上、存在しない投稿のように見せるため) が返ることを確認
        self.assertIn(response.status_code, [403, 404])


    def test_cannot_edit_other_users_quote_via_post(self):
        # 他のユーザーの投稿をPOSTリクエストで編集できないことを確認
        user_a = get_user_model().objects.create_user(username='user_a', password='password123')
        user_b = get_user_model().objects.create_user(username='user_b', password='password123')
        quote_a = Quote.objects.create(text="Aさんの歌詞", artist="歌手A", song_title="曲A", author=user_a)
        self.client.login(username='user_b', password='password123')
        url = reverse('quote_edit', kwargs={'pk': quote_a.pk})
        # Illegal Edit Attempt(不法な編集の試行) とわかる内容でPOSTリクエストを送る(実際の攻撃者はもっと巧妙な内容を送るかもしれないがテストはわかりやすい内容)
        response = self.client.post(url, {'text': 'Illegal Edit Attempt', 'artist': '歌手B', 'song_title': '曲B'}) 
        # 結果が 403 or 404 であることを確認
        self.assertIn(response.status_code, [403, 404])
        # データベースの中身が書き換わっていない(ユーザーAの歌詞のまま)か確認
        quote_a.refresh_from_db() # 最新の状態をDBから読み直す
        self.assertEqual(quote_a.text, "Aさんの歌詞")


    def test_cannot_delete_other_user_quote_returns_forbidden_or_not_found(self):
        # ユーザーBがユーザーAの投稿を消そうとしても拒絶され、データが消えないことを確認
        user_a = get_user_model().objects.create_user(username='user_a', password='password123')
        user_b = get_user_model().objects.create_user(username='user_b', password='password123')
        quote_a = Quote.objects.create(text="Aさんの歌詞", artist="歌手A", song_title="曲A", author=user_a)
        # ユーザーBでログインして削除ボタン(POST)を叩く
        self.client.login(username='user_b', password='password123')
        url = reverse('quote_delete', kwargs={'pk': quote_a.pk}) # urls.py で付けた名前(quote_delete)を使い削除用のURL取得
        response = self.client.post(url)
        self.assertIn(response.status_code, [403, 404])
        # データベースから削除されていないか確認
        self.assertTrue(Quote.objects.filter(pk=quote_a.pk).exists())


    def test_can_edit_own_quote(self):
        # 自分の投稿ならば正しく内容を更新できることを確認
        user = get_user_model().objects.create_user(username='testuser', password='password123')
        quote = Quote.objects.create(text="元の歌詞", artist="元の歌手", song_title="元の曲", author=user)
        # ログインして編集ページにPOSTリクエストを送る
        self.client.login(username='testuser', password='password123')
        url = reverse('quote_edit', kwargs={'pk': quote.pk})
        self.client.post(url, {'text': '更新した歌詞', 'artist': '更新した歌手', 'song_title': '更新した曲'})
        # データベースを読み直して変更が反映されているか確認
        quote.refresh_from_db()
        self.assertEqual(quote.text, "更新した歌詞")