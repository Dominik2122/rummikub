from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.
from django.contrib.auth import get_user_model
CurrentUser = get_user_model()

from django import template
register = template.Library()


class Tile(models.Model):
    number = models.CharField(max_length=5)
    color = models.CharField(max_length=20)
    visible = models.BooleanField(default=False)
    pos_left = models.CharField( default=  "", blank=True, max_length=15)
    pos_top = models.CharField( default = "",  blank=True, max_length=15)


class Game(models.Model):
    date = models.DateField(auto_now_add=True)
    player1 = models.ForeignKey(User, related_name="player1", on_delete=models.CASCADE)
    player2 = models.ForeignKey(User, related_name = 'player2', on_delete=models.CASCADE)
    tiles = models.ManyToManyField(Tile, blank = True, related_name = 'tiles')
    p1_tiles = models.ManyToManyField(Tile, blank = True, related_name = 'p1_tiles')
    p2_tiles = models.ManyToManyField(Tile, blank = True, related_name = 'p2_tiles')


    def get_absolute_url(self):
        return reverse('home')
