from django.shortcuts import render
from django.conf import settings
from .forms import Login_form, User_update_form, User_create_form
from django.contrib.auth.views import LoginView, LogoutView
#from django.views.generic import CreateView, TemplateView
from django.views import generic  # viewまとめ
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.shortcuts import render, redirect, resolve_url
from django.template.loader import render_to_string
from django.http import HttpResponse, Http404, HttpResponseBadRequest
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin  # ログインのみ
from .models import scraping, target
# import mojimoji    #python3.7でインストールエラー
import jaconv  # mojimojiの代わり
import re

# Create your views here.
"""
class Only_own_mixin(UserPassesTestMixin, LoginRequiredMixin):  # ログイン判別（もう使ってない）
    raise_exception = True

    def test_func(self):
        # 今ログインしてるユーザーのpkと、そのユーザー情報ページのpkが同じか、又はスーパーユーザーなら許可
        user = self.request.user
        return user.pk == self.kwargs['pk'] or user.is_superuser
"""
# Create your views here.


def tracking_ship(request):
    track_number = request.GET.get('track_number')
    if 9 < len(track_number) < 20:  # 10桁以上20桁未満で通す
        track_number = jaconv.z2h(
            track_number, digit=True, ascii=True)  # 全角を半角に
        track_number = re.sub("\\D", "", track_number)  # 数字以外を消す
        texts = scraping(track_number)  # 追跡番号検索
        data_dict = {}  # データ用
        target_td_num = {}  # データ数
        data = {'track_number': str(track_number)}
        for t in target:  # 一度取得データをdictで整形
            data_dict.update([(t, texts[t])])
        target_dict = {  # ターゲット一覧
            target[0]: "日本郵政",
            target[1]: "佐川急便",
            target[2]: "クロネコヤマト",
            target[3]: "西濃運輸",
            target[4]: "日本通運",
            target[5]: "福山通運",
        }
        for i in range(len(target)):
            target_td_num.update([(
                target[i], int((len(data_dict[target[i]]))/2)
            )])

        data.update([('data', data_dict)])  # 扱いやすい様辞書の入れ子にする
        data.update([('targets', target_dict)])  # ターゲット一覧
        data.update([('td_num', target_td_num)])  # ターゲットのtd数
        # print(data)
        return render(request, 'tracking/search.html', data)
    else:
        return render(request, 'tracking/search.html')


class Top(generic.TemplateView):
    template_name = 'tracking/top.html'


class Login(LoginView):
    # ログイン
    form_class = Login_form
    template_name = 'tracking/login.html'

    # def get_success_url(self):
    #    url = self.get_redirect_url()
    #    return url or resolve_url('tracking:predict', pk=self.request.user.pk)


class Logout(LogoutView):
    # ログアウト
    template_name = 'tracking/top.html'

    def log_out(self):
        logout(self.request)


User = get_user_model()


class User_detail(generic.DetailView):
    # ユーザ情報閲覧
    model = User
    template_name = 'tracking/user_detail.html'


class User_update(generic.UpdateView):
    # ユーザ情報更新
    model = User
    form_class = User_update_form
    template_name = 'tracking/user_update.html'

    def get_success_url(self):
        return resolve_url('tracking:user_detail', pk=self.kwargs['pk'])


class User_create(generic.CreateView):
    # ユーザ仮登録
    template_name = 'tracking/user_create.html'
    form_class = User_create_form

    def form_valid(self, form):
        # 仮登録と本登録用メールの発行.
        # 仮登録と本登録の切り替えは、is_active属性を使うと簡単
        # 退会処理も、is_activeをFalseにするだけ
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        # アクティベーションURLの送付
        current_site = get_current_site(self.request)
        domain = current_site.domain
        context = {
            'protocol': self.request.scheme,
            'domain': domain,
            'token': dumps(user.pk),
            'user': user,
        }

        subject = render_to_string(
            'mail_templates/subject.txt', context)
        message = render_to_string(
            'mail_templates/message.txt', context)

        user.email_user(subject, message)
        return redirect('tracking:user_create_done')


class User_create_done(generic.TemplateView):
    # ユーザ仮登録
    template_name = 'tracking/user_create_done.html'


class User_create_complete(generic.TemplateView):
    # メール内URLアクセス後のユーザ本登録
    template_name = 'tracking/user_create_complete.html'
    timeout_seconds = getattr(
        settings, 'ACTIVATION_TIMEOUT_SECONDS', 60*60*24)  # デフォルトでは1日以内

    def get(self, request, **kwargs):
        # tokenが正しければ本登録.
        token = kwargs.get('token')
        try:
            user_pk = loads(token, max_age=self.timeout_seconds)

        # 期限切れ
        except SignatureExpired:
            return HttpResponseBadRequest()

        # tokenが間違っている
        except BadSignature:
            return HttpResponseBadRequest()

        # tokenは問題なし
        else:
            try:
                user = User.objects.get(pk=user_pk)
            except User.DoesNotExist:
                return HttpResponseBadRequest()
            else:
                if not user.is_active:
                    # 問題なければ本登録とする
                    user.is_active = True
                    user.save()
                    return super().get(request, **kwargs)

        return HttpResponseBadRequest()
