# ra/views.py

import os
import time
from collections import defaultdict
import requests
from django.shortcuts import render, redirect
from dotenv import load_dotenv
import pandas as pd

# 챔피언 이름 한글화
df = pd.read_csv('./KORLIST.csv', encoding='euc-kr')
name_dict = pd.Series(df.B.values, index=df.A).to_dict()

load_dotenv()

def redirect_to_app(request):
    return redirect('/ra/')

def index(request):
    token = os.getenv('KEY')
    if not token:
        raise ValueError('API key not found')

    if request.method == 'POST':
        username = request.POST.get('username')
        tag = request.POST.get('tag')
        return redirect('get_match_info', username=username, tag=tag)
    
    context = {
        'token': token
    }
    return render(request, 'index.html', context)

# API header connect
def get_header():
    token = os.getenv('KEY')
    if not token:
        raise ValueError('API key not found')

    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0",
        "Accept-Language": "ko,en;q=0.9",
        "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://developer.riotgames.com",
        "X-Riot-Token": f"{token}"
    }
    return header

# get user puuid
def get_puuid(username, tag, headers):
    url = f'https://asia.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{username}/{tag}'
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    # puuid 확인
    # print(response.json())
    return response.json().get('puuid')

# get match id
def get_match_id(puuid, headers):
    url = f'https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count=1'
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    match_ids = response.json()
    if not match_ids:
        raise ValueError('No matches found')
    return match_ids[0]

# get match info by id
def get_match_info_by_id(match_id, headers):
    url = f'https://asia.api.riotgames.com/lol/match/v5/matches/{match_id}'
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

# game time calculate
def calculate_game_duration(match_info):
    gamestart = match_info['info']['gameCreation']
    gameend = match_info['info']['gameEndTimestamp']
    time_difference_ms = gameend - gamestart
    time_difference_s = time_difference_ms / 1000
    minutes = int(time_difference_s // 60)
    seconds = int(time_difference_s % 60)
    return f"{minutes}분 {seconds}초"

# get game info
def get_team_participants(match_info):
    participants = match_info['info']['participants']
    team_participants = defaultdict(list)
    for participant in participants:
        korean_name = get_korean_name(participant['championName'])
        team_participants[participant['placement']].append({
            'champion_name': korean_name,
            'username': participant['riotIdGameName'],
            'tagline': participant['riotIdTagline'],
            'kda': f"{participant['kills']}/{participant['deaths']}/{participant['assists']}",
            'kda_value': f"{str(participant['challenges']['kda'])[:4]}"
        })
    return sorted(team_participants.items())

# korean translate
def get_korean_name(english_name):
    return name_dict.get(english_name, "이름을 찾을 수 없습니다.")

# get match info
def get_match_info(request, username, tag):
    try:
        headers = get_header()
        puuid = get_puuid(username, tag, headers)
        match_id = get_match_id(puuid, headers)
        match_info = get_match_info_by_id(match_id, headers)
    except ValueError as e:
        return render(request, 'error.html', {'message': str(e)})
    except requests.RequestException as e:
        return render(request, 'error.html', {'message': f'Failed to load data: {e}'})
    except Exception as e:  # Catch any other unexpected exceptions
        return render(request, 'error.html', {'message': f'An unexpected error occurred: {e}'})
    
    time.sleep(0.3)
    
    game_duration = calculate_game_duration(match_info)
    team_participants = get_team_participants(match_info)

    context = {
        'match_id': match_id, 
        'game_duration': game_duration,
        'team_participants': team_participants
    }
    
    return render(request, 'match_info.html', context)

def custom_404(request, exception):
    return render(request, '404.html', status=404)
