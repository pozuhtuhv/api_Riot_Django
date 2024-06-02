import os
import time

import requests
import json
from django.shortcuts import render
from dotenv import load_dotenv

load_dotenv()

token = os.getenv('KEY1')

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
        start_index = 1
        end_index = 8
        champion_names = []
        for i in range(start_index, end_index + 1):
            champion_names.append(load_matches_info['info']['participants'][i]['championName'])
        for idx, champion_name in enumerate(champion_names, start=start_index):
            print(f"User {idx}: {champion_name}")