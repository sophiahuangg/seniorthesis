import psycopg2
from flask import Flask, render_template, request , Blueprint
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

    cur.execute(
        '''
        SELECT "TEAM_NAME", "GAME_DATE", "MATCHUP", "PTS", "FG_PCT", "FG3_PCT", 
                "REB", "AST", "STL", "BLK", "TOV"
        FROM games WHERE
        games."TEAM_NAME" = %s AND
        games."WL" = %s

        ''', (team, wl, )
   )
    games = cur.fetchall()
    
    colnames = []
    for column in cur.description:
        colnames.append(column)

    cur.close()
    return render_template('games.html', games=games, colnames=colnames)


@app.route('/teams/<team>/<date>/<matchup>')
def boxscores(team, date, matchup):
    cur = conn.cursor()


    cur.execute('''
            WITH scores AS (SELECT *
            FROM playoffboxscores
                UNION 
                SELECT * FROM regseasonboxscores)
        SELECT CONCAT("teamCity", ' ', "teamName") AS "team", CONCAT("firstName", ' ', "familyName") AS "player", 
                "position", "minutes", "fieldGoalsMade", 
                "threePointersMade",  "freeThrowsMade", "reboundsTotal", "assists", 
                "foulsPersonal", "points" FROM scores
        JOIN games ON scores."gameId" = games."GAME_ID"
        WHERE
        games."TEAM_ABBREVIATION" = %s 
        AND games."GAME_DATE" = %s
        AND games."MATCHUP" = %s
                ''', (team, date, matchup,))
    boxscores = cur.fetchall()
    
    colnames = []
    for column in cur.description:
        colnames.append(column)

    cur.close()
    return render_template('gamestats.html', colnames=colnames, boxscores=boxscores)


@app.route('/teams/<team>/<date>/pbp')
def pbp(team, date):
    cur = conn.cursor()

    cur.execute('''
            WITH pbp AS (SELECT *
            FROM playoffspbp
                UNION 
                SELECT * FROM regseasonpbp)
        SELECT 
                "clock", "teamTricode", CONCAT("playerName", ' ', "playerNameI") AS "player",
                "description", "actionType", "scoreHome", "scoreAway", "pointsTotal"
        FROM pbp
        JOIN games ON pbp."gameId" = games."GAME_ID"
        WHERE
        games."TEAM_ABBREVIATION" = %s 
        AND games."GAME_DATE" = %s
                ''', (team, date,))
    pbp = cur.fetchall()

    cur.execute('''
                SELECT "MATCHUP" FROM games
                WHERE games."TEAM_ABBREVIATION" = %s AND games."GAME_DATE" = %s
                ''', (team, date,))

    matchup = cur.fetchall()

    colnames = []
    for column in cur.description:
        colnames.append(column)

    cur.close()
    return render_template('pbp.html', colnames=colnames, pbp=pbp, date=date, matchup=matchup)

@app.route('/players', methods=['GET', 'POST'])
def player():
    cur = conn.cursor()

    player = request.args.get("player")
    print("player=", player)
    if player:
        cur.execute('''
            SELECT full_name, playerinfo."POSITION" FROM players
                    JOIN playerinfo
                    ON players.id=playerinfo."PERSON_ID"
                    WHERE is_active = 'true' AND playerinfo."POSITION" IS NOT NULL 
                    AND players.full_name ILIKE %s
                    ''', ('%' + player + '%',))
        players = cur.fetchall()
    else:
        cur.execute('''
            SELECT full_name, playerinfo."POSITION" FROM players
                    JOIN playerinfo
                    ON players.id=playerinfo."PERSON_ID"
                    WHERE is_active = 'true' AND playerinfo."POSITION" IS NOT NULL
                    ''')
        players = cur.fetchall()
    cur.close()
    return render_template('players.html', players=players)


if __name__ == '__main__':
    app.run(debug=True)


