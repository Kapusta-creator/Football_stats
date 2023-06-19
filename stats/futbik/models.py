import datetime

from django.db import models
# Create your models here.


class Clubs(models.Model):
    id = models.IntegerField(primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField(max_length=80, verbose_name="Название клуба")
    emblem = models.ImageField(verbose_name="Эмблема", default=None)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Клуб"
        verbose_name_plural = "Клубы"


class Players(models.Model):
    id = models.IntegerField(primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField(max_length=80)
    surname = models.CharField(max_length=80, default="")
    age = models.IntegerField(verbose_name="Возраст", null=None)
    shirtNo = models.IntegerField(verbose_name="Номер футболки", null=None)
    height = models.IntegerField(verbose_name="Рост", null=None)
    weight = models.IntegerField(verbose_name='Вес', null=None)
    club = models.ForeignKey(Clubs, on_delete=models.CASCADE, null=None, related_name="club_players")
    footed = models.CharField(max_length=10, default='right')

    def __str__(self):
        return f"{self.name} {self.surname}"

    class Meta:
        ordering = ["name", "surname"]
        verbose_name = "Игрок"
        verbose_name_plural = "Игроки"


class Championships(models.Model):
    id = models.AutoField(primary_key=True, serialize=False, verbose_name='ID')
    start_year = models.IntegerField(verbose_name='Начало чемпионата', default=1990)
    end_year = models.IntegerField(verbose_name='Конец чемпионата', default=1990)
    league = models.CharField(max_length=80, default="")
    country = models.CharField(max_length=80, default="")

    def __str__(self):
        return f"{self.country} {self.league}"

    class Meta:
        verbose_name = "Чемпионат"
        verbose_name_plural = "Чемпионаты"


class CustomDateTimeField(models.DateTimeField):
    def value_to_string(self, obj):
        val = self.value_from_object(obj)
        if val:
            val.replace(microsecond=0)
            print(val.strftime("%d-%m-%Y %HH:%MM"))
            return val.strftime("%d-%m-%Y %HH:%MM")
        return ''


class Matches(models.Model):
    id = models.IntegerField(primary_key=True, serialize=False, verbose_name='ID')
    championship = models.ForeignKey(Championships, verbose_name="Чемпионат", related_name="championship", on_delete=models.CASCADE)
    datetime = CustomDateTimeField(verbose_name="Дата и время проведения", default=datetime.datetime.fromisoformat('1900-11-04 00:05:23'))
    team1 = models.ForeignKey(Clubs, verbose_name="Команда 1", related_name='team1', on_delete=models.CASCADE, default=None)
    team2 = models.ForeignKey(Clubs, verbose_name="Команда 2", related_name='team2', on_delete=models.CASCADE, default=None)
    team1_score = models.IntegerField(verbose_name="Счет первой команды", default=0)
    team2_score = models.IntegerField(verbose_name="Счет первой команды", default=0)

    # def get_teams(self):
    #     teams_li = self.teams.all()
    #     res = []
    #     for team in teams_li:
    #         res.append(team.id)
    #     return ", ".join(res)

    # def clean(self):
    #     teams = self.cleaned_data.get('teams')
    #     if teams and teams.count() != 2:
    #         raise ValueError("Only 2 teams are allowed")
    #
    #     return self.cleaned_data

    def __str__(self):
        return f'{self.team1.name}" vs "{self.team2.name}; {str(self.datetime)}'

    class Meta:
        verbose_name = "Матч"
        verbose_name_plural = "Матчи"


class Lineup(models.Model):
    id = models.AutoField(primary_key=True, serialize=False, verbose_name="ID")
    match = models.ForeignKey(Matches, on_delete=models.CASCADE, default=None, related_name="lineup")
    player = models.ForeignKey(Players, on_delete=models.CASCADE, default=None)
    club = models.ForeignKey(Clubs, on_delete=models.CASCADE, default=None)
    is_first_eleven = models.BooleanField(default=False)
    position = models.CharField(max_length=10, default="")

    def __str__(self):
        return f"{self.club.name} {self.match.id} {self.player.name} {self.player.surname}"

    class Meta:
        verbose_name = "Состав"
        verbose_name_plural = "Составы"


class Hit(models.Model):
    match = models.ForeignKey(Matches, on_delete=models.CASCADE, default=None, related_name="hits")
    player = models.ForeignKey(Players, on_delete=models.CASCADE, default=None)
    club = models.ForeignKey(Clubs, on_delete=models.CASCADE, default=None)
    xPos = models.FloatField(default=None, verbose_name="X")
    yPos = models.FloatField(default=None, verbose_name="Y")
    distance = models.FloatField(default=None, verbose_name="Расстояние")
    angle = models.FloatField(default=90, verbose_name='Угол')
    passes_before = models.IntegerField(default=0, verbose_name='Пасы до удара')
    shots_before = models.IntegerField(default=0, verbose_name='Удары до удара')
    shots_by_team_before = models.IntegerField(default=0, verbose_name='Удары всей команды до удара')
    shooted_by = models.CharField(max_length=15, verbose_name='Чем ударил', default="Head")
    isGoal = models.BooleanField(default=False, verbose_name="Гол")

    PG = models.FloatField(default=0.5, verbose_name='predicted goal')

    def __str__(self):
        return f"Удар {self.player.name} Команда: {self.club.name} MatchId: {self.match.pk} " \
               f"x: {self.xPos} y: {self.yPos} гол: {self.isGoal}"

    class Meta:
        verbose_name = "Удар"
        verbose_name_plural = "Удары"

