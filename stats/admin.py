from django.contrib import admin

# Register your models here.
from .models import Player, BattingStat,BowlingStat,FieldingStat,Law,LawSubsection

# This makes your players and their stats searchable and filterable in the dashboard
@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'identifier')
    search_fields = ('name', 'identifier')

@admin.register(BattingStat)
class BattingStatAdmin(admin.ModelAdmin):
    list_display = ('player', 'format', 'runs', 'average', 'strike_rate')
    list_filter = ('format',) # This creates a filter sidebar on the right
    search_fields = ('player__name',) # Allows searching by player name

@admin.register(BowlingStat)
class BowlingStatAdmin(admin.ModelAdmin):
    list_display = ('player', 'format', 'wickets', 'economy', 'average','best_bowling_figures')
    list_filter = ('format',)
    search_fields = ('player__name',)

@admin.register(FieldingStat)
class FieldingStatAdmin(admin.ModelAdmin):
    list_display = ('player', 'format', 'dismisals', 'catch', 'stump_out','dismisals_per_inning')
    list_filter = ('format',)
    search_fields = ('player__name',)

@admin.register(Law)
class LawAdmin(admin.ModelAdmin):
    list_display = ('number', 'title')
    ordering = ('number',) # Keeps them in order 1, 2, 3...

@admin.register(LawSubsection)
class LawSubsectionAdmin(admin.ModelAdmin):
    # This creates a clean list view with columns
    list_display = ('number', 'title', 'law') 
    # This allows you to filter by the main Law (Law 1, Law 2, etc.)
    list_filter = ('law',) 
    # This adds a search bar for the content of the rules
    search_fields = ('title', 'content')