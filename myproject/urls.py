"""
URL configuration for myproject project.

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
from django.urls import include, path
from myapp import views
urlpatterns = [
        path('admin/', admin.site.urls),

    path('league_detail.html', views.league_detail, name='league_detail'),
path('match_detail.html', views.match_detail, name='match_detail'),
path('team_detail.html/<int:team_id>/', views.team_detail, name='team_detail'),    path('match_list.html', views.match_list, name='match_list'),
    path('match_list.html/<int:league_id>/', views.match_list, name='league_match_list'),
]