from django.db import models

# models.Model creates a class and it inherits from a class named models
# Game is inheriting models ; Model is the base class
# Anything models has, Game now has, plus whatever you add
class Game(models.Model):

    game_type = models.ForeignKey("GameType", on_delete=models.CASCADE)
    title = models.CharField(max_length=55)
    maker = models.CharField(max_length=55)
    gamer = models.ForeignKey("Gamer", on_delete=models.CASCADE)
    number_of_players = models.IntegerField()
    skill_level = models.IntegerField()