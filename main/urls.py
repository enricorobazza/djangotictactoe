from django.urls import path

from main.views.tictactoe import TicTacToeView

urlpatterns = [
    path('', TicTacToeView.index, name='index'),
    path('<str:room_name>/', TicTacToeView.room, name='room'),
]