import requests


# Recevoir le Puuid grace aux Pseudo pour faire les autres requetes
def getpuuid(summonername, key):
    urlsummonername = 'https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/'
    urlfinal = urlsummonername + summonername + "?api_key=" + key
    response = requests.get(urlfinal)
    response_json = response.json()
    if response_json == ({'status': {'message': 'Data not found - summoner not found', 'status_code': 404}}) :
        return 0
    else:
        return response_json['puuid']

# Recuperer l'Id de chaque partie
def getgameid(puuid, key, nbrstr, numberofgames):
    urlHistoriqueID ='https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/'
    HistoriqueID = urlHistoriqueID + puuid + '/ids?start=0&count=' + nbrstr + '&api_key=' + key
    response2 = requests.get(HistoriqueID)
    response_json2 = response2.json()
    IdGame = response_json2[numberofgames]
    return IdGame

#Utiliser les games Ids pour acceder a tous les parametres des parties
def getGameInfo (GameIdList, Key) :
    urlGame = 'https://europe.api.riotgames.com/lol/match/v5/matches/'
    GameInfo = []
    for i in GameIdList:
        Game = urlGame + i + "?api_key=" + Key
        response3 = requests.get(Game)
        response_json3 = response3.json()
        GameInfo.append(response_json3)
    return GameInfo

#retrouver le joueur voulu en parcourant les donnees d'une partie en la comparant aux puuid
def get_person_by_id(people_list, target_id):
    for person in people_list:
        if person['puuid'] == target_id:
            return person
    return None

#récuperer le nombre de fois qu'un personnage a été sélectionné pour une partie
def getnbrofgamesonchamps(championplayed):
    Champion = {}
    for champ in championplayed:
        if champ in Champion:
            Champion[champ] += 1
        else:
            Champion[champ] = 1
    return Champion

def getLP(Summoner, nbrgame) :
    UrlCalibreum = ('https://calibrum.4esport.fr/api/player/' + Summoner)
    response4 = requests.get(UrlCalibreum)
    response_json4 = response4.json()
    lpgains = []
    if response4 == 'ERROR':
        return 0
    else:
        for i in range(0, nbrgame):
            lpgains.append(response_json4['accounts'][0]['lpUpdates'][i]["LP"])
        return lpgains