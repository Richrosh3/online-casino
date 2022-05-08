from django.urls import path

from games.craps.web import views

urlpatterns = [
    path('session/<uuid:session>', views.CrapsSession.as_view(), name='craps_game')
]
