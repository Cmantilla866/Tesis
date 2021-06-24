import json
import os
import pandas as pd
import numpy as np
import math
data = []
sightItems = [3860, 3859, 3855, 3857, 3098, 3853, 3340, 3363, 2055, 3364]
sightItemsNames = {"3860": "BulwarkOfTheMountain", "3859": "TargonsBuckler", "3855": "RunesteelSpaulders",
                   "3857": "PauldronsOfWhiterock", "3098": "Frostfang", "3853": "ShardOfTrueIce",
                   "3340": "WardingTotem", "3363": "FarsightAlteration", "2055": "ControlWard", "3364": "OracleLens"}
springStats = pd.read_csv("D:/USUARIO/Documents/Json/Spring2021.csv")
summerStats = pd.read_csv("D:/USUARIO/Documents/Json/Summer2021.csv")
champions = pd.read_json('D:/USUARIO/Documents/Json/champion-summary.json')
championStats = pd.read_csv("D:/USUARIO/Documents/Json/championStats (2).csv")
for filename in os.listdir('D:/USUARIO/Documents/JsonGames2021'):
    gameCode = filename.replace(".json","")
    print(gameCode)
    # with open('D:/USUARIO/Documents/JsonTimeline/1120126_timeline.json') as json_file:
    with open('D:/USUARIO/Documents/JsonTimeLine2021/'+gameCode+'_timeline.json') as json_file:
        timeline = json.load(json_file)
        #print(timeline.keys())
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
        with open('D:/USUARIO/Documents/JsonGames2021/'+gameCode+'.json') as json_game:
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

                    if game["platformId"] == "ESPORTSTMNT04":
                        participantFrames[participantFrame][participant]["teamDragon%"] = int(springStats[
                            springStats["Team"] == team]["DRA%"].values[0])
                        participantFrames[participantFrame][participant]["teamHerald%"] = int(springStats[
                            springStats["Team"] == team]["HER%"].values[0])
                        participantFrames[participantFrame][participant]["teamNash%"] = int(springStats[
                            springStats["Team"] == team]["NASH%"].values[0])
                    else:
                        participantFrames[participantFrame][participant]["teamDragon%"] = int(summerStats[
                            summerStats["Team"] == team]["DRA%"].values[0])
                        participantFrames[participantFrame][participant]["teamHerald%"] = int(summerStats[
                            summerStats["Team"] == team]["HER%"].values[0])
                        participantFrames[participantFrame][participant]["teamNash%"] = int(summerStats[
                            summerStats["Team"] == team]["NASH%"].values[0])

                    participantFrames[participantFrame][participant]["championId"] = \
                        participants[int(participant) - 1]["championId"]

                    try:
                        participantFrames[participantFrame][participant]["championCSD"] = int(championStats[
                                                                                                  championStats[
                                                                                                      "Champion"] ==
                                                                                                  champions[
                                                                                                      champions["id"] ==
                                                                                                      participantFrames[
                                                                                                          participantFrame][
                                                                                                          participant][
                                                                                                          "championId"]][
                                                                                                      "name"].values[
                                                                                                      0]][
                                                                                                  "CSD@15"].values[0])

                        participantFrames[participantFrame][participant]["championGD"] = int(championStats[
                                                                                                 championStats[
                                                                                                     "Champion"] ==
                                                                                                 champions[
                                                                                                     champions["id"] ==
                                                                                                     participantFrames[
                                                                                                         participantFrame][
                                                                                                         participant][
                                                                                                         "championId"]][
                                                                                                     "name"].values[0]][
                                                                                                 "GD@15"].values[0])

                        participantFrames[participantFrame][participant]["championXPD"] = int(championStats[
                                                                                                  championStats[
                                                                                                      "Champion"] ==
                                                                                                  champions[
                                                                                                      champions["id"] ==
                                                                                                      participantFrames[
                                                                                                          participantFrame][
                                                                                                          participant][
                                                                                                          "championId"]][
                                                                                                      "name"].values[
                                                                                                      0]][
                                                                                                  "XPD@15"].values[0])
                    except:
                        participantFrames[participantFrame][participant]["championCSD"] = 0

                        participantFrames[participantFrame][participant]["championGD"] = 0

                        participantFrames[participantFrame][participant]["championXPD"] = 0

                    #participantFrames[participantFrame][participant]["teamId"] =
                    # participants[int(participant) - 1]["teamId"]
                    participantFrames[participantFrame][participant]["wardsPlaced"] = 0
                    participantFrames[participantFrame][participant]["wardsKilled"] = 0

                    if int(participant) <= 5:
                        participantFrames[participantFrame][participant]["goldDiff"] = \
                            participantFrames[participantFrame][participant]["totalGold"] - \
                            participantFrames[participantFrame][str(int(participant)+5)]["totalGold"]
                        participantFrames[participantFrame][participant]["xpDiff"] = \
                            participantFrames[participantFrame][participant]["xp"] - \
                            participantFrames[participantFrame][str(int(participant) + 5)]["xp"]
                    del participantFrames[participantFrame][participant]["totalGold"]
                    del participantFrames[participantFrame][participant]["xp"]

                    items = []
                    for item in range(3):
                        if not participantFrame == 0:
                            if not participantFrames[participantFrame - 1][participant]["item" + str(item)] == 0:
                                items.append(participantFrames[participantFrame - 1][participant]["item" + str(item)])

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

                    for item in range(len(items)):
                        participantFrames[participantFrame][participant]["item" + str(item)] = items[item]

                    del participantFrames[participantFrame][participant]["participantId"]
                    for key in participantFrames[participantFrame][participant].keys():
                        frame[key + " - " + participant] = participantFrames[participantFrame][participant][key]
                frame["minute"] = participantFrame + 1
                frame["dragon"] = Dragon
                frame["rift"] = Rift
                frame["baron"] = Baron
                #print(frame)
                data.append(frame)
                # print(participantFrames[participantFrame])

        """WardEvents = []
        for event in range(len(events)):

            if events[event]['type'] == 'WARD_PLACED':
                events[event]['participantId'] = events[event]['creatorId']
                del events[event]['creatorId']
                WardEvents.append(events[event])

            if events[event]['type'] == 'WARD_KILL':
                events[event]['participantId'] = events[event]['killerId']
                del events[event]['killerId']
                WardEvents.append(events[event])

        #print(WardEvents)

        for wardEvent in range(len(WardEvents)):
            minute = math.floor(WardEvents[wardEvent]["timestamp"]/60000)
            WardEvents[wardEvent]["position"] = participantFrames[minute][str(WardEvents[wardEvent]["participantId"])]["position"]
            print(WardEvents[wardEvent])
        print(len(WardEvents))"""

with open('D:/USUARIO/Documents/Json/DataFrame2021.json', 'w') as outfile:
    json.dump(data, outfile)

    #
