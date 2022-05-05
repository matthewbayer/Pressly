"""newsletter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from app import views
from django.urls.conf import include

urlpatterns = [
    path('activate/<uidb64>/<token>/', views.activate, name="activate"),
    path('admin/', admin.site.urls),
    path('not-active/', views.not_active, name="not-active"),
    path('', views.press_release, name="index"), #Used to be index
    path('api/press-release/', views.generate_pr, name="press_release"),
    path('api/submit_data/', views.submit_data_backend, name="submit_data_backend"),
    #path('app/press-release/', views.press_release, name="press_release"),
    path('app/', views.press_release, name="app"),  #Used to be app
    path('submit-data/', views.submit_data, name="submit_data"),
    path('login/', views.log_in, name="login"),
    path('logout/', views.log_out, name="logout"),
    path('sign-up/', views.sign_up, name="signup"),
    path('privacy/', views.privacy, name="privacy"),
    path('terms/', views.terms, name="terms"),
    path('django-rq/', include('django_rq.urls')),
    path('history/', views.history, name='history')
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)