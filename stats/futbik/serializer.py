from rest_framework import serializers

from .models import Players, Clubs, Matches, Championships, Lineup, Hit


class ClubSerializer(serializers.ModelSerializer):
    club_players = serializers.StringRelatedField(many=True)

    class Meta:
        model = Clubs
        fields = ['id', 'name', 'club_players']


class ClubField(serializers.PrimaryKeyRelatedField):
    def to_representation(self, value):
        pk = super(ClubField, self).to_representation(value)
        try:
            item = Clubs.objects.get(pk=pk)
            serializer = ClubSerializer(item)
            return serializer.data
        except Exception as e:
            print(e)


class ClubListingField(serializers.RelatedField):

    def to_representation(self, value):
        return {"name": value.name, "id": value.id}


class PlayerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Players
        fields = ('name', 'surname', 'age', 'id', 'club', 'height', 'weight', 'shirtNo', 'footed')

class PlayerListingField(serializers.RelatedField):

    def to_representation(self, value):
        return {'id': value.id}


class HitPlayerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Players
        fields = ['id']


class HitListingField(serializers.RelatedField):

    def to_representation(self, value):
        return {"xPos": value.xPos, 'yPos': value.yPos, 'isGoal': value.isGoal, 'club': value.club.id,
                'player': HitPlayerSerializer(value.player).data, 'PG': value.PG}


class ChampionshipSerializer(serializers.ModelSerializer):

    class Meta:
        model = Championships
        fields = ['id', 'start_year', 'end_year', 'league', 'country']


class ChampionshipRelatedField(serializers.RelatedField):

    def to_representation(self, value):
        return {"id": value.id, "name": value.name}


class ClubRelatedField(serializers.RelatedField):

    def to_representation(self, value):
        return {"id": value.id, "name": value.name}


# class ScoreRelatedField(serializers.RelatedField):
#
#     def to_representation(self, value):
#         #print(value)
#         return f"{value}"


class MatchListingField(serializers.RelatedField):

    def to_representation(self, value):
        return {"id": value.id}





class HitSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hit
        fields = ['xPos', 'yPos', 'distance', 'isGoal', 'club', 'player', 'match', 'PG']


class LineupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lineup
        fields = ['player', 'club', 'match', 'is_first_eleven', 'position', 'id']


class LineupRelatedField(serializers.RelatedField):

    def to_representation(self, value):
        return {'player': f"{value.player.name} {value.player.surname}", 'club': value.club.name,
                'club_id': value.club.id, 'is_first_eleven': value.is_first_eleven, "playerNo": value.player.shirtNo,
                'playerId': value.player.id}


class MatchSerializer(serializers.ModelSerializer):
    lineup = LineupRelatedField(many=True, default=[], read_only=True)
    hits = HitListingField(many=True, read_only=True, default=[])

    class Meta:
        model = Matches
        fields = ['id', 'datetime', 'championship', 'lineup', 'team1', 'team2', 'team1_score', 'team2_score', 'hits']


class MatchSerializerApi(serializers.ModelSerializer):
    lineup = LineupRelatedField(many=True, default=[], read_only=True)
    hits = HitListingField(many=True, read_only=True, default=[])
    team1 = ClubRelatedField(many=False, read_only=True)
    team2 = ClubRelatedField(many=False, read_only=True)

    class Meta:
        model = Matches
        fields = ['id', 'datetime', 'championship', 'lineup', 'team1', 'team2', 'team1_score', 'team2_score', 'hits']



# class ScoreSerializer(serializers.ModelSerializer):
#     #club = ClubListingField(read_only=True)
#     #match = MatchListingField(read_only=True)
#
#     class Meta:
#         model = Score
#         fields = "__all__"


