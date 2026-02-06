from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
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

#ログインユーザー × 投稿データの紐付け(他人の投稿は編集不可)
class QuoteCreateView(LoginRequiredMixin, CreateView):
    model = Quote
    template_name = 'oshi_quotes/quote_form.html'
    fields = ['text', 'artist', 'song_title']
    success_url = reverse_lazy('quote_list')

# 投稿者情報を現在のログインユーザーに設定
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

# 投稿編集用ビュー
class QuoteUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Quote
    fields = ['text', 'artist', 'song_title']
    template_name = 'oshi_quotes/quote_form.html'
    success_url = reverse_lazy('quote_list')

    def test_func(self):
        quote = self.get_object()
        return quote.author == self.request.user