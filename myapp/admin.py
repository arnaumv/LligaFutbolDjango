from django.contrib import admin

from django.contrib import admin
from .models import League, Team, Player, Match, Event


class EventInline(admin.TabularInline):
    model = Event
    extra = 0

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        field = super(EventInline, self).formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == 'player':
            if request._obj_ is not None:
                field.queryset = field.queryset.filter(team__in=[request._obj_.home_team, request._obj_.away_team])
            else:
                field.queryset = field.queryset.none()
        return field


class MatchAdmin(admin.ModelAdmin):
    list_display = ('home_team', 'away_team', 'league', 'date', 'result')
    inlines = [EventInline]

    def get_form(self, request, obj=None, **kwargs):
        request._obj_ = obj
        return super(MatchAdmin, self).get_form(request, obj, **kwargs)

    def result(self, obj):
        home_goals = obj.event_set.filter(type='G', player__team=obj.home_team).count()
        away_goals = obj.event_set.filter(type='G', player__team=obj.away_team).count()
        return f"{home_goals} - {away_goals}"
    result.short_description = 'Result'

class EventAdmin(admin.ModelAdmin):
    list_display = ('match', 'type', 'player', 'time')



class PlayerInline(admin.TabularInline):
    model = Player
    extra = 0

class TeamAdmin(admin.ModelAdmin):
    inlines = [PlayerInline]

admin.site.register(League)
if admin.site.is_registered(Team):
    admin.site.unregister(Team)
admin.site.register(Team, TeamAdmin)
admin.site.register(Player)
admin.site.register(Match, MatchAdmin)
admin.site.register(Event, EventAdmin)