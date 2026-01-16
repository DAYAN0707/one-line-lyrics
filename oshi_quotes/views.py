from django.views.generic import ListView, CreateView # Create_Viewを追加
from django.contrib.auth.mixins import LoginRequiredMixin # ログイン必須にするため
from django.urls import reverse_lazy
from .models import Quote

class QuoteListView(ListView):
    model = Quote
    template_name = 'oshi_quotes/quote_list.html'
    context_object_name = 'quotes'

class QuoteCreateView(LoginRequiredMixin, CreateView):
    model = Quote
    template_name = 'oshi_quotes/quote_form.html'
    fields = ['text', 'artist', 'song_title'] # 入力してもらう項目
    success_url = reverse_lazy('quote_list') # 保存したら一覧へ

    def form_valid(self, form):
        form.instance.author = self.request.user # ログイン中のユーザーを作者にする
        return super().form_valid(form)
    
