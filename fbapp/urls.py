from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.fbapp, name="fbapp"),
    path("signup/", views.signup, name="signup"),
    path("signin/", views.signin, name="signin"),
    path("signout/", views.signout, name="signout"),
    path("tankbar/", views.tankbar, name="tankbar"),
    path("bheader/", views.bheader, name="bheader"),
    path("dash/", views.dash, name="dash"),
    path("profile/", views.profile, name="profile"),
    path("teamchoice/", views.teamchoice, name="teamchoice"),
    path("teaminfo/", views.teaminfo, name="teaminfo"),
    path("playerprofile/", views.playerprofile, name="playerprofile"),
    path("playerslist/", views.playerslist, name="playerslist"),
    path("stat/", views.stat, name="stat"),
    path("article/<int:articleID>", views.article, name="article"),
    path("articles/", views.articles, name="articles"),
    path("arthelper/", views.arthelper, name="arthelper"),
    path("makeart/", views.makeart, name="makeart"),
    path("deleteart/", views.deleteart, name="deleteart"),
    path("games/", views.games, name="games"),
    path("gameperweek/", views.gameperweek, name="gameperweek"),
    path("playbyplay/",views.playbyplay, name="playbyplay"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
