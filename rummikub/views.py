from django.views.generic import TemplateView
from game.models import Game
from django.db.models import Q
class HomePage(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(HomePage, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            context['games_list'] = Game.objects.filter(Q(player2=user) | Q(player1=user))

        return context
