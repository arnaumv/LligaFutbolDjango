from django.shortcuts import render, get_object_or_404
from .models import League, Match, Team, Player, Event  # Add Event here
from django.http import Http404
from django.db.models import Q  # Add this to use Q in your queries

def league_detail(request):
    leagues = League.objects.all()
    if not leagues:
        raise Http404("No leagues available.")
    league_details = []
    for league in leagues:
        matches = Match.objects.filter(league=league)
        teams = Team.objects.filter(league=league)
        league_details.append({'league': league, 'matches': matches, 'teams': teams})
    return render(request, 'league_detail.html', {'league_details': league_details})


def match_detail(request):
    matches = Match.objects.all()
    return render(request, 'match_detail.html', {'matches': matches})


def team_detail(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    matches = Match.objects.filter(Q(home_team=team) | Q(away_team=team))
    events = Event.objects.filter(match__in=matches)
    return render(request, 'team_detail.html', {'team': team, 'matches': matches, 'events': events})

def player_ranking(request, league_id):
    league = get_object_or_404(League, id=league_id)
    players = Player.objects.filter(team__in=league.teams.all()).order_by('-goals')
    return render(request, 'player_ranking.html', {'players': players})

def match_list(request, league_id=None):
    if league_id is not None:
        league = get_object_or_404(League, id=league_id)
        matches = Match.objects.filter(league=league)
    else:
        matches = Match.objects.all()
    return render(request, 'myapp/match_list.html', {'matches': matches})