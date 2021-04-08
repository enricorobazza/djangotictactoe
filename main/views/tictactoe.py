from django.shortcuts import render

class TicTacToeView():
    def index(request):
        return render(request, "tictactoe/index.html", {})

    def room(request, room_name):
        return render(request, 'tictactoe/room.html', {'room_name': room_name})
