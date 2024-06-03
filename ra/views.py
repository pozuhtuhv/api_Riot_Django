# ra/views.py

import os
import time
from collections import defaultdict
import requests
import json
from django.shortcuts import render, redirect
from dotenv import load_dotenv

load_dotenv()

def home(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        tag = request.POST.get('tag')
        return redirect('get_match_info', username=username, tag=tag)
    return render(request, 'home.html')

def get_match_info(request, username, tag):
    token = os.getenv('KEY')
    if not token:
        return render(request, 'error.html', {'message': 'API key not found'})

    with requests.Session() as session:
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0",
            "Accept-Language": "ko,en;q=0.9",
            "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "https://developer.riotgames.com",
            "X-Riot-Token": f"{token}"
        }
        
        # puuid load
        try:
            puuid_response = session.get(f'https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{username}/{tag}', headers=header)
            puuid_response.raise_for_status()  # Raise an HTTPError for bad responses
            puuid_data = puuid_response.json()
            puuid = puuid_data.get('puuid')
            print(f"PUUID: {puuid}")  # 디버깅 출력
        except requests.RequestException as e:
            return render(request, 'error.html', {'message': f'Failed to load PUUID: {e}'})
        
        time.sleep(0.3)
        
        # match_id load
        try:
            match_id_response = session.get(f'https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count=1', headers=header)
            match_id_response.raise_for_status()
            match_ids = match_id_response.json()
            if not match_ids:
                return render(request, 'error.html', {'message': 'No matches found'})
            match_id = match_ids[0]
        except requests.RequestException as e:
            return render(request, 'error.html', {'message': f'Failed to load match IDs: {e}'})
        
        # find_matches_info
        try:
            match_info_response = session.get(f'https://asia.api.riotgames.com/lol/match/v5/matches/{match_id}', headers=header)
            match_info_response.raise_for_status()
            match_info = match_info_response.json()
            
            # 게임 시간
            gamestart = match_info['info']['gameCreation']
            gameend = match_info['info']['gameEndTimestamp']
            time_difference_ms = gameend - gamestart
            time_difference_s = time_difference_ms / 1000
            minutes = int(time_difference_s // 60)
            seconds = int(time_difference_s % 60)
            game_duration = f"{minutes}분 {seconds}초"
            
            # 참가자 정보 추출
            participants = match_info['info']['participants']
            team_participants = defaultdict(list)
            for participant in participants:
                team_participants[participant['placement']].append({
                    'champion_name': participant['championName'],
                    'username': participant['riotIdGameName'],
                    'tagline': participant['riotIdTagline'],
                    'kda': f"{participant['kills']}/{participant['deaths']}/{participant['assists']}",
                    'kda_value': f"{str(participant['challenges']['kda'])[:4]}"
                })
            
            # 팀을 순서대로 정렬
            sorted_team_participants = sorted(team_participants.items())

            context = {
                'game_duration': game_duration,
                'team_participants': sorted_team_participants  # 정렬된 팀 참가자 정보 전달
            }
            
            return render(request, 'match_info.html', context)
        except requests.RequestException as e:
            return render(request, 'error.html', {'message': f'Failed to load match info: {e}'})

def custom_404(request, exception):
    return render(request, '404.html', status=404)
