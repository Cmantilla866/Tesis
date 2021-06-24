import json
import pandas as pd

with open('D:/USUARIO/Documents/JsonTimeLine/1530436_timeline.json') as json_file:
    timeline = json.load(json_file)
    print(timeline.keys())
    participantFrames = []
    events = []
    frames = timeline['frames']
    print(frames[0].keys())
    print(frames[0]["events"][0].keys())
    print(len(frames[0]["participantFrames"]))
    for frame in range(len(frames)):
        for ev in range(len(frames[frame]["events"])):
            if not events.__contains__(frames[frame]["events"][ev]["type"]):
                events.append(frames[frame]["events"][ev]["type"])
    print(events)
    for XD in range(1,6):
        print(XD)
    with open('D:/USUARIO/Documents/Json/champion-summary.json') as json_champions:
        champions = json.load(json_champions)
        print(champions[0]["id"]==-1)
    champions = pd.read_json('D:/USUARIO/Documents/Json/champion-summary.json')
    championStats = pd.read_csv("D:/USUARIO/Documents/Json/championStats (1).csv")
    print(champions.columns)

    with open('D:/USUARIO/Documents/JsonTimeLine/1530436_timeline.json') as json_file:
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
        with open('D:/USUARIO/Documents/JsonGames/1530436.json') as json_game:
            game = json.load(json_game)
            team = game["participantIdentities"][0]["player"]["summonerName"].split()[0]
            print(game.keys())
            participants = game["participants"]
            participantFrames[0]["1"]["championId"] = \
                participants[0]["championId"]
            participantFrames[0]["1"]["championCSD"] = championStats[championStats["Champion"] == champions[champions["id"] == participantFrames[0]["1"]["championId"]]["name"].values[0]]["CSD@15"].values[0]
            #print(participantFrames[0]["1"]["championCSD"])
            #print(type(champions[champions["id"] == participantFrames[0]["1"]["championId"]]["name"].values[0]))
