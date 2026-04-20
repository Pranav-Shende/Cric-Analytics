"""
URL configuration for cricket_site project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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


# cricket_site/urls.py
# from django.contrib import admin
# from django.urls import path
# from stats.views import master_dashboard, laws_list

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', master_dashboard, name='home'),
#     path('laws/', laws_list, name='laws_list'),
# ]


# cricket_site/urls.py
from stats.views import *
from django.contrib import admin
from django.urls import path
  # Make sure this import is at the top
from django.conf import settings
from django.conf.urls.static import static
# from django.contrib import admin
# from django.urls import path
# from stats.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('batsmen/', batsmen_list, name='batsmen_list'),
    path('bowlers/', bowlers_list, name='bowlers_list'),
    path('fielders/', fielders_list, name='fielders_list'),
    path('all-rounders/', all_rounders_list, name='all_rounders_list'),
    path('laws/', laws_list, name='laws_list'),
    path('ipl/', ipl_live_data, name='ipl_data'),
    path('world cup',worlcup_live_data,name='world_cup_data'),
    path('live/',live_data,name='live_score'),
    path('ranking/',icc_rankings,name='icc_ranking'),
    path('search/', player_search, name='player_search'),
    # The Profile Page: uses the Player's ID to show their specific data
    path('player/<int:player_id>/', player_profile, name='player_profile'),
    path('compare/', compare_players, name='compare_players'),
    path('dls/', dls_calculator, name='dls_calculator'),
    path('ipl_standing/',ipl_standing,name='ipl_standing'),
    path('run-secret-scraper-123/', trigger_scraper, name='trigger_scraper'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)