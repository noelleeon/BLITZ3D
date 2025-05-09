###############################################
# Filename: views.py                          #
# Purpose: The backend to handle the logic of #
# all the different views/urls that get called#
###############################################
import os
import json
import random
import traceback
import requests
import nfl_data_py as nfl
import pytz
from datetime import datetime, timezone
import asyncio
from django.db import models
from django.contrib import messages
from fbapp.models import Member, Articles
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpRequest, StreamingHttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.template import loader
from django.core.cache import cache
from django import template
from dotenv import load_dotenv
import openai
from openai import OpenAI
from channels.routing import ProtocolTypeRouter
from typing import AsyncGenerator
from bs4 import BeautifulSoup
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# https://medium.com/@resshin24/how-to-connect-the-mysql-database-in-python-django-9433a243da8e
# ^^^ How to use the mysql db in my views.py file

#https://www.geeksforgeeks.org/using-python-environment-variables-with-python-dotenv/
load_dotenv()
#https://github.com/Kouidersif/openai-API/blob/main/openapp/views.py
#https://www.geeksforgeeks.org/openai-python-api/
client = OpenAI(api_key=os.environ.get(""))

#https://stackoverflow.com/questions/1070398/how-to-assign-a-value-to-a-variable-in-a-django-template
register = template.Library()

# https://www.geeksforgeeks.org/user-authentication-system-using-django/
###################################################
# Function: fbapp                                 #///////////////////////////////////
# Description: This is the landing page of my app #/////////////////////////////////
# Parameters: request (to request to html)        #//////////////////////////////////
# Return value: render -> rendered html file      #/////////////////////////////////
###################################################
def fbapp(request):
    return render(request, "myfirst.html")

###################################################
# Function: signup                                #////////////////////////////////////
# Description: this collects a form and signs the #///////////////////////////////////
# user up. If valid the page directs to dash if   #////////////////////////////////
# not valid the page directs to the home page.    #///////////////////////////////////
# Parameters: request (to request the html)       #//////////////////////////////////
# Return value: redirect -> to another route      #/////////////////////////////////////
###################################################
# https://forum.djangoproject.com/t/how-do-i-make-signup-page-available-only-for-logged-in-staff-users-in-django-allauth/12868/3
# https://www.geeksforgeeks.org/user-authentication-system-using-django/
@csrf_protect
def signup(request):
    if request.method == 'POST':
        print("the request is post")
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not username or not password:
            return render(request, "myfirst.html")
        #https://stackoverflow.com/questions/3090302/how-do-i-get-the-object-if-it-exists-or-none-if-it-does-not-exist-in-django
        if Member.objects.filter(username=username).exists():
            messages.error(request, "Snooze you lose! Choose a different username")
            return render(request, "signup.html")
        #https://stackoverflow.com/questions/41332528/how-to-hash-django-user-password-in-django-rest-framework
        #https://stackoverflow.com/questions/25098466/how-to-store-django-hashed-password-without-the-user-object
        try:
            hashpass = make_password(password)
            user = Member(username=username)
            user.set_password(password)
            user.save()
        #https://stackoverflow.com/questions/2293291/create-a-session-in-django
            messages.success(request, "You've been drafted! Play hard")
            login(request, user)
            return redirect('dash')
        except Exception as e:
            error_message = f"Error: {str(e)}\n{traceback.format_exc()}"
            messages.error(request, error_message)
            #messages.error(request, f"Error: {str(e)}")
            return render(request, "myfirst.html")

