from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView # UpdateViewのインポート
from .models import Quote
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin # UserPassesTestMixinのインポート

class QuoteListView(ListView):
    model = Quote
    template_name = 'oshi_quotes/quote_list.html'
    context_object_name = 'quotes'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # ランダムな1件を 'random_quote' としてテンプレートに渡す
        context['random_quote'] = Quote.objects.order_by('?').first()
        return context

# ログインユーザーと投稿データを紐付ける（投稿作成用ビュー）
class QuoteCreateView(LoginRequiredMixin, CreateView):
    model = Quote
    template_name = 'oshi_quotes/quote_form.html'
    fields = ['text', 'artist', 'song_title']
    success_url = reverse_lazy('quote_list')

# 投稿者を現在のログインユーザーとして保存
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

# 投稿編集用ビュー（他ユーザーの投稿は編集不可）
class QuoteUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Quote
    fields = ['text', 'artist', 'song_title']
    template_name = 'oshi_quotes/quote_form.html'
    success_url = reverse_lazy('quote_list')

    raise_exception = True # 権限がない場合に403エラーを返す

# 投稿者本人のみ編集可能かを判定
    def test_func(self):
        quote = self.get_object()
        return quote.author == self.request.user
    