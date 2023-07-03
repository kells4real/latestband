"""band URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from app import auth_views as login_view
from app.views import redirected, register

handler404 = 'app.views.handler404'
handler500 = 'app.views.handler500'
handler403 = 'app.views.handler403'

urlpatterns = [
    path('redirect/', redirected, name="redirect"),
    path('tz_detect/', include('tz_detect.urls')),
    path('settings/admin/', admin.site.urls),
    path('account/', include('app.urls')),
    path('hey',  include('landing.urls')),
    path('create-account/', register, name="register"),
    path('login/', login_view.LoginView.as_view(template_name='landing/home.html'), name='login'),
    path('session_expired/', login_view.LoginView.as_view(template_name='landing/home2.html'), name='login2'),
    path('logout/', login_view.LogoutView.as_view(template_name='landing/home.html'), name='logout'),
    path('password-reset/',
         login_view.PasswordResetView.as_view(
             template_name='app/password_reset.html'
         ),
         name='password_reset'),
    path('password-reset/done/',
         login_view.PasswordResetDoneView.as_view(
             template_name='app/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         login_view.PasswordResetConfirmView.as_view(
             template_name='app/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         login_view.PasswordResetCompleteView.as_view(
             template_name='app/password_reset_complete.html'
         ),
         name='password_reset_complete'),

    path('password-change/',
         login_view.PasswordChangeView.as_view(
             template_name='app/password_change.html'
         ),
         name='password_change'),

    path('password-change-done/',
         login_view.PasswordChangeDoneView.as_view(
             template_name='app/password_change_done.html'
         ),
         name='password_change_done'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)