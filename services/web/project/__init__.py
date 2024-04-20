import psycopg2
from flask import Flask, render_template
from nba_api.live.nba.endpoints import scoreboard

app = Flask(__name__)
app.config.from_object("project.config.Config")
app.config['SECRET_KEY'] = 'secret'
conn = psycopg2.connect(app.config["SQLALCHEMY_DATABASE_URI"])

def livescore():
    return scoreboard.ScoreBoard().games.get_dict()

@app.route('/')
def main():
    
    live = livescore()

    
    cur = conn.cursor()
    cur.execute('SELECT "abbreviation" FROM teams')
    teams = cur.fetchall()
    cur.execute('SELECT DISTINCT "POSITION" FROM playerinfo WHERE "POSITION" IS NOT NULL')
    positions = cur.fetchall()

    cur.execute('''
        SELECT column_name FROM information_schema.columns WHERE table_name = 'playercareerstats' 
        AND column_name NOT IN ('Team_ID', 'PLAYER_ID', 'LEAGUE_ID')
                
    ''')
    stats = cur.fetchall()
    cur.close()
    return render_template('index.html', teams=teams, positions=positions, stats=stats, live=live)


@app.route('/teams', methods=['GET', 'POST'])
def get_teams():
    cur = conn.cursor()

    cur.execute('''
        SELECT DISTINCT full_name
        FROM teams
        ORDER BY 1
    ''')
    teams = cur.fetchall()

    cur.execute('''
        SELECT DISTINCT CAST("SEASON_ID" AS INTEGER) % 10000 as season
        FROM games
        WHERE CAST("SEASON_ID" AS INTEGER) % 10000 >= 2014
        ORDER BY 1 DESC
    ''')
    years = cur.fetchall()

    cur.execute('''
        SELECT DISTINCT teams.full_name, CAST("SEASON_ID" AS INTEGER) % 10000 as season,
                games."WL", COUNT(*) as num
        FROM teams
    JOIN games ON games."TEAM_ID" = teams.id
    WHERE CAST("SEASON_ID" AS INTEGER) % 10000 >= 2014
    GROUP BY games."WL", teams.full_name, 2
    ORDER BY 1, 2 DESC;

    ''')
    teaminfo = cur.fetchall()

    cur.execute('''
        SELECT DISTINCT teams.full_name,
                games."WL", COUNT(*) as num
        FROM teams
    JOIN games ON games."TEAM_ID" = teams.id
    GROUP BY games."WL", teams.full_name
    ORDER BY 1, 3 DESC;

    ''')
    winloss = cur.fetchall()

    cur.close()  
    return render_template('teams.html', teams = teams, years = years, teaminfo = teaminfo, winloss = winloss)


@app.route('/teams/<team>/<wl>')
def teamgames(team, wl):
    cur = conn.cursor()

    cur.execute('''
        SELECT column_name FROM information_schema.columns
                WHERE table_name LIKE 'games'
                AND column_name NOT IN ('SEASON_ID', 'TEAM_ID', 'TEAM_NAME', 'GAME_ID', 'WL', 'MIN')
                ORDER BY ordinal_position
                ''')
    colnames = cur.fetchall()

    cur.execute(
        '''
        SELECT "TEAM_ABBREVIATION", "GAME_DATE", "MATCHUP", "PTS", "FGM", "FGA",
        "FG_PCT", "FG3M", "FG3A", "FG3_PCT", "FTM", "FTA", "FT_PCT",
        "OREB", "DREB", "REB", "AST", "STL", "BLK", "TOV", "PF", "PLUS_MINUS"
        FROM games WHERE
        games."TEAM_NAME" = %s AND
        games."WL" = %s

        ''', (team, wl, )
   )
    games = cur.fetchall()
    

    cur.close()
    return render_template('games.html', games=games, colnames=colnames)

@app.route('/teams/<team>/<date>/<matchup>')
def boxscores(team, date, matchup):
    cur = conn.cursor()

    cur.execute('''
        SELECT column_name FROM information_schema.columns
                WHERE table_name LIKE 'regseasonboxscores'
                AND column_name NOT IN ('gameId', 'teamId', 'teamSlug', 'personId', 'nameI', 'playerSlug', 'jerseyNum', 'comment')
                ORDER BY ordinal_position
                ''')
    colnames = cur.fetchall()

    cur.execute('''
            WITH scores AS (SELECT *
            FROM playoffboxscores
                UNION 
                SELECT * FROM regseasonboxscores)
        SELECT "teamCity", "teamName" , "teamTricode", "firstName", "familyName", 
                "position", "minutes", "fieldGoalsMade", 
                "fieldGoalsAttempted", "fieldGoalsPercentage", "threePointersMade", "threePointersAttempted", 
                "threePointersPercentage", "freeThrowsMade", "freeThrowsAttempted", "freeThrowsPercentage",
                "reboundsOffensive", "reboundsDefensive", "reboundsTotal", "assists", "steals", "blocks", "turnovers",
                "foulsPersonal", "points", "plusMinusPoints" FROM scores
        JOIN games ON scores."gameId" = games."GAME_ID"
        WHERE
        games."TEAM_ABBREVIATION" = %s 
        AND games."GAME_DATE" = %s
        AND games."MATCHUP" = %s
                ''', (team, date, matchup,))
    boxscores = cur.fetchall()
    

    cur.close()
    return render_template('gamestats.html', colnames=colnames, boxscores=boxscores)

@app.route('/teams/<team>/<date>/pbp')
def pbp(team, date):
    cur = conn.cursor()

    cur.execute('''
        SELECT column_name FROM information_schema.columns
                WHERE table_name = 'regseasonpbp'
                ORDER BY ordinal_position
                ''')
    colnames = cur.fetchall()

    cur.execute('''
            WITH pbp AS (SELECT *
            FROM playoffspbp
                UNION 
                SELECT * FROM regseasonpbp)
        SELECT 
               *
        FROM pbp
        JOIN games ON pbp."gameId" = games."GAME_ID"
        WHERE
        games."TEAM_ABBREVIATION" = %s 
        AND games."GAME_DATE" = %s
                ''', (team, date,))
    pbp = cur.fetchall()
    cur.close()
    return render_template('pbp.html', colnames=colnames, pbp=pbp)

@app.route('/players')
def player():
    cur = conn.cursor()

    cur.execute('''
        SELECT ARRAY_AGG(full_name), playerinfo."POSITION" FROM players
                JOIN playerinfo
                ON players.id=playerinfo."PERSON_ID"
                WHERE is_active = 'true' AND playerinfo."POSITION" IS NOT NULL
                GROUP BY 2
                ''')
    players = cur.fetchall()

    cur.execute('''
        SELECT DISTINCT "POSITION" FROM playerinfo
                WHERE "POSITION" IS NOT NULL
                ''')
    position = cur.fetchall()
    cur.close()
    return render_template('players.html', players=players, position=position)

if __name__ == '__main__':
    app.run(debug=True)


