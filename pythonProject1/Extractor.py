import leaguepedia_parser as lp

print(lp.get_regions())

tournaments = lp.get_tournaments('Europe', year=2021)
print([t["name"] for t in tournaments])

import types
from leaguepedia_parser.site.leaguepedia import leaguepedia


def get_games_hashes(self, tournament_name=None, **kwargs):
    """Returns the list server, gameId and hashes of games played in a tournament.

    :param tournament_name
                Name of the tournament, which can be gotten from get_tournaments().
    :return:
                A list of game dictionaries.
    """
    games = leaguepedia.query(tables='ScoreboardGames',
                              fields='Tournament = tournament, ''MatchHistory = match_history_url, ',
                              where="ScoreboardGames.Tournament='{}'".format(tournament_name),
                              order_by="ScoreboardGames.DateTime_UTC",
                              **kwargs)
    data = [
        {
            "tournament": game["tournament"],
            "server": game["match_history_url"].split("/")[5],
            "gameId": game["match_history_url"].split("/")[6].split("?gameHash=")[0],
            "hash": game["match_history_url"].split("/")[6].split("?gameHash=")[1],
        }
        for game in games
    ]
    return data


lp.get_games_hashes = types.MethodType(get_games_hashes, lp)
games = lp.get_games_hashes('LEC 2021 Spring')
print(games[:3])

