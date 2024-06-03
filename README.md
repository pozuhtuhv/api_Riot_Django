### framework_Django_Riot (~ing)

### Process

#### Django_Riot_전적_process
- https://americas.api.riotgames.com/ - load_puuid
- /riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine} - 계정 PUUID
- https://asia.api.riotgames.com/ - load_asia_matches
- /lol/match/v5/matches/by-puuid/{puuid}/ids - PUUID 를 이용한 매치 정보
- /lol/match/v5/matches/{matchId} - matchId 검색
- 리스트 노출

#### Guide
1. .env -> Your Riot Key
2. python manage.py runserver
3. http://127.0.0.1:8000/ra/
4. Username and Tagline / search

![docs](https://raw.githubusercontent.com/pozuhtuhv/0000_imgstorage/main/framework_Django_Riot_1.png)

![docs](https://raw.githubusercontent.com/pozuhtuhv/0000_imgstorage/main/framework_Django_Riot_2.png)

### docs
https://developer.riotgames.com/
