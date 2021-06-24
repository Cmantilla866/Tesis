from fastapi import FastAPI, Query
import pandas as pd
import os
import h2o
import matplotlib.pyplot as plt
from fastapi.responses import FileResponse
from typing import Optional
import requests
import json


app = FastAPI()


@app.on_event("startup")
def startup_event():
    h2o.init(url="http://localhost:54321")


@app.get("/")
async def index(url: str = Query(..., description="Link de la partida que se quiere analizar del tipo "
                                                 "https://matchhistory.lan.leagueoflegends.com/"),
                minute: Optional[int] = Query(0, description="Minuto entero de la partida que se desea ver en el mapa",
                                              title="Minuto de partida")):
    """
    <h3>Con base en la información de una partida, predice minuto a minuto si cada jugador en la partido puso un ward.</h3>
    * Si se especifica un minuto en especifico se mostrará una gráfica con la posición de todos los jugadores y si
    pusieron un ward o no.
    * Si no se especifica se devolverá un Json con todas las estadisticas de la partida junto a las predicciones
    minuto a minuto.
    </br>
    </br>
    <h2>Interpretación de la Imágen:</h2>
    <h3>Los puntos que se observan en el mapa son las ubicaciones de los jugadores</h3>
    * Si el punto es de color azul significa que el jugador de equipo azul puso un ward según la información de la partida
    * Si el punto es de color rojo significa que el jugador de equipo rojo puso un ward según la información de la partida
    * Si el punto es de color verde significa que el jugador de equipo azul puso un ward según la predicción del modelo
    * Si el punto es de color amarillo significa que el jugador de equipo rojo puso un ward según la predicción del modelo
    """
    KappaL = url.split("/")
    gameCode = KappaL[6].split("?")[0]

    if os.path.exists('Predicted_' + gameCode + '.json'):
        frame = pd.read_json('Predicted_' + gameCode + '.json')
        if minute == 0:
            return frame.to_dict()
        else:
            img = plt.imread("mapa.PNG")
            lanes = ["TOP", "JG", "MID", "ADC", "SUPP"]

            xB, yB, playerB, xR, yR, playerR = [], [], [], [], [], []
            xB_predicted, yB_predicted, playerB_predicted, xR_predicted, yR_predicted, playerR_predicted = \
                [], [], [], [], [], []

            for lane in lanes:
                if frame.iloc[minute]["wardsPlaced - " + lane + "B"] == 1:
                    xB.append(frame.iloc[minute]["positionX - " + lane + "B"])
                    yB.append(frame.iloc[minute]["positionY - " + lane + "B"])
                    playerB.append(lane)
                if frame.iloc[minute]["wardsPlaced - " + lane + "R"] == 1:
                    xR.append(frame.iloc[minute]["positionX - " + lane + "R"])
                    yR.append(frame.iloc[minute]["positionY - " + lane + "R"])
                    playerR.append(lane)
                if frame.iloc[minute]["wardsPlaced - " + lane + "B_predicted"] == 1:
                    xB_predicted.append(frame.iloc[minute]["positionX - " + lane + "B"])
                    yB_predicted.append(frame.iloc[minute]["positionY - " + lane + "B"])
                    playerB_predicted.append(lane)
                if frame.iloc[minute]["wardsPlaced - " + lane + "R_predicted"] == 1:
                    xR_predicted.append(frame.iloc[minute]["positionX - " + lane + "R"])
                    yR_predicted.append(frame.iloc[minute]["positionY - " + lane + "R"])
                    playerR_predicted.append(lane)

            fig, ax = plt.subplots(figsize=(15, 15))
            ax.scatter(xB, yB, s=4000, c="b", alpha=0.4)
            ax.scatter(xR, yR, s=4000, c="r", alpha=0.4)
            ax.scatter(xB_predicted, yB_predicted, s=2000, c="g", alpha=0.4)
            ax.scatter(xR_predicted, yR_predicted, s=2000, c="y", alpha=0.4)

            for i, txt in enumerate(playerB):
                ax.text(xB[i], yB[i], s=txt, size="x-large", weight="bold", ha="center", va="center", style="oblique")
            for i, txt in enumerate(playerR):
                ax.text(xR[i], yR[i], s=txt, size="x-large", weight="bold", ha="center", va="center", style="oblique")
            for i, txt in enumerate(playerB_predicted):
                ax.text(xB_predicted[i], yB_predicted[i], s=txt, size="x-large", weight="bold", ha="center",
                        va="center",
                        style="oblique")
            for i, txt in enumerate(playerR_predicted):
                ax.text(xR_predicted[i], yR_predicted[i], s=txt, size="x-large", weight="bold", ha="center",
                        va="center",
                        style="oblique")

            ax.imshow(img, extent=[0, 15000, 0, 15000])
            fig.savefig('full_figure.png')

            return FileResponse("full_figure.png")
    else:
        data = []
        sightItems = [3860, 3859, 3855, 3857, 3098, 3853, 3340, 3363, 2055, 3364]
        sightItemsNames = {"3860": "BulwarkOfTheMountain", "3859": "TargonsBuckler", "3855": "RunesteelSpaulders",
                           "3857": "PauldronsOfWhiterock", "3098": "Frostfang", "3853": "ShardOfTrueIce",
                           "3340": "WardingTotem", "3363": "FarsightAlteration", "2055": "ControlWard",
                           "3364": "OracleLens"}
        springStats = pd.read_csv("Spring.csv")
        summerStats = pd.read_csv("Summer.csv")
        champions = pd.read_json('champion-summary.json')
        championStats = pd.read_csv("championStats (1).csv")

        KappaL = url.split("/")
        gameCode = KappaL[6].split("?")[0]

        cookies = "ajs_group_id=null; ajs_user_id=null; osano_consentmanager_uuid=586d90e4-135d-469f-af88-b51ca0392758; " \
                  "osano_consentmanager_expdate=1641910356172; _gcl_au=1.1.20772009.1609774663; " \
                  "_gid=GA1.2.523524002.1609774663; _hjTLDTest=1; _hjid=4aa280a0-12ac-4291-9e2b-fe249a47f84e; " \
                  "_hjFirstSeen=1; ping_session_id=106ffd64-05c5-4765-aeaf-b4706d7c6eb4; _hjAbsoluteSessionInProgress=0; " \
                  "_tli=6864292941341953194; " \
                  "PVPNET_TOKEN_LAN" \
                  "=eyJkYXRlX3RpbWUiOjE2MDk3NzQ2ODE2MDcsImdhc19hY2NvdW50X2lkIjoyMDA5NjI0MTUsInB2cG5ldF9hY2NvdW50X2lkIjoyMDA5NjI0MTUsInN1bW1vbmVyX25hbWUiOiJjcmlzbWFudGkyMCIsInZvdWNoaW5nX2tleV9pZCI6IjkwMzQ3NTJiMmI0NTYwNDRhZTg3ZjI1OTgyZGFkMDdkIiwic2lnbmF0dXJlIjoiZFZMejVSR2p4RFRLMWpydEZaU2U5VU92U0gxaDIxbWR0alRLZ29aT2JZQkkzVFRkZFdDMEhGZWZjREhORlRuWDZJOFA3SVpJNlprVkFGM0M5VzB6ckFoZDFXc3FNeXo5TklMbWQ0ZXJsNHREdXlTdTFUR0xEVlRLT1RYek5YN28rR0F5a1ZEa014TkpjNEhiSVQvUUU3MzYwTmlmN1VYcUxuZ0wyN21ueEFRPSJ9; PVPNET_ACCT_LAN=crismanti20; PVPNET_ID_LAN=200962415; PVPNET_REGION=lan; PVPNET_LANG=es_ES; id_token=eyJraWQiOiJzMSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiIyYWNmYWM4Ni03ZDg2LTU2OTgtOGU1MS00NWJiNWI4NjA3Y2UiLCJjb3VudHJ5IjoiY29sIiwicGxheWVyX3Bsb2NhbGUiOiJlbi1VUyIsImFtciI6WyJwYXNzd29yZCJdLCJpc3MiOiJodHRwczpcL1wvYXV0aC5yaW90Z2FtZXMuY29tIiwibG9sIjpbeyJjdWlkIjoyMDA5NjI0MTUsImNwaWQiOiJMQTEiLCJ1aWQiOjIwMDk2MjQxNSwidW5hbWUiOiJDbWFudGkiLCJwdHJpZCI6bnVsbCwicGlkIjoiTEExIiwic3RhdGUiOiJFTkFCTEVEIn1dLCJsb2NhbGUiOiJlc19FUyIsImF1ZCI6InJzby13ZWItY2xpZW50LXByb2QiLCJhY3IiOiJ1cm46cmlvdDpicm9uemUiLCJwbGF5ZXJfbG9jYWxlIjoiZW4tVVMiLCJleHAiOjE2MDk4NjEwODAsImlhdCI6MTYwOTc3NDY4MCwiYWNjdCI6eyJnYW1lX25hbWUiOiJjcmlzbWFudGkyMCIsInRhZ19saW5lIjoiTEFOIn0sImp0aSI6IkFRdEpDYUlvWU9BIiwibG9naW5fY291bnRyeSI6ImNvbCJ9.GJHIfn_GlVL7IJ10NtkANiaXLplUzaZg5LlPVma5nv9o5Qik6ZqLiRAzQL-a1fpGDdPFso340ERLlwscgJDh1bp9apTFL9-8_ezVvL1Nj6O92OAILVQG-kVOu5XnEjFany0aEUMKfa1I6gyviuhqSzwjnCwONZwtaMCDj7D5ztk; id_hint=sub%3D2acfac86-7d86-5698-8e51-45bb5b8607ce%26lang%3Des%26game_name%3Dcrismanti20%26tag_line%3DLAN%26id%3D200962415%26summoner%3Dcrismanti20%26region%3DLA1%26tag%3Dlan; __cfduid=d135ba66f522c2a1b88562170a9670baf1609774683; osano_consentmanager=oe4vGLfdiMusKqf4aCfbA3h2dBNuChJoqlgX4K71YZvG_Z3PfHbgVDP5c_ewkjB_nk1YDDsm6gieusi0ppc0n4tQsII6VD6sBXoZWYOq-_Ctg7IXK-79TJw72S-ZfaE8C-PEJU2JpDLfecgmOdiJLLHjA8fGb1cX6DGSeeGIWroxZrpesuUcI-v0mKkHDKxYigrfQQIl5InEbuZFqJ-m3SKjhaMDeTpUkqaea1ntexSWorOePFW6w9L2YnSIv2fsgny6YFAuKhJilh3XakncN00RWKGt27e8a9glkWAkY_U0h1Aj7pDlTJ732GJlFw4AdtyCxg==; _ga_FXBJE5DEDD=GS1.1.1609774662.1.1.1609774684.38; _tlc=login.lolesports.com%2F:1609774684:na.leagueoflegends.com%2Fes-mx%2F:leagueoflegends.com; _tlv=1.1609774664.1609774664.1609774684.2.1.2; _ga=GA1.2.985745498.1608732737; _tlp=2820:16705876; _tls=*.1069393:1069394..6864292941341953194 "

        base_match_history_stats_url = "https://acs.leagueoflegends.com/v1/stats/game/{}/{}?gameHash={}"
        base_match_history_stats_timeline_url = "https://acs.leagueoflegends.com/v1/stats/game/{}/{}/timeline?gameHash={}"

        url = base_match_history_stats_url.format(KappaL[5], KappaL[6].split("?")[0],
                                                  KappaL[6].split("?")[1].split("&")[0].split("=")[1])
        timeline_url = base_match_history_stats_timeline_url.format(KappaL[5], KappaL[6].split("?")[0],
                                                                    KappaL[6].split("?")[1].split("&")[0].split("=")[1])

        game_data = requests.get(url, cookies={c.split("=")[0]: c.split("=")[1] for c in cookies.split(";")}).json()
        timeline_data = requests.get(timeline_url,
                                     cookies={c.split("=")[0]: c.split("=")[1] for c in cookies.split(";")}).json()

        with open(gameCode + '.json', 'w') as outfile:
            json.dump(game_data, outfile)

        with open(gameCode + '_timeline.json', 'w') as outfile:
            json.dump(timeline_data, outfile)

        with open(gameCode + '_timeline.json') as json_file:
            timeline = json.load(json_file)
            # print(timeline.keys())
            participantFrames = []
            events = []
            frames = timeline['frames']
            events = []
            for frame in range(len(frames)):
                participantFrames.append(frames[frame]["participantFrames"])
                for event in range(len(frames[frame]['events'])):
                    """if frames[frame]['events'][event]['type'] == 'WARD_PLACED':
                        frames[frame]['events'][event]['participantId'] = frames[frame]['events'][event]['creatorId']
                        del frames[frame]['events'][event]['creatorId']
                        events.append(frames[frame]['events'][event])

                    if frames[frame]['events'][event]['type'] == 'WARD_KILL':
                        frames[frame]['events'][event]['participantId'] = frames[frame]['events'][event]['killerId']
                        del frames[frame]['events'][event]['killerId']
                        events.append(frames[frame]['events'][event])"""
                    events.append(frames[frame]['events'][event])
            """types = []
            for ev in events:
                if not types.__contains__(ev["type"]):
                    types.append(ev["type"])
            print(types)"""
            with open(gameCode + '.json') as json_game:
                game = json.load(json_game)
                participants = game["participants"]
                dragonSpawn = 5
                dragonRate = 5
                riftSpawn = 8
                riftRate = 6
                baronSpawn = 20
                baronRate = 7
                for participantFrame in range(len(participantFrames)):
                    frame = {}
                    Dragon = 0
                    Rift = 0
                    Baron = 0
                    for participant in participantFrames[participantFrame]:
                        del participantFrames[participantFrame][participant]["currentGold"]
                        del participantFrames[participantFrame][participant]["minionsKilled"]
                        del participantFrames[participantFrame][participant]["jungleMinionsKilled"]
                        del participantFrames[participantFrame][participant]["dominionScore"]
                        del participantFrames[participantFrame][participant]["teamScore"]

                        participantFrames[participantFrame][participant]["positionX"] = \
                            participantFrames[participantFrame][participant]["position"]["x"]
                        participantFrames[participantFrame][participant]["positionY"] = \
                            participantFrames[participantFrame][participant]["position"]["y"]
                        del participantFrames[participantFrame][participant]["position"]

                        """position = [participantFrames[participantFrame][participant]["position"]["x"],
                                    participantFrames[participantFrame][participant]["position"]["y"]]
                        participantFrames[participantFrame][participant]["position"] = position"""

                        participantFrames[participantFrame][participant]["dead"] = 0

                        if participantFrame + 1 >= dragonSpawn:
                            Dragon = 1
                        else:
                            Dragon = 0

                        if riftSpawn <= participantFrame + 1 <= 20:
                            Rift = 1
                        else:
                            Rift = 0

                        if participantFrame + 1 >= baronSpawn:
                            Baron = 1
                        else:
                            Baron = 0

                        team = game["participantIdentities"][int(participant) - 1]["player"]["summonerName"].split()[0]

                        try:
                            if game["platformId"] == "ESPORTSTMNT05":
                                participantFrames[participantFrame][participant]["teamDragon%"] = int(springStats[
                                                                                                          springStats[
                                                                                                              "Team"] == team][
                                                                                                          "DRA%"].values[
                                                                                                          0])
                                participantFrames[participantFrame][participant]["teamHerald%"] = int(springStats[
                                                                                                          springStats[
                                                                                                              "Team"] == team][
                                                                                                          "HER%"].values[
                                                                                                          0])
                                participantFrames[participantFrame][participant]["teamNash%"] = int(springStats[
                                                                                                        springStats[
                                                                                                            "Team"] == team][
                                                                                                        "NASH%"].values[
                                                                                                        0])
                            else:
                                participantFrames[participantFrame][participant]["teamDragon%"] = int(summerStats[
                                                                                                          summerStats[
                                                                                                              "Team"] == team][
                                                                                                          "DRA%"].values[
                                                                                                          0])
                                participantFrames[participantFrame][participant]["teamHerald%"] = int(summerStats[
                                                                                                          summerStats[
                                                                                                              "Team"] == team][
                                                                                                          "HER%"].values[
                                                                                                          0])
                                participantFrames[participantFrame][participant]["teamNash%"] = int(summerStats[
                                                                                                        summerStats[
                                                                                                            "Team"] == team][
                                                                                                        "NASH%"].values[
                                                                                                        0])
                        except:
                            participantFrames[participantFrame][participant]["teamDragon%"] = 50
                            participantFrames[participantFrame][participant]["teamHerald%"] = 50
                            participantFrames[participantFrame][participant]["teamNash%"] = 50

                        participantFrames[participantFrame][participant]["championId"] = \
                            participants[int(participant) - 1]["championId"]

                        try:
                            participantFrames[participantFrame][participant]["championCSD"] = int(championStats[
                                                                                                      championStats[
                                                                                                          "Champion"] ==
                                                                                                      champions[
                                                                                                          champions[
                                                                                                              "id"] ==
                                                                                                          participantFrames[
                                                                                                              participantFrame][
                                                                                                              participant][
                                                                                                              "championId"]][
                                                                                                          "name"].values[
                                                                                                          0]][
                                                                                                      "CSD@15"].values[
                                                                                                      0])

                            participantFrames[participantFrame][participant]["championGD"] = int(championStats[
                                                                                                     championStats[
                                                                                                         "Champion"] ==
                                                                                                     champions[
                                                                                                         champions[
                                                                                                             "id"] ==
                                                                                                         participantFrames[
                                                                                                             participantFrame][
                                                                                                             participant][
                                                                                                             "championId"]][
                                                                                                         "name"].values[
                                                                                                         0]][
                                                                                                     "GD@15"].values[0])

                            participantFrames[participantFrame][participant]["championXPD"] = int(championStats[
                                                                                                      championStats[
                                                                                                          "Champion"] ==
                                                                                                      champions[
                                                                                                          champions[
                                                                                                              "id"] ==
                                                                                                          participantFrames[
                                                                                                              participantFrame][
                                                                                                              participant][
                                                                                                              "championId"]][
                                                                                                          "name"].values[
                                                                                                          0]][
                                                                                                      "XPD@15"].values[
                                                                                                      0])
                        except:
                            participantFrames[participantFrame][participant]["championCSD"] = 0

                            participantFrames[participantFrame][participant]["championGD"] = 0

                            participantFrames[participantFrame][participant]["championXPD"] = 0

                        # participantFrames[participantFrame][participant]["teamId"] =
                        # participants[int(participant) - 1]["teamId"]
                        participantFrames[participantFrame][participant]["wardsPlaced"] = 0
                        participantFrames[participantFrame][participant]["wardsKilled"] = 0

                        if int(participant) <= 5:
                            participantFrames[participantFrame][participant]["goldDiff"] = \
                                participantFrames[participantFrame][participant]["totalGold"] - \
                                participantFrames[participantFrame][str(int(participant) + 5)]["totalGold"]
                            participantFrames[participantFrame][participant]["xpDiff"] = \
                                participantFrames[participantFrame][participant]["xp"] - \
                                participantFrames[participantFrame][str(int(participant) + 5)]["xp"]
                        del participantFrames[participantFrame][participant]["totalGold"]
                        del participantFrames[participantFrame][participant]["xp"]

                        items = []
                        for item in range(3):
                            if not participantFrame == 0:
                                if not participantFrames[participantFrame - 1][participant]["item" + str(item)] == 0:
                                    items.append(
                                        participantFrames[participantFrame - 1][participant]["item" + str(item)])

                        for ev in events:
                            if ev['type'] == 'ITEM_PURCHASED' and ev['participantId'] == int(participant) \
                                    and (participantFrame - 1) * 60000 < ev['timestamp'] <= participantFrame * 60000 \
                                    and sightItems.__contains__(ev["itemId"]) and not items.__contains__(ev["itemId"]):
                                items.append(ev["itemId"])
                            if ev['type'] == 'ITEM_DESTROYED' and ev['participantId'] == int(participant) \
                                    and (participantFrame - 1) * 60000 < ev['timestamp'] <= participantFrame * 60000 \
                                    and sightItems.__contains__(ev["itemId"]):
                                if items.__contains__(ev["itemId"]):
                                    items.remove(ev["itemId"])
                            if ev['type'] == 'ITEM_SOLD' and ev['participantId'] == int(participant) \
                                    and (participantFrame - 1) * 60000 < ev['timestamp'] <= participantFrame * 60000 \
                                    and sightItems.__contains__(ev["itemId"]):
                                if items.__contains__(ev["itemId"]):
                                    items.remove(ev["itemId"])
                            if ev['type'] == 'WARD_PLACED' and ev['creatorId'] == int(participant) \
                                    and (participantFrame - 1) * 60000 < ev['timestamp'] <= participantFrame * 60000 \
                                    and not ev['wardType'] == 'UNDEFINED':
                                if participantFrames[participantFrame][participant]["wardsPlaced"] < 1:
                                    participantFrames[participantFrame][participant]["wardsPlaced"] = \
                                        participantFrames[participantFrame][participant]["wardsPlaced"] + 1
                            if ev['type'] == 'WARD_KILL' and ev['killerId'] == int(participant) \
                                    and (participantFrame - 1) * 60000 < ev['timestamp'] <= participantFrame * 60000 \
                                    and not ev['wardType'] == 'UNDEFINED':
                                if participantFrames[participantFrame][participant]["wardsKilled"] < 1:
                                    participantFrames[participantFrame][participant]["wardsKilled"] = \
                                        participantFrames[participantFrame][participant]["wardsKilled"] + 1
                            if ev['type'] == 'CHAMPION_KILL' and ev['victimId'] == int(participant) \
                                    and (participantFrame - 1) * 60000 < ev['timestamp'] <= participantFrame * 60000:
                                participantFrames[participantFrame][participant]["dead"] = 1
                            if ev['type'] == 'ELITE_MONSTER_KILL' and ev['monsterType'] == 'DRAGON' \
                                    and (participantFrame - 1) * 60000 < ev['timestamp'] <= participantFrame * 60000:
                                Dragon = 0
                                dragonSpawn = participantFrame + 1 + dragonRate
                            if ev['type'] == 'ELITE_MONSTER_KILL' and ev['monsterType'] == 'RIFTHERALD' \
                                    and (participantFrame - 1) * 60000 < ev['timestamp'] <= participantFrame * 60000:
                                Rift = 0
                                riftSpawn = participantFrame + 1 + riftRate
                            if ev['type'] == 'ELITE_MONSTER_KILL' and ev['monsterType'] == 'BARON_NASHOR' \
                                    and (participantFrame - 1) * 60000 < ev['timestamp'] <= participantFrame * 60000:
                                Baron = 0
                                baronSpawn = participantFrame + 1 + baronRate
                            """if ev['type'] == 'WARD_KILL' and ev['killerId'] == int(participant) \
                                    and (participantFrame-1) * 60000 < ev['timestamp'] <= participantFrame * 60000:
                                participantFrames[participantFrame][participant]["wardsKilled"] = \
                                    participantFrames[participantFrame][participant]["wardsKilled"] + 1"""

                        participantFrames[participantFrame][participant]["item0"] = 0
                        participantFrames[participantFrame][participant]["item1"] = 0
                        participantFrames[participantFrame][participant]["item2"] = 0
                        participantFrames[participantFrame][participant]["item3"] = 0

                        for item in range(len(items)):
                            participantFrames[participantFrame][participant]["item" + str(item)] = items[item]

                        del participantFrames[participantFrame][participant]["participantId"]
                        for key in participantFrames[participantFrame][participant].keys():
                            frame[key + " - " + participant] = participantFrames[participantFrame][participant][key]
                    frame["minute"] = participantFrame + 1
                    frame["dragon"] = Dragon
                    frame["rift"] = Rift
                    frame["baron"] = Baron
                    # print(frame)
                    data.append(frame)
                    # print(participantFrames[participantFrame])

        with open('DataFrame_' + gameCode + '.json', 'w') as outfile:
            json.dump(data, outfile)

        frame = pd.read_json('DataFrame_' + gameCode + '.json')

        for C in frame.columns:
            newColumn = C
            newColumn = newColumn.replace(" - 10", " - SUPPR") if " - 10" in newColumn else newColumn
            newColumn = newColumn.replace(" - 1", " - TOPB") if " - 1" in newColumn else newColumn
            newColumn = newColumn.replace(" - 2", " - JGB") if " - 2" in newColumn else newColumn
            newColumn = newColumn.replace(" - 3", " - MIDB") if " - 3" in newColumn else newColumn
            newColumn = newColumn.replace(" - 4", " - ADCB") if " - 4" in newColumn else newColumn
            newColumn = newColumn.replace(" - 5", " - SUPPB") if " - 5" in newColumn else newColumn
            newColumn = newColumn.replace(" - 6", " - TOPR") if " - 6" in newColumn else newColumn
            newColumn = newColumn.replace(" - 7", " - JGR") if " - 7" in newColumn else newColumn
            newColumn = newColumn.replace(" - 8", " - MIDR") if " - 8" in newColumn else newColumn
            newColumn = newColumn.replace(" - 9", " - ADCR") if " - 9" in newColumn else newColumn
            frame.rename(columns={C: newColumn}, inplace=True)

        frame.rename(columns={'goldDiff - TOPB': 'goldDiff - TOP'}, inplace=True)
        frame.rename(columns={'goldDiff - JGB': 'goldDiff - JG'}, inplace=True)
        frame.rename(columns={'goldDiff - MIDB': 'goldDiff - MID'}, inplace=True)
        frame.rename(columns={'goldDiff - ADCB': 'goldDiff - ADC'}, inplace=True)
        frame.rename(columns={'goldDiff - SUPPB': 'goldDiff - SUPP'}, inplace=True)

        frame.rename(columns={'xpDiff - TOPB': 'xpDiff - TOP'}, inplace=True)
        frame.rename(columns={'xpDiff - JGB': 'xpDiff - JG'}, inplace=True)
        frame.rename(columns={'xpDiff - MIDB': 'xpDiff - MID'}, inplace=True)
        frame.rename(columns={'xpDiff - ADCB': 'xpDiff - ADC'}, inplace=True)
        frame.rename(columns={'xpDiff - SUPPB': 'xpDiff - SUPP'}, inplace=True)

        frame.rename(columns={'teamDragon% - TOPB': 'teamDragon% - B'}, inplace=True)
        frame.rename(columns={'teamDragon% - SUPPR': 'teamDragon% - R'}, inplace=True)
        frame.rename(columns={'teamHerald% - TOPB': 'teamHerald% - B'}, inplace=True)
        frame.rename(columns={'teamHerald% - SUPPR': 'teamHerald% - R'}, inplace=True)
        frame.rename(columns={'teamNash% - TOPB': 'teamNash% - B'}, inplace=True)
        frame.rename(columns={'teamNash% - SUPPR': 'teamNash% - R'}, inplace=True)

        frame = frame.drop(
            ['teamDragon% - JGB', 'teamDragon% - MIDB', 'teamDragon% - ADCB', 'teamDragon% - SUPPB',
             'teamDragon% - TOPR',
             'teamDragon% - JGR', 'teamDragon% - MIDR', 'teamDragon% - ADCR'], axis=1)
        frame = frame.drop(
            ['teamHerald% - JGB', 'teamHerald% - MIDB', 'teamHerald% - ADCB', 'teamHerald% - SUPPB',
             'teamHerald% - TOPR',
             'teamHerald% - JGR', 'teamHerald% - MIDR', 'teamHerald% - ADCR'], axis=1)
        frame = frame.drop(
            ['teamNash% - JGB', 'teamNash% - MIDB', 'teamNash% - ADCB', 'teamNash% - SUPPB', 'teamNash% - TOPR',
             'teamNash% - JGR', 'teamNash% - MIDR', 'teamNash% - ADCR'], axis=1)

        cat = ['baron', 'dead - TOPB', 'dead - SUPPR', 'dead - JGB', 'dead - MIDB', 'dead - ADCB', 'dead - SUPPB',
               'dead - TOPR', 'dead - JGR', 'dead - MIDR', 'dead - ADCR', 'dragon', 'rift', 'wardsKilled - TOPB',
               'wardsKilled - SUPPR', 'wardsKilled - JGB', 'wardsKilled - MIDB', 'wardsKilled - ADCB',
               'wardsKilled - SUPPB', 'wardsKilled - TOPR', 'wardsKilled - JGR', 'wardsKilled - MIDR',
               'wardsKilled - ADCR',
               'wardsPlaced - TOPB', 'wardsPlaced - JGB', 'wardsPlaced - MIDB', 'wardsPlaced - ADCB',
               'wardsPlaced - SUPPB',
               'wardsPlaced - TOPR', 'wardsPlaced - JGR', 'wardsPlaced - MIDR', 'wardsPlaced - ADCR',
               'wardsPlaced - SUPPR']
        frame[cat] = (frame[cat] == 1)

        array_var_obj = ['wardsPlaced - TOPB', 'wardsPlaced - JGB', 'wardsPlaced - MIDB', 'wardsPlaced - ADCB',
                         'wardsPlaced - SUPPB', 'wardsPlaced - TOPR', 'wardsPlaced - JGR', 'wardsPlaced - MIDR',
                         'wardsPlaced - ADCR', 'wardsPlaced - SUPPR']
        array_var_ind = [col for col in frame.columns if col not in array_var_obj]

        frame[array_var_ind].to_csv('TestDataframe.csv')
        H2Odf = h2o.import_file('TestDataframe.csv')
        H2Odf = H2Odf.drop("C1")

        models = {}

        for var_obj in array_var_obj:
            models[var_obj] = h2o.load_model(var_obj.split(" - ")[1] + "_Best")
            frame[var_obj + "_predicted"] = models[var_obj].predict(H2Odf).as_data_frame()['predict'].tolist()

        with open('Predicted_' + gameCode + '.json', 'w') as outfile:
            json.dump(frame.to_dict(), outfile)

        if minute == 0:
            return frame.to_dict()
        else:
            img = plt.imread("mapa.PNG")
            lanes = ["TOP", "JG", "MID", "ADC", "SUPP"]

            xB, yB, playerB, xR, yR, playerR = [], [], [], [], [], []
            xB_predicted, yB_predicted, playerB_predicted, xR_predicted, yR_predicted, playerR_predicted = \
                [], [], [], [], [], []

            for lane in lanes:
                if frame.iloc[minute]["wardsPlaced - " + lane + "B"] == 1:
                    xB.append(frame.iloc[minute]["positionX - " + lane + "B"])
                    yB.append(frame.iloc[minute]["positionY - " + lane + "B"])
                    playerB.append(lane)
                if frame.iloc[minute]["wardsPlaced - " + lane + "R"] == 1:
                    xR.append(frame.iloc[minute]["positionX - " + lane + "R"])
                    yR.append(frame.iloc[minute]["positionY - " + lane + "R"])
                    playerR.append(lane)
                if frame.iloc[minute]["wardsPlaced - " + lane + "B_predicted"] == 1:
                    xB_predicted.append(frame.iloc[minute]["positionX - " + lane + "B"])
                    yB_predicted.append(frame.iloc[minute]["positionY - " + lane + "B"])
                    playerB_predicted.append(lane)
                if frame.iloc[minute]["wardsPlaced - " + lane + "R_predicted"] == 1:
                    xR_predicted.append(frame.iloc[minute]["positionX - " + lane + "R"])
                    yR_predicted.append(frame.iloc[minute]["positionY - " + lane + "R"])
                    playerR_predicted.append(lane)

            fig, ax = plt.subplots(figsize=(15, 15))
            ax.scatter(xB, yB, s=4000, c="b", alpha=0.4)
            ax.scatter(xR, yR, s=4000, c="r", alpha=0.4)
            ax.scatter(xB_predicted, yB_predicted, s=2000, c="g", alpha=0.4)
            ax.scatter(xR_predicted, yR_predicted, s=2000, c="y", alpha=0.4)

            for i, txt in enumerate(playerB):
                ax.text(xB[i], yB[i], s=txt, size="x-large", weight="bold", ha="center", va="center", style="oblique")
            for i, txt in enumerate(playerR):
                ax.text(xR[i], yR[i], s=txt, size="x-large", weight="bold", ha="center", va="center", style="oblique")
            for i, txt in enumerate(playerB_predicted):
                ax.text(xB_predicted[i], yB_predicted[i], s=txt, size="x-large", weight="bold", ha="center",
                        va="center",
                        style="oblique")
            for i, txt in enumerate(playerR_predicted):
                ax.text(xR_predicted[i], yR_predicted[i], s=txt, size="x-large", weight="bold", ha="center",
                        va="center",
                        style="oblique")

            ax.imshow(img, extent=[0, 15000, 0, 15000])
            fig.savefig('full_figure.png')

            return FileResponse("full_figure.png")
