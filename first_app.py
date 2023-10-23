import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import altair as alt
from Functions import getpuuid, getgameid, getGameInfo,get_person_by_id, getnbrofgamesonchamps, getLP

# Clef API
Key = "RGAPI-fa8ebc95-d799-471e-b41a-5206b7ea3355"
st.title("What are my League Stats?")
# Recevoir le Summoner Name et le nombre de partie voulu
# SummonerName = input('Please enter summoner name:')
SummonerName = st.text_input('SummonerName')
SummonerName = ("Manguier")
st.write('Current Summoner Name is :', SummonerName)
numberofgames = 10
numberofgames = st.number_input('number of games', min_value=1, max_value=10, value=5, step=1)
st.write('number of games :', numberofgames)

# Variables
defeat = 0
victory = 0
KDA = []
goldEarned = []
totalMinionsKilled = []
totalDamageDealtToChampions = []
visionScore = []
ChampionPlayed = []
averageGoldEarned = 0
averagetotalMinionsKilled = 0
averagetotalDamageDealtToChampions = 0
averagevisionScore = 0
AverageKDA = 0
championrows = []
championgamescolumn = []

# Le main
puuid = getpuuid(SummonerName, Key)

if puuid == 0:
    print("The summoner does not exist.")
else:
    GameIdList = []
    for i in range(0, numberofgames):
        nbrstr = str(numberofgames)
        GameID = getgameid(puuid, Key, nbrstr, i)
        GameIdList.append(GameID)
    First20GamesInfo = getGameInfo(GameIdList, Key)
    x = getLP(SummonerName, numberofgames)

    # recevoir toutes les infos
    for i in range(0, numberofgames):
        target = get_person_by_id(First20GamesInfo[i]['info']['participants'], puuid)
        KDA.append((target['assists'] + target['kills'])/(target['deaths']+1))
        goldEarned.append(target['goldEarned'])
        totalMinionsKilled.append(target['totalMinionsKilled'])
        totalDamageDealtToChampions.append(target['totalDamageDealtToChampions'])
        visionScore.append(target['visionScore'])
        ChampionPlayed.append(target['championName'])
        win = target['win']
        if win is True:
            victory += 1
        else:
            defeat += 1

    for i in range(0,numberofgames):
        averageGoldEarned += goldEarned[i]//numberofgames
        averagetotalMinionsKilled += totalMinionsKilled[i]//numberofgames
        averagetotalDamageDealtToChampions += totalDamageDealtToChampions[i]//numberofgames
        averagevisionScore += visionScore[i]//numberofgames
        AverageKDA += KDA[i]//numberofgames
    # Bar plot
    result = getnbrofgamesonchamps(ChampionPlayed)

    championgamescolumn = list(result.keys())
    championrows = list(result.values())

    fig = px.bar(x=championgamescolumn, y=championrows, labels={'x': 'Champion', 'y': 'Number of Games Played'})
    fig.update_layout(
        xaxis_tickangle=-45  # Rotates the x-axis labels for better readability
    )


    # Pie chart

    labels = "Wins", "Losses"
    size = [victory, defeat]

    piechart = px.pie(names=labels, values=size)

    # On page


    # spider chart
    score = [
        (averageGoldEarned / 10000),
        (averagetotalMinionsKilled / 50),
        (averagetotalDamageDealtToChampions / 20000),
        (averagevisionScore / 50),
        (AverageKDA / 2)
    ]

    variables = ['Gold Earned', 'Minions Killed', 'Damage Dealt', 'Vision Score', 'KDA']

    # Create a radar chart
    spider = go.Figure()

    spider.add_trace(go.Scatterpolar(
        r=score + score[:1],
        theta=variables + [variables[0]],
        fill='toself',
        name='Player Score'
    ))

    st.title('LP GAINS')

    # Assuming you have a function `getLP` that returns LpList
    LpList = getLP(SummonerName, numberofgames)

    x_values = list(range(numberofgames))
    y_values = [LpList[i] for i in range(numberofgames)]

    # Create a Pandas DataFrame with X and Y columns
    data = pd.DataFrame({'X': x_values, 'Y': y_values})
    # Create an Altair line chart
    chart = alt.Chart(data).mark_line().encode(
        x='X',
        y='Y'
    ).properties(
        title='LP Gains'
    )

    # Show the chart
    with st.container():
        st.altair_chart(chart, use_container_width=True)
    with st.container():
        st.title('Number of Games on Champions')
        st.plotly_chart(fig)
        st.title('Win Lose ratio')
        st.plotly_chart(piechart)
        st.title('Player Average Score')
        st.plotly_chart(spider)
