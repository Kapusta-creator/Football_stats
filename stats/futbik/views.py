from django.shortcuts import render, redirect

from django.views.generic import TemplateView, FormView, CreateView, UpdateView

from rest_framework import viewsets, permissions
from rest_framework import generics
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializer import PlayerSerializer, ClubSerializer, MatchSerializer, ChampionshipSerializer, HitSerializer, LineupSerializer, MatchSerializerApi
from .models import Players, Clubs, Matches, Championships, Hit, Lineup
# Create your views here.


class PlayersView(TemplateView):
    template_name = "players.html"

    def get(self, request):
        players = Players.objects.filter()
        ctx = {'players': players}
        return render(request, self.template_name, ctx)


class PlayersViewSet(viewsets.ModelViewSet):
    queryset = Players.objects.all().order_by('id')
    serializer_class = PlayerSerializer


class ClubsViewSet(viewsets.ModelViewSet):
    queryset = Clubs.objects.all().order_by('name')
    serializer_class = ClubSerializer


class MatchViewSet(viewsets.ModelViewSet):
    queryset = Matches.objects.all()
    serializer_class = MatchSerializer
    serializer_class_api = MatchSerializerApi

    def serialize_matches_api(self, matches):
        matches_response = []
        for match in matches:
            match_to_response = {}
            serialized_match = self.serializer_class_api(match).data
            match_to_response['datetime'] = serialized_match['datetime']
            match_to_response['id'] = serialized_match['id']
            match_to_response['lineup'] = {}
            match_to_response['lineup'][serialized_match['team1']['id']] = []
            match_to_response['lineup'][serialized_match['team2']['id']] = []
            for player in serialized_match['lineup']:
                match_to_response['lineup'][player['club_id']].append({'player_name': player['player'],
                                                                       'is_first_eleven': player['is_first_eleven'],
                                                                       'playerNo': player['playerNo'], 'id': player['playerId']})
            match_to_response['hits'] = {}
            match_to_response['hits'][serialized_match['team1']['id']] = []
            match_to_response['hits'][serialized_match['team2']['id']] = []
            team1_predicted_score = 0
            team2_predicted_score = 0
            for hit in serialized_match['hits']:
                match_to_response['hits'][hit['club']].append({"xPos": hit['xPos'], "yPos": hit['yPos'],
                                                               'isGoal': hit['isGoal'],
                                                               'player': hit['player']['id'], 'PG': round(hit['PG'], 2)})
                if hit['club'] == serialized_match['team1']['id']:
                    team1_predicted_score += round(hit['PG'], 2)
                else:
                    team2_predicted_score += round(hit['PG'], 2)
            match_to_response['team1'] = serialized_match['team1']
            match_to_response['team2'] = serialized_match['team2']
            match_to_response["team1_score"] = serialized_match['team1_score']
            match_to_response["team2_score"] = serialized_match['team2_score']
            match_to_response['team1_predicted_score'] = round(team1_predicted_score, 2)
            match_to_response['team2_predicted_score'] = round(team2_predicted_score, 2)
            matches_response.append(match_to_response)
        return matches_response

    def serialize_matches(self, matches):
        data = []
        for match in matches:
            data.append(self.serializer_class(match).data)
        return data

    @action(detail=False, methods=['get'], url_path="(?P<date_from>\d{4}-\d\d-\d\d)/(?P<date_to>\d{4}-\d\d-\d\d)")
    def get_by_date(self, request, date_from=None, date_to=None):
        if request.method == "GET":
            matches_data = self.queryset.filter(
                datetime__range=[date_from + " 00:00:00", date_to + " 23:59:59"],
            )
            return Response(data=self.serialize_matches_api(matches_data))

    @action(detail=False, methods=['get'], url_path='last/(?P<last>\d+)')
    def get_n_last(self, request, last):
        if request.method == "GET":
            matches_data = self.queryset.order_by('-datetime')[:int(last)]
            return Response(data=self.serialize_matches_api(matches_data))

    #@action(detail=True, methods=['patch'], url_path='update_predict/(?P<match_id>\d+)')
    #def post_by_match(self, request, match_id=None):
    #    if request.method == "PATCH":



class ChampionshipViewSet(viewsets.ModelViewSet):
    queryset = Championships.objects.all()
    serializer_class = ChampionshipSerializer

    def serialize_championships(self, championships):
        data = []
        for match in championships:
            data.append(self.serializer_class(match).data)
        return data

    @action(detail=False, methods=['get'], url_path="name/(?P<championship_name>).+")
    def get_by_name(self, request, championship_name=None):
        if request.method == "GET":
            championships_data = self.queryset.filter(
                name=championship_name
            )
            data = []
            for championship in championships_data:
                data.append(self.serializer_class(championship).data)
            return Response(data=data)

    @action(detail=False, methods=['get'], url_path="start_year/(?P<start_year>\d+)")
    def get_by_year(self, request, start_year=None):
        if request.method == "GET":
            championship_data = self.queryset.filter(
                start_year=int(start_year)
            )
            return Response(data=self.serialize_championships(championship_data))


class ChampionshipList(generics.ListAPIView):
    serializer_class = ChampionshipSerializer

    def get_queryset(self):
        data = dict(self.request.query_params)
        for key, item in data.items():
            if key == 'id':
                data['id'] = int(item[0])
            elif key == 'start_year':
                data['start_year'] = int(item[0])
            elif key == 'end_year':
                data['end_year'] = int(item[0])
            else:
                data[key] = item[0]
        queryset = Championships.objects.filter(**data)
        return queryset


class LineupList(generics.ListAPIView):
    serializer_class = LineupSerializer

    def get_queryset(self):
        data = dict(self.request.query_params)
        for key, item in data.items():
            data[key] = int(item[0])
        queryset = Lineup.objects.filter(**data)
        return queryset


class HitViewSet(viewsets.ModelViewSet):
    queryset = Hit.objects.all()
    serializer_class = HitSerializer
    #permission_classes = (permissions.AllowAny, )

    @action(detail=False, methods=['get'], url_path="by_match_id/(?P<match_id>\d+)")
    def get_by_match(self, request, match_id=None):
        if request.method == "GET":
            hits = self.queryset.prefetch_related('lineup__player', 'lineup__club', 'lineup__match').filter(
                lineup__match__id=match_id
            )
            data = []
            for hit in hits:
                data.append(self.serializer_class(hit).data)
            return Response(data=data)

    @action(detail=False, methods=['get'], url_path="by_player_id/(?P<player_id>\d+)")
    def get_by_player(self, request, player_id=None):
        if request.method == "GET":
            hits = self.queryset.filter(
                lineup__player__id=player_id
            )
            data = []
            for hit in hits:
                data.append(self.serializer_class(hit).data)
            return Response(data=data)

    # @action(detail=True, methods=['post'], url_path='predicted_hit')
    # def post_predicted(self, request):
    #     if request.method == 'POST':
    #         print(request.data)
    #     return Response(data=request.data)


class LineupViewSet(viewsets.ModelViewSet):
    queryset = Lineup.objects.all()
    serializer_class = LineupSerializer


class MainView(TemplateView):
    template_name = "futbik_main.html"

    def get(self, request):
        return render(request, self.template_name, {})


class MapView(TemplateView):
    template_name = "test_map.html"

    def get(self, request):
        return render(request, self.template_name, {})
