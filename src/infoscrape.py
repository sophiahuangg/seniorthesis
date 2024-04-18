import pandas as pd, time, os, asyncio, aiohttp
from nba_api.stats.endpoints import leaguegamefinder, commonplayerinfo, playercareerstats
from nba_api.stats.static import teams, players


dir = 'datasets'
if not os.path.exists(dir):
	os.makedirs(dir)

custom_headers = {
    'Host': 'stats.nba.com',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
}

'''
# Getting all teams
teamsdf = pd.DataFrame(teams.get_teams())
teamsdf.to_csv(os.path.join(dir, 'teams.csv'), index = False)

# Getting all players
playersdf = pd.DataFrame(players.get_players())
playersdf.to_csv(os.path.join(dir, 'players.csv'), index = False)
'''

# Getting League Games
gamefinder = leaguegamefinder.LeagueGameFinder(league_id_nullable='00').get_data_frames()[0]
gamefinder.to_csv(os.path.join(dir, 'games.csv'), index = False)

'''
# Getting active player information as well and player statistics
playerinfodf = pd.DataFrame()
statsdf = pd.DataFrame()

for i in players.get_active_players():
	try:
		playerinfo = commonplayerinfo.CommonPlayerInfo(player_id = i['id']).common_player_info.get_data_frame()
		playerinfodf = pd.concat([playerinfodf, playerinfo], axis=0)
		time.sleep(0.3)
		statsinfo = playercareerstats.PlayerCareerStats(player_id = i['id']).career_totals_regular_season.get_data_frame()
		statsdf = pd.concat([statsdf, statsinfo], axis=0)
		time.sleep(0.3)
		print(i)
	except requests.exceptions.RequestException as e:
		print(f"Error on attempt {i}")

playerinfodf.to_csv(os.path.join(dir, 'playerinfo.csv'), index = False)
statsdf.to_csv(os.path.join(dir, 'playercareerstats.csv'), index = False)
'''

