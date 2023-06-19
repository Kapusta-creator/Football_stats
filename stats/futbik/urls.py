from django.urls import path, include, register_converter
from rest_framework import routers
from datetime import date, datetime

from . import views, api


class DateConverter:
    regex = r"\d{4}-\d{1,2}-\d{1,2}"
    format = "%Y-%m-%d"

    def to_python(self, value: str) -> date:
        return datetime.strptime(value, self.format).date()

    def to_url(self, value: date) -> str:
        return value.strftime(self.format)


register_converter(DateConverter, "date")



router = routers.DefaultRouter()
router.register(r'players', views.PlayersViewSet)
router.register(r'clubs', views.ClubsViewSet)
router.register(r'matches', views.MatchViewSet)
router.register(r'championships', views.ChampionshipViewSet)
router.register(r'hits', views.HitViewSet)
router.register(r'lineups', views.LineupViewSet)
#router.register(r'championship_list', views.ChampionshipList)






urlpatterns = [
    path('', views.MainView.as_view()),
    path('api/', include(router.urls)),
    path('players/', views.PlayersView.as_view()),
    path('map/', views.MapView.as_view()),
    path('api/all_matches', api.all_matches),
    path('api/championship_list', views.ChampionshipList.as_view()),
    path('api/lineup_list', views.LineupList.as_view()),
    path('api/predicted_hit/', api.post_predicted_hit),
    #path('api/matches/get/<date:date_from>/<date:date_to>', views.MatchViewSet.as_view())
]
#/api/lineup_list?match=1647698&player=146780