###################################################
# Function: signin                                #//////////////////////////////
# Description: this collects a form and signs the #//////////////////////////////
# user in. If valid the page directs to dash if   #////////////////////////////
# not valid the page directs to the home page.    #
# Parameters: request (to request the html)       #
# Return value: redirect -> to another route      #
###################################################
@csrf_protect
def signin(request): 
    # if the http method is post grab the entered username and password
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        #https://docs.djangoproject.com/en/5.1/topics/auth/default/#:~:text=To%20log%20a%20user%20in,session%2C%20using%20Django's%20session%20framework.
        user = authenticate( request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.info(request, "Touchdown! Don't fumble this.")
            return redirect('dash')
        else:
            messages.info(request, "Either the user doesn't exist or you forgot your password.")
            return render(request, "myfirst.html")

###################################################
# Function name: signout                          #
# Description: Signs the user out and clears sess #
# Parameters: request                             #
# Return value: redirects to signin               #
###################################################
#https://stackoverflow.com/questions/76644005/request-session-clear-vs-request-session-flush-in-django
@login_required
def signout(request):
    if request.method == 'POST':
        logout(request)
        request.session.flush()
        return redirect('fbapp')

############################################################################################
##########################         TANK BAR        #########################################
############################################################################################
###################################################
# Function name: searchnav                        #
# Description: this is the ai bot named tank      #
# Parameters: Request                             #
# Return value: answer about a given question.    #
###################################################
#https://community.openai.com/t/questions-about-assistant-threads/485239
#Provided from code section of the openAI project
#https://platform.openai.com/docs/overview?lang=python
#https://stackoverflow.com/questions/77444332/openai-python-package-error-chatcompletion-object-is-not-subscriptable
@csrf_exempt
@login_required
def tankbar(request):
    answer = None
    print(request.method)
    if request.method == 'POST':
        try:
            if not request.body:
                return JsonResponse({'error_message': 'Empty request body'}, status=400)
            print(request.body)
            data = json.loads(request.body)
            question = data.get("question")
            completion = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                {"role":"system","content":"You are a helpful assistant who answers only questions about American football, anything ranging to players, news, teams, history, or statistics. You talk like an American football coach who talks a lot of smack. If someone asks you about anything other than American football you tell them to get lost."},
                {"role":"user","content":question}]
            )
            complete_dict = completion.model_dump()
            answer = complete_dict['choices'][0]['message']['content']
            return JsonResponse({'answer':answer})
        except Exception as e:
            error_message = f"Error: {str(e)}\n{traceback.format_exc()}"
            return JsonResponse({'error_message': error_message}, status=500)
    return JsonResponse({'message':'yo'}, status=200)

#############################################################################################
##########################          HEADER         ##########################################
#############################################################################################
###################################################
# Function name: bheader                          #
# Description: Requests to build the header bar   #
# Parameters: request                             #
# Return value: redirects to the header bar       #
###################################################
@login_required
def bheader(request):
    return render(request, "bheader.html")

#############################################################################################
##########################        DASHBOARD        ##########################################
#############################################################################################
###################################################
# Function name: dash                             #
# Description: Requests to build the dashboard    #
# Parameters: request                             #
# Return value: redirects to the dashboard        #
###################################################
@login_required
def dash(request):
    return render(request, "dashboard.html")

#Not utilized right now
@login_required
def profile(request):
    return render(request, "profile.html")

###################################################
# Function name: teamchoice                       #
# Description: Takes gameID and returns team stats#
# Parameters: request                             #
# Return value: sends data to the stat page       #
###################################################
#https://reintech.io/blog/connecting-to-external-api-in-django
@login_required
def teamchoice(request):
    return render(request, "stats.html")

@login_required
def teaminfo(request):
    if request.method == "POST":
        data = json.loads(request.body)
        nowteam = str(data.get("team"))
        url = "https://tank01-nfl-live-in-game-real-time-statistics-nfl.p.rapidapi.com/getNFLTeams"
        querystring = {"sortBy":"standings","rosters":"false","schedules":"false","topPerformers":"true","teamStats":"true"}
        headers = {
             ,  
        }