cookies = "ajs_group_id=null; ajs_user_id=null; osano_consentmanager_uuid=586d90e4-135d-469f-af88-b51ca0392758; osano_consentmanager_expdate=1641910356172; _gcl_au=1.1.20772009.1609774663; _gid=GA1.2.523524002.1609774663; _hjTLDTest=1; _hjid=4aa280a0-12ac-4291-9e2b-fe249a47f84e; _hjFirstSeen=1; ping_session_id=106ffd64-05c5-4765-aeaf-b4706d7c6eb4; _hjAbsoluteSessionInProgress=0; _tli=6864292941341953194; PVPNET_TOKEN_LAN=eyJkYXRlX3RpbWUiOjE2MDk3NzQ2ODE2MDcsImdhc19hY2NvdW50X2lkIjoyMDA5NjI0MTUsInB2cG5ldF9hY2NvdW50X2lkIjoyMDA5NjI0MTUsInN1bW1vbmVyX25hbWUiOiJjcmlzbWFudGkyMCIsInZvdWNoaW5nX2tleV9pZCI6IjkwMzQ3NTJiMmI0NTYwNDRhZTg3ZjI1OTgyZGFkMDdkIiwic2lnbmF0dXJlIjoiZFZMejVSR2p4RFRLMWpydEZaU2U5VU92U0gxaDIxbWR0alRLZ29aT2JZQkkzVFRkZFdDMEhGZWZjREhORlRuWDZJOFA3SVpJNlprVkFGM0M5VzB6ckFoZDFXc3FNeXo5TklMbWQ0ZXJsNHREdXlTdTFUR0xEVlRLT1RYek5YN28rR0F5a1ZEa014TkpjNEhiSVQvUUU3MzYwTmlmN1VYcUxuZ0wyN21ueEFRPSJ9; PVPNET_ACCT_LAN=crismanti20; PVPNET_ID_LAN=200962415; PVPNET_REGION=lan; PVPNET_LANG=es_ES; id_token=eyJraWQiOiJzMSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiIyYWNmYWM4Ni03ZDg2LTU2OTgtOGU1MS00NWJiNWI4NjA3Y2UiLCJjb3VudHJ5IjoiY29sIiwicGxheWVyX3Bsb2NhbGUiOiJlbi1VUyIsImFtciI6WyJwYXNzd29yZCJdLCJpc3MiOiJodHRwczpcL1wvYXV0aC5yaW90Z2FtZXMuY29tIiwibG9sIjpbeyJjdWlkIjoyMDA5NjI0MTUsImNwaWQiOiJMQTEiLCJ1aWQiOjIwMDk2MjQxNSwidW5hbWUiOiJDbWFudGkiLCJwdHJpZCI6bnVsbCwicGlkIjoiTEExIiwic3RhdGUiOiJFTkFCTEVEIn1dLCJsb2NhbGUiOiJlc19FUyIsImF1ZCI6InJzby13ZWItY2xpZW50LXByb2QiLCJhY3IiOiJ1cm46cmlvdDpicm9uemUiLCJwbGF5ZXJfbG9jYWxlIjoiZW4tVVMiLCJleHAiOjE2MDk4NjEwODAsImlhdCI6MTYwOTc3NDY4MCwiYWNjdCI6eyJnYW1lX25hbWUiOiJjcmlzbWFudGkyMCIsInRhZ19saW5lIjoiTEFOIn0sImp0aSI6IkFRdEpDYUlvWU9BIiwibG9naW5fY291bnRyeSI6ImNvbCJ9.GJHIfn_GlVL7IJ10NtkANiaXLplUzaZg5LlPVma5nv9o5Qik6ZqLiRAzQL-a1fpGDdPFso340ERLlwscgJDh1bp9apTFL9-8_ezVvL1Nj6O92OAILVQG-kVOu5XnEjFany0aEUMKfa1I6gyviuhqSzwjnCwONZwtaMCDj7D5ztk; id_hint=sub%3D2acfac86-7d86-5698-8e51-45bb5b8607ce%26lang%3Des%26game_name%3Dcrismanti20%26tag_line%3DLAN%26id%3D200962415%26summoner%3Dcrismanti20%26region%3DLA1%26tag%3Dlan; __cfduid=d135ba66f522c2a1b88562170a9670baf1609774683; osano_consentmanager=oe4vGLfdiMusKqf4aCfbA3h2dBNuChJoqlgX4K71YZvG_Z3PfHbgVDP5c_ewkjB_nk1YDDsm6gieusi0ppc0n4tQsII6VD6sBXoZWYOq-_Ctg7IXK-79TJw72S-ZfaE8C-PEJU2JpDLfecgmOdiJLLHjA8fGb1cX6DGSeeGIWroxZrpesuUcI-v0mKkHDKxYigrfQQIl5InEbuZFqJ-m3SKjhaMDeTpUkqaea1ntexSWorOePFW6w9L2YnSIv2fsgny6YFAuKhJilh3XakncN00RWKGt27e8a9glkWAkY_U0h1Aj7pDlTJ732GJlFw4AdtyCxg==; _ga_FXBJE5DEDD=GS1.1.1609774662.1.1.1609774684.38; _tlc=login.lolesports.com%2F:1609774684:na.leagueoflegends.com%2Fes-mx%2F:leagueoflegends.com; _tlv=1.1609774664.1609774664.1609774684.2.1.2; _ga=GA1.2.985745498.1608732737; _tlp=2820:16705876; _tls=*.1069393:1069394..6864292941341953194"

import requests
import json

base_match_history_stats_url = "https://acs.leagueoflegends.com/v1/stats/game/{}/{}?gameHash={}"
base_match_history_stats_timeline_url = "https://acs.leagueoflegends.com/v1/stats/game/{}/{}/timeline?gameHash={}"

all_games_data = []

for g in games:
    url = base_match_history_stats_url.format(g["server"], g["gameId"], g["hash"])
    timeline_url = base_match_history_stats_timeline_url.format(g["server"], g["gameId"], g["hash"])

    game_data = requests.get(url, cookies={c.split("=")[0]: c.split("=")[1] for c in cookies.split(";")}).json()
    timeline_data = requests.get(timeline_url,
                                 cookies={c.split("=")[0]: c.split("=")[1] for c in cookies.split(";")}).json()

    with open('D:/USUARIO/Documents/JsonGames2021/' + g["gameId"] + '.json', 'w') as outfile:
        json.dump(game_data, outfile)

    with open('D:/USUARIO/Documents/JsonTimeline2021/' + g["gameId"] + '_timeline.json', 'w') as outfile:
        json.dump(timeline_data, outfile)

