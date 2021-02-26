from django.urls import path
from . import views
app_name = 'game'
urlpatterns = [
    path('<int:pk>/', views.GameDet.as_view(), name = 'game' ),
    path('create/', views.CreateGame.as_view(), name = 'create')

]