#https://stackoverflow.com/questions/12353288/getting-values-from-json-using-python
#https://stackoverflow.com/questions/59074990/how-to-iterate-through-json-object-in-python-and-get-key
        response = requests.get(url, headers=headers, params=querystring)
        startr = response.json()
        teamInfo = {}
        teamsbody = startr.get('body', [])
        for team in teamsbody:
            if str(team['teamID']) == nowteam:
                # General team stuff for top of team card   
                teamstats = team['teamStats']
                rushing = teamstats['Rushing']
                kicking = teamstats['Kicking']
                passing = teamstats['Passing']
                punting = teamstats['Punting']
                receiving = teamstats['Receiving']
                defense = teamstats['Defense']
                teamInfo = {
                   'nflComLogo1': team['nflComLogo1'].rstrip('/'),
                   'teamName': team['teamName'],
                   'teamAbv': team['teamAbv'],
                   'teamCity': team['teamCity'],
                   'conferenceAbv': team['conferenceAbv'],
                   'division': team['division'],
                   'rushYds': rushing['rushYds'],
                   'carries': rushing['carries'],
                   'rushTD': rushing['rushTD'],
                   'fgAttempts': kicking['fgAttempts'],
                   'fgMade': kicking['fgMade'],
                   'xpMade': kicking['xpMade'],
                   'fgYds': kicking['fgYds'],
                   'kickYards': kicking['kickYards'],
                   'xpAttempts': kicking['xpAttempts'],
                   'passAttempts': passing['passAttempts'],
                   'passTD': passing['passTD'],
                   'passYds': passing['passYds'],
                   'intercept': passing['int'],
                   'passCompletions': passing['passCompletions'],
                   'puntYds': punting['puntYds'],
                   'punts': punting['punts'],
                   'receptions': receiving['receptions'],
                   'recTD': receiving['recTD'],
                   'targets': receiving['targets'],
                   'recYds': receiving['recYds'],
                   'fumblesLost': defense['fumblesLost'],
                   'defTD': defense['defTD'],
                   'fumblesRecovered': defense['fumblesRecovered'],
                   'qbHits': defense['qbHits'],
                   'passDeflections': defense['passDeflections'],
                   'totalTackles': defense['totalTackles'],
                   'defensiveInterceptions': defense['defensiveInterceptions'],
                   'rushingYardsAllowed': defense['rushingYardsAllowed'],
                   'sacks': defense['sacks'],
                   'rushingTDAllowed': defense['rushingTDAllowed'],
                }
                break
        return JsonResponse({'teamInfo':teamInfo})
    return JsonResponse({'error':'Post method missing'}, status=405)
    
