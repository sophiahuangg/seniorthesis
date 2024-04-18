import pandas as pd, time, os, asyncio, aiohttp
from nba_api.stats.endpoints import leaguegamefinder, playbyplayv3

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

gamefinder = leaguegamefinder.LeagueGameFinder(league_id_nullable='00', season_type_nullable='Regular Season').get_data_frames()[0]

# Getting Play By Play Data

playdf = pd.read_csv('datasets/regSeasonPBP.csv')


num = 14492
for id in gamefinder['GAME_ID'].unique().tolist()[14492:]:
	try:
		playdf = pd.concat([playdf, playbyplayv3.PlayByPlayV3(id).play_by_play.get_data_frame()], axis = 0)
		print("SUCCESS ON ", id, "; num ", num)
		num+=1
	except Exception as e:
		print("ERROR on id ", id)
		print("Error=", type(e).__name__)
		playdf.to_csv(('datasets/regSeasonPBP.csv'), index = False)
		num+=1
		break
