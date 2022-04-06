from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def index(request):
    return render(request, 'menus/index.html')


@login_required
def games(request):
    return render(request, 'menus/games.html')