###################################################
# Function name: playerprofile                    #
# Description: Grabs every player and build a row #
# of grabbed data for each. Also uses pagination  #
# Parameters: request                             #
# Return value: array of player infos and stat pag#
###################################################    
@login_required
def playerprofile(request):
    #Url and header for grabbing single player from different api
        #https://medium.com/geekculture/web-scraping-tables-in-python-using-beautiful-soup-8bbc31c5803e
        #https://stackoverflow.com/questions/34144389/how-to-get-value-from-tables-td-in-beautifulsoup
    if request.method == 'POST':
        playerInfo = []
        #https://stackoverflow.com/questions/39376164/how-to-treat-uppercase-and-lowercase-words-the-same-in-python
        data = json.loads(request.body)
        playerID = str(data.get("playerID", "")).lower()
        url = "https://tank01-nfl-live-in-game-real-time-statistics-nfl.p.rapidapi.com/getNFLPlayerInfo"
        querystring = {"playerID":playerID,"getStats":"true"}
        headers = {
            ,
        }
        response = requests.get(url, headers=headers, params=querystring)
        respp = response.json()
        resp = respp['body']
        respo = resp.get('stats', {})
        playerInfo = {
            "espnHeadshot": resp.get('espnHeadshot', ''),
            "espnName": resp.get('espnName', ''),
            "weight": resp.get('weight', ''),
            "jerseyNum": resp.get('jerseyNum', ''),
            "team": resp.get('team', ''),
            "age": resp.get('age', ''),
            "pos": resp.get('pos', ''),
            "fantasyLink": resp.get('fantasyProsLink', ''),
            "rushYds": respo.get('Rushing', {}).get('rushYds', 0),
            "carries": respo.get('Rushing', {}).get('carries', 0),
            "rushTD": respo.get('Rushing', {}).get('rushTD', 0),
            "passAttempts": respo.get('Passing', {}).get('passAttempts', 0),
            "passTD": respo.get('Passing', {}).get('passTD', 0),
            "passYds": respo.get('Passing', {}).get('passYds', 0),
            "intr": respo.get('Passing', {}).get('int', 0),
            "passCompletions": respo.get('Passing', {}).get('passCompletions', 0),
            "receptions": respo.get('Receiving', {}).get('receptions', 0),
            "recTD": respo.get('Receiving', {}).get('recTD', 0),
            "targets": respo.get('Receiving', {}).get('targets', 0),
            "recYds": respo.get('Receiving', {}).get('recYds', 0),
            "totalTackles": respo.get('Defense', {}).get('totalTackles', 0),
            "fumblesLost": respo.get('Defense', {}).get('fumblesLost', 0),
            "fumblesRecovered": respo.get('Defense', {}).get('fumblesRecovered', 0),
            "defTD": respo.get('Defense', {}).get('defTD', 0),
            "soloTackles": respo.get('Defense', {}).get('soloTackles', 0),
            "defensiveInterceptions": respo.get('Defense', {}).get('defensiveInterceptions', 0),
            "qbHits": respo.get('Defense', {}).get('qbHits', 0),
            "passDeflections": respo.get('Defense', {}).get('passDeflections', 0),
            "sacks": respo.get('Defense', {}).get('sacks', 0),
        }
        return JsonResponse({"player":playerInfo})
    return JsonResponse({'error':'Post method missing'}, status=405)

###################################################
# Function name: playerchoice                     #
# Description: Requests to build the header bar   #
# Parameters: request                             #
# Return value: redirects to the header bar       #
###################################################
@login_required
def playerslist(request):
    if request.method == 'POST':
        #https://stackoverflow.com/questions/39376164/how-to-treat-uppercase-and-lowercase-words-the-same-in-python
        data = json.loads(request.body)
        usertext = str(data.get("usertext", "")).lower()
        userteam = data.get("userteam", "")
        userposition = str(data.get("userposition", "")).lower()
        usersort = str(data.get("usersort", "")).lower()
        url = "https://tank01-nfl-live-in-game-real-time-statistics-nfl.p.rapidapi.com/getNFLPlayerList"
        headers = {
            ,
        }
        response = requests.get(url, headers=headers)
        resp = response.json()
        playerrespo = resp['body']
        playersInfo = []
        for player in playerrespo:
            namematch = not usertext or usertext in (str(player['espnName'])).lower()
            teammatch = not userteam or userteam == player['teamID']
            positionmatch = not userposition or userposition in (str(player['pos'])).lower()
            if not usertext and not userteam and not userposition:
                return JsonResponse({"Please provide at least one filter"})

            if namematch and teammatch and positionmatch:
                playersInfo.append({
                    'espnName':player.get('espnName', "N/A"),
                    'jerseyNum':player.get('jerseyNum', "N/A"),
                    'team':player.get('team', "N/A"),
                    'age':player.get('age', "N/A"),
                    'espnHeadshot':player.get('espnHeadshot', "N/A"),
                    'pos':player.get('pos', "N/A"),
                    'playerID':player.get('playerID', "N/A"),
                })

        if usersort:
            if usersort == 'team':
                playersInfo.sort(key=lambda x: x.get('team', '').lower())
            elif usersort == 'name':
                playersInfo.sort(key=lambda x: x.get('espnName', '').lower())
            elif usersort == 'age':
                playersInfo.sort(key=lambda x: x.get('age', 0))
       
        return JsonResponse({"players":playersInfo})
    return JsonResponse({'error':'Post method missing'}, status=405)

