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
import random

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
            for i in ['red', 'blue', '#ffaa00', 'black']:
                for j in range(13):
                    tile = models.Tile(color=i, number = int(int(j)+1), pos_top = 1, pos_left = 1)
                    tile.save()
                    nr = tile.pk
                    tile = models.Tile.objects.get(pk=nr)
                    game.tiles.add(tile)
                    game.save()
                for j in range(13):
                    tile = models.Tile(color=i, number = int(int(j)+1), pos_top = 1, pos_left = 1)
                    tile.save()
                    nr = tile.pk
                    tile = models.Tile.objects.get(pk=nr)
                    game.tiles.add(tile)
                    game.save()
            joker1 = models.Tile(color = 'red', number="J", pos_left=1, pos_top=1)
            joker2 = models.Tile(color = 'black', number="J", pos_left=1, pos_top=1)
            joker1.save()
            joker2.save()
            game.tiles.add(joker1)
            game.tiles.add(joker2)
            game.save()
            x = random.randint(0, 2)
            if x==0:
                game.start_player = game.player1
            else:
                game.start_player = game.player2
            game.save()
            tiles = game.tiles.all()
            list_of_tiles = list(tiles)
            random.shuffle(list_of_tiles)
            for i in range(26):
                x = list_of_tiles.pop()
                if i % 2 ==0:
                    x.pos_left = 2
                    x.pos_top = 2
                    x.save()
                    game.p1_tiles.add(x)
                else:
                    x.pos_left = 3
                    x.pos_top = 3
                    x.save()
                    game.p2_tiles.add(x)
            game.save()
        return reverse("game:game", kwargs={"pk":self.object.pk})


class GameDet(LoginRequiredMixin, DetailView):
    model = models.Game
    template_name = 'game.html'

    def get(self, request, *args, **kwargs):
        game = self.get_object()
        start_player = game.start_player
        if request.is_ajax():
            if 'lewa' in request.GET:
                top = request.GET['gora']
                left = request.GET['lewa']
                tileId = request.GET['tid']
                prevTile = game.tiles.filter(last = True)
                if len(list(prevTile)) != 0:
                    prevTile = prevTile.first()
                    prevTile.last = False
                    prevTile.save()

                tile = models.Tile.objects.get(id=tileId)
                tile.last = True
                if tile.pos_top == '2':
                    tile.last_left = "2"
                    tile.last_top = "2"
                elif tile.pos_top == '3':
                    tile.last_left = "3"
                    tile.last_top = "3"
                elif tile.pos_top == '1':
                    tile.last_left = '1'
                    tile.last_top = "1"
                else:
                    tile.last_left = left
                    tile.last_top = top

                tile.save()
                prev_tile_id = str(tile.pk)
            prev_tile_id = None
            if 'left' in request.GET and request.user == start_player:
                top = request.GET['to']
                left = request.GET['left']
                tileId = request.GET['t']
                tile = models.Tile.objects.get(id = tileId)
                if tile.pos_top == "1" and self.request.user == game.player1:
                    tile.pos_top = "2"
                    tile.pos_left ="2"
                    tile.save()
                    game.p1_tiles.add(tile)
                    game.save()
                elif tile.pos_top == '1' and  self.request.user == game.player2:
                    tile.pos_top = "3"
                    tile.pos_left = "3"
                    tile.save()
                    game.p2_tiles.add(tile)
                    game.save()
                else:
                    tile.pos_left = left
                    tile.pos_top = top
                    tile.save()
            if 'p' in request.GET and request.user == start_player:
                if request.user == game.player1:
                    game.start_player = game.player2
                else:
                    game.start_player = game.player1
                game.save()


            if 'undo' in request.GET and request.user == start_player:
                prevTile = game.tiles.filter(last = True)
                if len(list(prevTile)) != 0:
                    prev_tile = game.tiles.filter(last=True).first()
                    prev_tile.pos_top = prev_tile.last_top
                    prev_tile.pos_left = prev_tile.last_left
                    prev_tile.last = False

                    prev_tile.save()

            tiles = self.get_object().tiles.all()
            tiles_positions = []
            for tile in tiles:
                top = str(tile.pos_top)
                left = str(tile.pos_left)
                tile_id = str(tile.pk)
                color = str(tile.color)
                number = str(tile.number)
                if top == '2':
                    tiles_positions.append([top, left, tile_id, color, number, 'p1'])
                elif top == '3':
                    tiles_positions.append([top, left, tile_id, color, number, 'p2'])
                elif top != '1':
                    tiles_positions.append([top, left, tile_id, color, number, 'tb'])
                else:
                    tiles_positions.append([top, left, tile_id, color, number, 'un'])




            if request.user != start_player:
                refresh_info = True
            else:
                refresh_info = False

            return JsonResponse({'tiles_positions':tiles_positions,
                                'currentPlayer':start_player.username,
                                'refresh_info':refresh_info,
                                'prev_tile': prev_tile_id})



        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        game = models.Game.objects.get(pk=int(self.kwargs['pk']))
        context = super(GameDet, self).get_context_data(**kwargs)
        context['game'] = game
        context['user'] = self.request.user
        context['player1'] = game.player1
        context['p1_tiles'] = game.p1_tiles.all()
        context['player2'] = game.player2
        context['p2_tiles'] = game.p2_tiles.all()
        context['tiles'] = game.tiles.all()
        return context
