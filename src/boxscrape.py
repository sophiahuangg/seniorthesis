import pandas as pd, time
from nba_api.stats.endpoints import leaguegamefinder, BoxScoreTraditionalV3

# Use SeasonId class from the NBA API



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

playoffboxscores = pd.DataFrame()


# Getting League Games

playoffs = leaguegamefinder.LeagueGameFinder(league_id_nullable='00', season_type_nullable='Regular Season', game_id_nullable='11700012').get_data_frames()[0]
print(playoffs)
'''
num = 0
for id in playoffs['GAME_ID'].unique().tolist():
	try:
		playoffboxscores = pd.concat([playoffboxscores, boxscoretraditionalv3.BoxScoreTraditionalV3(id).player_stats.get_data_frame()], axis=0)
		print("Finished id ", id)
		num += 1
		print("num=", num)
		time.sleep(0.1)
	except Exception as e:
		print("Error=", type(e).__name__)
		print("Failed on ", id)
		break


playoffboxscores.to_csv(('../datasets/regseasonboxscores.csv'), index = False)
'''
