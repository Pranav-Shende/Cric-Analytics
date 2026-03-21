from django.db import models

# Create your models here.    
class Player(models.Model):
    name = models.CharField(max_length=200)
    identifier = models.CharField(max_length=100, unique=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='player_pics/', default='player_pics/default.png')
    # ai_bio
    ai_bio = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.country})"
    
class BattingStat(models.Model):
    # Linking this stat to a specific player
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='batting_stats')
    format = models.CharField(max_length=20) # Test, ODI, T20I, IPL, etc.
    matches = models.IntegerField(default=0)
    innings = models.IntegerField(default=0)
    runs = models.IntegerField(default=0)
    average = models.FloatField(null=True, blank=True)
    strike_rate = models.FloatField(null=True, blank=True)
    is_league = models.BooleanField(default=False) # To separate IPL from International
    rank = models.IntegerField(null=True, blank=True)
    centuries = models.IntegerField(default=0, db_column='100')
    half_centuries = models.IntegerField(default=0, db_column='50')
    highest_score = models.CharField(max_length=10, default='0', blank=True, null=True)
    ducks= models.IntegerField(default=0)
    fours=models.IntegerField(default=0)
    sixes=models.IntegerField(default=0)
    not_out=models.IntegerField(default=0)
    span= models.CharField(max_length=10, default='0', blank=True, null=True)

    def __str__(self):
        return f"{self.player.name} - {self.format}"
   
class BowlingStat(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='bowling_stats')
    format = models.CharField(max_length=10)  # Test, ODI, T20I
    matches = models.IntegerField(default=0)
    innings = models.IntegerField(default=0)
    overs = models.FloatField(default=0.0)
    wickets = models.IntegerField(default=0)
    average = models.FloatField(null=True, blank=True)
    economy = models.FloatField(null=True, blank=True)
    best_bowling_figures = models.CharField(max_length=20, null=True, blank=True) # e.g., "5/19"
    balls= models.IntegerField(default=0)
    span=models.CharField(max_length=10, default='0', blank=True, null=True)
    runs = models.IntegerField(default=0)
    strike_rate = models.FloatField(null=True, blank=True)
    four_wic=models.IntegerField(default=0)
    five_wic= models.IntegerField(default=0)

    def __str__(self):
        return f"{self.player.name} - {self.format} Bowling"  
    
class FieldingStat(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='fielding_stats')
    format = models.CharField(max_length=10)  # Test, ODI, T20I
    matches = models.IntegerField(default=0)
    innings = models.IntegerField(default=0)
    catch = models.IntegerField(default=0.0)
    stump_out = models.IntegerField(default=0)
    dismisals = models.IntegerField(default=0)
    dismisals_per_inning = models.FloatField(null=True, blank=True)
    span=models.CharField(max_length=10, default='0', blank=True, null=True)

    def __str__(self):
        return f"{self.player.name} - {self.format} Fielding"  
    
    
# stats/models.py
class AllRounderStat(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    format = models.CharField(max_length=20) # e.g., Test, ODI, T20I
    all_rounder_rating = models.FloatField()
    runs_bat = models.IntegerField(default=0)
    innings_bat = models.IntegerField(default=0)
    innings_bowl = models.IntegerField(default=0)
    wickets = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.player.name} - {self.format}"
    
class Law(models.Model):
    number = models.IntegerField(unique=True)
    title = models.CharField(max_length=200)

    def __str__(self):
        return f"Law {self.number}: {self.title}" 
     
class LawSubsection(models.Model):
    law = models.ForeignKey(Law, related_name='subsections', on_delete=models.CASCADE)
    number = models.CharField(max_length=10) # e.g., "1.1"
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        # This shows "1.1: Number of players" in the admin
        return f"{self.number}: {self.title}"
    


