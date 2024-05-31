import os
import time

import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
from dotenv import load_dotenv

load_dotenv()

token = os.getenv('KEY')

def index(request):
    return render(request, 'board/index.html')

def load(request):
    if request.method == 'POST':
        username = request.POST['username']
        tag = request.POST['tag']
        header = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0",
                    "Accept-Language": "ko,en;q=0.9",
                    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
                    "Origin": "https://developer.riotgames.com",
                    "X-Riot-Token": f"{token}"
                }
        puuid = requests.post(f'https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{username}/{tag}', headers=header)
        if puuid.status_code == 200:
            time.sleep(0.3)
            match_id = request.post(f'https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count=1', headers=header)
            if match_id.status_code == 200:
                soup = BeautifulSoup(match_id.text, 'html.parser')
                