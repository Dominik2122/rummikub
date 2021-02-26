from django.views.generic import TemplateView
from game.models import Game
class HomePage(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(HomePage, self).get_context_data(**kwargs)
        context['games_list'] = Game.objects.all()

        return context
