"""
URL configuration for betfair_bot project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from betfair_bot import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('place-bet/', views.place_bet, name='place_bet'),
    path('betting-history/', views.betting_history, name='betting_history'),
    path('accounts/', include('accounts.urls')),
    path('testing/', views.testing_view, name='testing'),
    path('race-selection/', views.race_selection, name='race_selection'),
]
