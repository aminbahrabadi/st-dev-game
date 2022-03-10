from django.contrib.auth import get_user_model
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login
from django.views.generic import CreateView

from .forms import RegisterForm


User = get_user_model()


class UserRegister(CreateView):
    template_name = 'accounts/user_create.html'
    form_class = RegisterForm

    def get_success_url(self):
        return reverse_lazy('game:question_list')


class UserLoginView(LoginView):
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('game:game_start')
    form_class = AuthenticationForm
    redirect_field_name = REDIRECT_FIELD_NAME

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('game:game_start'))

        return super(UserLoginView, self).get(request, *args, **kwargs)

    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):

        # Sets a test cookie to make sure the user has cookies enabled
        request.session.set_test_cookie()

        return super(UserLoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        auth_login(self.request, form.get_user())

        # If the test cookie worked, go ahead and
        # delete it since its no longer needed
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()

        return super(UserLoginView, self).form_valid(form)

    def get_success_url(self):
        redirect_to = self.request.GET.get(self.redirect_field_name)
        if not url_has_allowed_host_and_scheme(url=redirect_to, allowed_hosts=self.request.get_host()):
            redirect_to = self.success_url
        messages.success(self.request, 'Welcome {}!'.format(self.request.user.username))
        return redirect_to


class UserLogoutView(LoginRequiredMixin, LogoutView):
    def get_next_page(self):
        messages.success(self.request, 'You have logged out!')
        return reverse_lazy('accounts:login')


