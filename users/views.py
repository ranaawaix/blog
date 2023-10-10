from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from users.forms import SignUpForm, LoginForm, UserSearchForm, AddUserForm, SuperProfileForm, UserProfileForm, \
    ChangePasswordForm


# Create your views here.

class SignUpView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'users/signup.html'
    success_url = reverse_lazy('login')


class UserLoginView(LoginView):
    form_class = LoginForm
    template_name = 'users/login.html'
    success_url = reverse_lazy('dashboard')


class UserLogoutView(LogoutView):
    next_page = 'login'


class AllUsersView(ListView):
    model = User
    template_name = 'users/all_users.html'
    context_object_name = 'users'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = UserSearchForm(self.request.GET)
        context['search_query'] = self.request.GET.get('search_query')
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search_query')
        if search_query:
            queryset = User.objects.filter(username__icontains=search_query)

        return queryset


class AddUserView(CreateView):
    model = User
    form_class = AddUserForm
    template_name = 'users/add_new.html'


class SuperProfile(UpdateView):
    model = User
    form_class = SuperProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('all-users')


class UserProfile(UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('all-posts')


class DeleteProfile(DeleteView):
    model = User
    template_name = 'users/confirm_delete.html'
    success_url = 'all-users'


class ChangePassword(PasswordChangeView):
    form_class = ChangePasswordForm
    template_name = 'users/password_change.html'
    success_url = reverse_lazy('change-password-done')


class ChangePasswordDone(PasswordChangeDoneView):
    template_name = 'users/change_password_done.html'
