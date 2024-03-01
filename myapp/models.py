from django.db import models

class League(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=200)
    league = models.ForeignKey(League, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.league.name})"


class Player(models.Model):
    name = models.CharField(max_length=200)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    number = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.team.name})"


class Match(models.Model):
    date = models.DateTimeField()
    home_team = models.ForeignKey(Team, related_name='home_matches', on_delete=models.CASCADE)
    away_team = models.ForeignKey(Team, related_name='away_matches', on_delete=models.CASCADE)
    league = models.ForeignKey(League, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.home_team.name} vs {self.away_team.name} ({self.date.strftime('%Y-%m-%d')}) - {self.result()}"

    def result(self):
        home_goals = self.event_set.filter(type='G', player__team=self.home_team).count()
        away_goals = self.event_set.filter(type='G', player__team=self.away_team).count()
        return f"{home_goals} - {away_goals}"

class Event(models.Model):
    EVENT_TYPES = (
        ('G', 'Goal'),
        ('Y', 'Yellow Card'),
        ('R', 'Red Card'),
        ('F', 'Foul'),
    )
    type = models.CharField(max_length=1, choices=EVENT_TYPES)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    time = models.TimeField()

    def __str__(self):
        return f"{self.get_type_display()} by {self.player.name} at {self.time}"