@login_required
def stat(request):
    return render(request, "stat.html")

#############################################################################################
##########################        ARTICLES         ##########################################
#############################################################################################
@login_required
def articles(request):
    allarts = Articles.objects.all()
    return render(request, "articles.html", {'allarts':allarts})

@login_required
def article(request, articleID):
    article = Articles.objects.get(id=articleID)
    if article.author == request.user.username:
        artpermission = "yes"
    else:
        artpermission = "no"
    author = article.author
    userauthor = request.user.username
    return render(request, "article.html", {'article': article, 'userauthor':userauthor,'author':author,'artpermission':artpermission})

@login_required
def arthelper(request):
    if request.method == "POST":
        redirect('makeart')
    return redirect('makeart')

@login_required
def makeart(request):
    if request.method == "POST":
        title = request.POST.get("arttitle")
        content = request.POST.get("artcontent")
        if title and content:
            # Save the article
            article = Articles.objects.create(
                userid=request.user,
                author=request.user.username,
                arttitle=title,
                content=content
            )
            article.save()
            return redirect('articles')
    return render(request, "makeart.html")

@login_required
def deleteart(request):
    if request.method == "POST":
        articleID = request.POST.get("deleteart")    
        article = Articles.objects.get(id=articleID)
        article.delete()
        return redirect("articles")

#https://www.geeksforgeeks.org/working-with-datetime-objects-and-timezones-in-python/
#############################################################################################
##########################        GAME ROOM        ##########################################
#############################################################################################
@login_required
def games(request):
    return render(request, "games.html")

@login_required
def gameperweek(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            week = data.get('week')
            url = "https://tank01-nfl-live-in-game-real-time-statistics-nfl.p.rapidapi.com/getNFLGamesForWeek"
            querystring = {"week":week,"seasonType":"reg","season":"2024"}
            headers = {
        	        ,
            }
            response = requests.get(url, headers=headers, params=querystring)
            respo = response.json()
            allgames = []
            for game in respo['body']:
                gamedata = {
                    'gameID': game['gameID'],
                    'away': game['away'],
                    'home': game['home'],
                    'teamIDHome': game['teamIDHome'],
                    'teamIDAway': game['teamIDAway'],
                    'gameTime': game['gameTime'],
                    'gameStatusCode' : game['gameStatusCode'],
                }
                allgames.append(gamedata)
            return JsonResponse({'allgames':allgames})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid method, only POST allowed'}, status=405)

@login_required
def playbyplay(request):
   #https://rapidapi.com/tank01/api/tank01-nfl-live-in-game-real-time-statistics-nfl  
    if request.method == "POST":
       data = json.loads(request.body.decode('utf-8'))
       gameID = data.get('gameID')

       cachename = f"pbp{gameID}"
       cacherespo = cache.get(cachename)
       if cacherespo:
           return JsonResponse(cacherespo)

       url = "https://tank01-nfl-live-in-game-real-time-statistics-nfl.p.rapidapi.com/getNFLBoxScore"
       querystring = {"gameID":gameID,"playByPlay":"true"}
       headers = {
	        ,
       }
       response = requests.get(url, headers=headers, params=querystring)
       body = response.json()
       respo = body['body']
       smallerdata = {
           "allPlayByPlay":respo.get('allPlayByPlay', 'N/A'),
           "currentPeriod":respo.get('currentPeriod', 'N/A'),
           "gameClock":respo.get('gameClock', 'N/A'),
           "homePts":respo.get('homePts', 'N/A'),
           "awayPts":respo.get('awayPts', 'N/A'),
       }
       cache.set(cachename, respo, timeout=30)
       return JsonResponse(smallerdata)
