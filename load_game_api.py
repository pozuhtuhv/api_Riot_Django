import os
import time
from collections import defaultdict
import requests
import json
from django.shortcuts import render
from dotenv import load_dotenv

load_dotenv()

token = os.getenv('KEY')

username = 'pozuhtuhv'
tag = '0731'

with requests.Session() as session:
    header = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0",
                "Accept-Language": "ko,en;q=0.9",
                "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
                "Origin": "https://developer.riotgames.com",
                "X-Riot-Token": f"{token}"
            }
    
    # puuid load
    puuid = session.get(f'https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{username}/{tag}', headers=header)
    if puuid.status_code == 200:
        load_puuid = json.loads(puuid.text)
        print(load_puuid)
        load_puuid = load_puuid.get('puuid')
        print(load_puuid)
    time.sleep(0.3)
    # matche_id load
    matche_id = session.get(f'https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/{load_puuid}/ids?start=0&count=1', headers=header)
    if matche_id.status_code == 200:
        info_matches = json.loads(matche_id.text)
        print(info_matches[0])
        # find_matches_info
        load_matches = session.get(f'https://asia.api.riotgames.com/lol/match/v5/matches/{info_matches[0]}', headers=header)
        # if load_matches.status_code == 200:
        load_matches_info = json.loads(load_matches.text)
        # 게임 시간
        gamestart = load_matches_info['info']['gameCreation']
        gameend = load_matches_info['info']['gameEndTimestamp']
        # 밀리초 단위의 차이 계산
        time_difference_ms = gameend - gamestart
        # 밀리초를 초로 변환
        time_difference_s = time_difference_ms / 1000
        # 초를 분과 초로 변환
        minutes = int(time_difference_s // 60)
        seconds = int(time_difference_s % 60)
        print(f"{minutes}분 {seconds}초")

        # 참가자 정보를 추출
        champion_names = [participant['championName'] for participant in load_matches_info['info']['participants']]
        username = [participant['riotIdGameName'] for participant in load_matches_info['info']['participants']]
        tagline = [participant['riotIdTagline'] for participant in load_matches_info['info']['participants']]
        team = [participant['placement'] for participant in load_matches_info['info']['participants']]
        kda = [str(participant['challenges']['kda'])[:4] for participant in load_matches_info['info']['participants']]
        kills = [participant['kills'] for participant in load_matches_info['info']['participants']]
        assists = [participant['assists'] for participant in load_matches_info['info']['participants']]
        deaths = [participant['deaths'] for participant in load_matches_info['info']['participants']]
        

        # 팀별로 참가자 정보를 그룹화
        team_participants = defaultdict(list)
        for idx in range(len(champion_names)):
            team_participants[team[idx]].append({
                'champion_name': champion_names[idx],
                'username': username[idx],
                'tagline': tagline[idx],
                'kda': kda[idx],
                'k/d/a': f"{kills[idx]}/{deaths[idx]}/{assists[idx]}"
            })

        # 각 팀별 참가자 정보를 출력
        for team_placement in sorted(team_participants):
            print(f"Team {team_placement}:")
            for idx, participant in enumerate(team_participants[team_placement]):
                print(f"  User {idx + 1}:")
                print(f"    Champion Name: {participant['champion_name']}")
                print(f"    Username: {participant['username']}")
                print(f"    Tagline: {participant['tagline']}")
                print(f"    KDA: {participant['kda']}")
                print(f"    K/D/A: {participant['k/d/a']}")
            print()  # 각 팀별 출력 후 한 줄 띄우기