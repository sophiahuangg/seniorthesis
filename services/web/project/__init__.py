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

    cur.close()
    return render_template('index.html', teams=teams, live=live)


@app.route('/teams', methods=['GET', 'POST'])
def get_teams():
    cur = conn.cursor()

    cur.execute('''
        SELECT DISTINCT full_name, abbreviation
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
    GROUP BY games."WL", teams.full_name, 2, 3
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
        SELECT "TEAM_NAME", "GAME_DATE" AS "GAME DATE", "MATCHUP", 
        ROUND(CAST("PTS" AS numeric), 0) AS "PTS", 
        ROUND(CAST("FG_PCT"*100 AS numeric), 2) AS "FG PCT", 
        ROUND(CAST("FG3_PCT"*100 AS numeric), 2) AS "FG3 PCT", 
        ROUND(CAST("FT_PCT"*100 AS numeric), 2) AS "FT PCT",
        ROUND(CAST("REB" AS numeric), 0) AS "REB", 
        ROUND(CAST("AST" AS numeric), 0) AS "AST", 
        ROUND(CAST("STL" AS numeric), 0) AS "STL", 
        ROUND(CAST("BLK" AS numeric), 0) AS "BLK", 
        ROUND(CAST("TOV" AS numeric), 0) AS "TOV"
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
        CREATE TEMP TABLE IF NOT EXISTS boxsc AS 
        WITH scores AS (SELECT *
            FROM playoffboxscores
                UNION 
                SELECT * FROM regseasonboxscores)
        SELECT CONCAT("teamCity", ' ', "teamName") AS "TEAM NAME", CONCAT("firstName", ' ', "familyName") AS "PLAYER", 
                "position" AS "POSITION", "minutes" AS "MINUTES", 
                CONCAT(ROUND(CAST("fieldGoalsMade" AS numeric), 0), '-', ROUND(CAST("fieldGoalsAttempted" AS numeric), 0)) AS "FG",
                CONCAT(ROUND(CAST("freeThrowsMade" AS numeric), 0), '-', ROUND(CAST("freeThrowsAttempted" AS numeric), 0)) AS "FT",
                CONCAT(ROUND(CAST("threePointersMade" AS numeric), 0), '-', ROUND(CAST("threePointersAttempted" AS numeric), 0)) AS "3P",
                ROUND(CAST("reboundsTotal" AS numeric), 0) AS "REB", 
                ROUND(CAST("assists" AS numeric), 0) AS "AST", 
                ROUND(CAST("foulsPersonal" AS numeric), 0) AS "FOULS", 
                ROUND(CAST("points" AS numeric), 0) AS "PTS" FROM scores
        JOIN games ON scores."gameId" = games."GAME_ID"
        WHERE
        games."TEAM_ABBREVIATION" = %s 
        AND games."GAME_DATE" = %s
        AND games."MATCHUP" = %s
        ORDER BY 1, "PTS" DESC
        ''', (team, date, matchup,))
    
    cur.execute('''
    SELECT * FROM boxsc
                ''')

    boxscores = cur.fetchall()
    
    colnames = []
    for column in cur.description:
        colnames.append(column)

    cur.execute('''
        SELECT "TEAM NAME", "PLAYER", "PTS" FROM boxsc
        ORDER BY "PTS" DESC
        LIMIT 5
            ''')
    
    topscore = cur.fetchall()
    
    scrcol = []
    for column in cur.description:
        scrcol.append(column)

    cur.execute('''
        SELECT "TEAM NAME", "PLAYER", "AST" FROM boxsc
        ORDER BY "AST" DESC
        LIMIT 5
            ''')
    
    topast = cur.fetchall()
    
    astcol = []
    for column in cur.description:
        astcol.append(column)

        cur.execute('''
        SELECT "TEAM NAME", "PLAYER", "REB" FROM boxsc
        ORDER BY "REB" DESC
        LIMIT 5
            ''')
    
    topreb = cur.fetchall()
    
    rebcol = []
    for column in cur.description:
        rebcol.append(column)

    cur.close()
    return render_template('gamestats.html', colnames=colnames, boxscores=boxscores, date=date, matchup=matchup, topscore=topscore, scrcol=scrcol, topast=topast, astcol=astcol,
                           topreb=topreb, rebcol=rebcol)


