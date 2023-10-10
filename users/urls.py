from django.contrib.auth import views as auth_views
from django.urls import path
from users import views


urlpatterns = [
    path('signup', views.SignUpView.as_view(), name='signup'),
    path('login', views.UserLoginView.as_view(), name='login'),
    path('logout', views.UserLogoutView.as_view(), name='logout'),
    path('all_users', views.AllUsersView.as_view(), name='all-users'),
    path('add_user', views.AddUserView.as_view(), name='add-user'),
    path('super_profile/<int:pk>', views.SuperProfile.as_view(), name='profile'),
    path('user_profile/<int:pk>', views.UserProfile.as_view(), name='user-profile'),
    path('delete_profile/<int:pk>', views.DeleteProfile.as_view(), name='delete-profile'),
    path('change_password', views.ChangePassword.as_view(), name='change-password'),
    path('change_password_done', views.ChangePasswordDone.as_view(), name='change-password-done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset_form.html'),
         name='password_reset'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
]
