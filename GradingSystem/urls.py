from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('review', views.review, name='review'),
    path('about', views.aboutUs, name='aboutUs'),
    path('contact', views.contact, name='contact'),
    path('login', views.login, name='login'),
    path('createAccount', views.createAccount, name='createAccount'),
    path('review_form', views.review_form, name='review_form'),
    path('logout', views.logout, name='logout'),

    path('activate/<uidb64>/<token>',
         views.ActivateAccountView.as_view(), name='activate'),
    #     path('reset_password/',
    #          auth_views.PasswordResetView.as_view(
    #              template_name='accounts/password_reset.html'),
    #          name="reset_password"),
    #     path('reset_password_sent/',
    #          auth_views.PasswordResetDoneView.as_view(
    #              template_name='accounts/password_reset_sent.html'),
    #          name="password_reset_done"),
    #     path('reset/<uidb64>/<token>/',
    #          auth_views.PasswordResetConfirmView.as_view(
    #              template_name='accounts/password_reset_form.html'),
    #          name="password_reset_confirm"),
    #     path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"),
    #          name="password_reset_complete")


    path('reset_password/',
         auth_views.PasswordResetView.as_view(
             template_name='accounts/password_reset.html'),
         name="reset_password"),

    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='accounts/password_reset_sent.html'),
         name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(),
         name="password_reset_confirm"),

    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='accounts/password_reset_done.html'),
         name="password_reset_complete"),
]


# implementing forget password steps
# 1 - Email sent success message   # PasswordResetView.as_view()
# 2 - Email sent success message   # PasswordResetDoneView.as_view()
# 3 - Link to password Reset form in email # PasswordResetComfirmView.as_view()
# 4 - Password Successfully changed message # PasswordREsetcompleteView.as_view()
