from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, View, DetailView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from . import models
from django.http import HttpResponse, HttpResponseRedirect
from django.http import request
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.http import JsonResponse

CurrentUser = get_user_model()
import random
# Create your views here.
class GameView(LoginRequiredMixin, TemplateView):
    template_name = 'game.html'


class CreateGame(LoginRequiredMixin, CreateView):
    model = models.Game
    fields = ['player1', 'player2']
    template_name = 'game_create.html'
    def get_success_url(self):
        game = models.Game.objects.get(pk=int(self.object.pk))
        if not game.tiles.exists():
            for i in ['red', 'blue', 'yellow', 'black']:
                for j in range(13):
                    tile = models.Tile(color=i, number = int(int(j)+1), pos_top = 1, pos_left = 1)
                    tile.save()
                    nr = tile.pk
                    tile = models.Tile.objects.get(pk=nr)
                    game.tiles.add(tile)
                    game.save()
            tiles = game.tiles.all()
            list_of_tiles = list(tiles)
            random.shuffle(list_of_tiles)
            for i in range(26):
                x = list_of_tiles.pop()
                if i % 2 ==0:
                    x.pos_left = 2
                    x.pos_top = 2
                    game.p1_tiles.add(x)
                else:
                    x.pos_left = 3
                    x.pos_top = 3
                    game.p2_tiles.add(x)
        return reverse("game:game", kwargs={"pk":self.object.pk})





class GameDet(LoginRequiredMixin, DetailView):
    model = models.Game
    template_name = 'game.html'


    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            if 'position[top]' in request.GET:
                top = request.GET['position[top]']
                left = request.GET['position[left]']
                tileId = request.GET['tile']
                tile = models.Tile.objects.get(id = tileId)
                tile.pos_left = left
                tile.pos_top = top
                tile.save()
            tiles = self.get_object().tiles.all()
            tiles_positions = []
            for tile in tiles:
                top = str(tile.pos_top)
                left = str(tile.pos_left)
                tile_id = str(tile.pk)
                if top != '1' and top != '2' and top != '3':
                    tiles_positions.append([top, left, tile_id])

            return JsonResponse({'tiles_positions':tiles_positions})



        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        game = models.Game.objects.get(pk=int(self.kwargs['pk']))
        context = super(GameDet, self).get_context_data(**kwargs)
        context['game'] = game
        context['player1'] = game.player1
        context['p1_tiles'] = game.p1_tiles.all()
        context['player1'] = game.player1
        context['p1_tiles'] = game.p1_tiles.all()
        context['tiles'] = game.tiles.all()
        return context