@app.route('/teams/<team>/<date>/pbp')
def pbp(team, date):
    cur = conn.cursor()

    cur.execute('''
            WITH pbp AS (SELECT "gameId", "clock", "teamTricode", "playerName", "playerNameI",
                "description", "actionType", "scoreHome", "scoreAway", "pointsTotal"
            FROM playoffspbp
                UNION 
                SELECT "gameId", "clock", "teamTricode", "playerName",  "playerNameI",
                "description", "actionType", "scoreHome", "scoreAway", "pointsTotal"
            FROM regseasonpbp)
        SELECT 
                "clock" as "CLOCK", "teamTricode" AS "TEAM", CONCAT("playerName", ' ', "playerNameI") AS "PLAYER",
                "description" AS "DESCRIPTION", "actionType" AS "ACTION", ROUND(CAST("scoreHome" AS numeric), 0) AS "HOME SCORE", ROUND(CAST("scoreAway" AS numeric), 0) AS "AWAY SCORE", ROUND(CAST("pointsTotal" AS numeric), 0) AS "TOTAL POINTS"
        FROM pbp
        JOIN games ON pbp."gameId" = games."GAME_ID"
        WHERE
        games."TEAM_ABBREVIATION" = %s 
        AND games."GAME_DATE" = %s
        AND pbp."teamTricode" is NOT NULL
        ORDER BY pbp."pointsTotal", pbp."clock"
                ''', (team, date,))
    pbp = cur.fetchall()
    
    colnames = []
    for column in cur.description:
        colnames.append(column)

    cur.execute('''
                SELECT "MATCHUP" FROM games
                WHERE games."TEAM_ABBREVIATION" = %s AND games."GAME_DATE" = %s
                ''', (team, date,))

    matchup = cur.fetchall()

    cur.close()
    return render_template('pbp.html', colnames=colnames, pbp=pbp, date=date, matchup=matchup)

@app.route('/players', methods=['GET', 'POST'])
def player():
    player = request.args.get("player")
    print("Player:", player)

    cur = conn.cursor()

    if player:
        cur.execute('''
            SELECT  players.full_name AS "NAME", playerinfo."TEAM_ABBREVIATION" AS "TEAM", playerinfo."JERSEY" AS "NUMBER", playerinfo."POSITION", playerinfo."HEIGHT", 
                    ROUND(CAST(playerinfo."WEIGHT" AS numeric), 0) AS "WEIGHT", ROUND(CAST(playercareerstats."FG_PCT"*100 AS numeric), 2) AS "FG PCT", 
                    ROUND(CAST(playercareerstats."FG3_PCT"*100 AS numeric), 2) AS "FG3 PCT",
                    ROUND(CAST(playercareerstats."FT_PCT"*100 AS numeric), 2) AS "FT PCT" FROM players
                    JOIN playerinfo
                    ON players.id=playerinfo."PERSON_ID"
                    JOIN playercareerstats ON players.id=playercareerstats."PLAYER_ID"
                    WHERE is_active = 'true' AND playerinfo."POSITION" IS NOT NULL 
                    AND players.full_name ILIKE %s
                    ''', ('%' + player + '%',))
        players = cur.fetchall()
    else:
        cur.execute('''
            SELECT  players.full_name AS "NAME", playerinfo."TEAM_ABBREVIATION" AS "TEAM", playerinfo."JERSEY" AS "NUMBER", playerinfo."POSITION", playerinfo."HEIGHT", 
                    ROUND(CAST(playerinfo."WEIGHT" AS numeric), 0) AS "WEIGHT", ROUND(CAST(playercareerstats."FG_PCT"*100 AS numeric), 2) AS "FG PCT", 
                    ROUND(CAST(playercareerstats."FG3_PCT"*100 AS numeric), 2) AS "FG3 PCT",
                    ROUND(CAST(playercareerstats."FT_PCT"*100 AS numeric), 2) AS "FT PCT" FROM players
                    JOIN playerinfo
                    ON players.id=playerinfo."PERSON_ID"
                    JOIN playercareerstats ON players.id=playercareerstats."PLAYER_ID"
                    WHERE is_active = 'true' AND playerinfo."POSITION" IS NOT NULL 
                    ''')
        players = cur.fetchall()
        
    colnames = []
    for column in cur.description:
        colnames.append(column)

    cur.close()
    return render_template('players.html', players=players, colnames=colnames, player=player)

@app.route('/<team>/roster')
def teamlist(team):
    cur = conn.cursor()
    cur.execute('''
    SELECT CONCAT("FIRST_NAME", ' ', "LAST_NAME") AS "NAME",
                "COUNTRY",
                "BIRTHDATE"::date,
                "POSITION",
                "JERSEY",
                CONCAT("DRAFT_YEAR", ' Round ', "DRAFT_ROUND", ' Pick ', "DRAFT_NUMBER") AS "NBA DRAFT"
                FROM playerinfo
                JOIN players 
                ON players.id=playerinfo."PERSON_ID"
                JOIN teams
                ON playerinfo."TEAM_ID"=teams.id
                WHERE is_active = 'true'
                AND playerinfo."TEAM_ABBREVIATION" = %s
                ''', (team,))
    roster = cur.fetchall()
    
    colnames = []
    for column in cur.description:
        colnames.append(column)

    cur.execute('''
                SELECT full_name FROM teams
                WHERE teams.abbreviation = %s
                ''', (team,))
    teamname = cur.fetchall()
                
    cur.close()
    return render_template('teamroster.html', roster=roster, colnames=colnames, teamname=teamname)

if __name__ == '__main__':
    app.run(debug=True)


