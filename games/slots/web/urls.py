from django.urls import path

from games.slots.web import views

urlpatterns = [
    path('session/<uuid:session>', views.SlotsSession.as_view(), name='slots_game')
]
