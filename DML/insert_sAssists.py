import requests
import oracledb
import cx_Oracle
import os

cx_Oracle.init_oracle_client(lib_dir="C:\Program Files\instantclient_21_12")

season = 20232024

def getGames():
    games = requests.get("https://api-web.nhle.com/v1/schedule/2023-09-01").json()
    seasonStart = games['regularSeasonStartDate']
    games = []
    i = 0
    while i < 4:
        firstWeek = requests.get("https://api-web.nhle.com/v1/schedule/" + str(seasonStart)).json()
        seasonStart = firstWeek['nextStartDate']
        for day in firstWeek["gameWeek"]:
            for game in day['games']:
                if game['gameState'] != "OFF":
                    return games
                games.append(game)
            
        i = i + 1

    return games


def getConnection():
    try:
        username = os.environ.get("zOracleDb_user")
        password = os.environ.get("zOracleDb_Pass")
        connect_string = "tcps://adb.us-phoenix-1.oraclecloud.com:1522/fssjrzpe2zgsiup_seis630fall2023_high.adb.oraclecloud.com?" \
        "wallet_location=C:/Users/fleon/OneDrive/Desktop/UST/SEIS 630/Wallet&retry_delay=3"
        connection = cx_Oracle.connect(username, password, connect_string)
        print("Successfully connected to Oracle Database")
        return connection
    except Exception as e:
        print(str(e))
        return None

def selectPlayer(cursor):
    try:
        sql = "SELECT * FROM Player"
        cursor.execute(sql,)
        rows = cursor.fetchall()
        col_names = [row[0] for row in cursor.description]
        for col in col_names:
            print(col)
        for row in rows:
            print(row)
    except cx_Oracle.Error as error:
        print('Error occurred:')
        print(error)

def insertPlayer(cursor, playerid):
    try:
        sql = "INSERT INTO PLAYER(player_id) VALUES(:playerid)"
        cursor.execute(sql, [playerid])
    except cx_Oracle.IntegrityError:
        return
    except cx_Oracle.Error as error:
        print('Error occurred:')
        print(error)

def insertTeam(cursor, teamId, teamLocation, teamname):
    try:
        sql = "INSERT INTO TEAM(teamid, teamlocation, teamname) VALUES(:teamId, :teamLocation, :teamname)"
        cursor.execute(sql, [teamId, teamLocation, teamname])
    except cx_Oracle.IntegrityError:
        return
    except cx_Oracle.Error as error:
        print('Error occurred:')
        print(error)

def insertGame(cursor, gameId, hometeam, awayteam, homeshots, awayshots, homescore, awayscore, winningdgoalieid, gamedate, venue):
    insertPlayer(cursor, winningdgoalieid)
    try:
        sql = "INSERT INTO Game(gameid, seasonid, hometeam, awayteam, homeshots, awayshots, homescore, awayscore, winninggoalieid, gamedate, venue) VALUES(:gameId, :seasonid, :hometeam, :awayteam, :homeshots, :awayshots, :homescore, :awayscore, :winninggoalieid,  TO_DATE(:gamedate,'YYYY-MM-DD'), :venue)"
        cursor.execute(sql, [gameId, season, hometeam, awayteam, homeshots, awayshots, homescore, awayscore, winningdgoalieid, gamedate, venue])

    except cx_Oracle.Error as error:
        print('Error occurred:')
        print(error)

def insertEventWithString(cursor, sql, vals):
    try:
        cursor.execute(sql, vals)
    except cx_Oracle.Error as error:
        print("***********************************************************************************************************************************************")
        print('Error occurred:')
        print(error)

def insertGeneralEvent(cursor, playid, gameid, period, timeremaining, name):
    try:
        sql = "INSERT INTO GameEvent(playid, game_gameid, game_seasonid, eventperiod, timeremaining, name) VALUES(:playid, :gameid, :season, :period, :timeremaining, :name)"
        cursor.execute(sql, [playid, gameid, season, period, timeremaining, name])
    except oracledb.IntegrityError as e:
        return
    except cx_Oracle.Error as error:
        print('Error occurred:')
        print(error)

def iteratePlays(cursor, plays, gameid):
    for play in plays:
        playid = play['eventId']
        event = play['typeDescKey']
        if 'details' in play.keys():
            details = play['details']
            assist2 = None
            
            if 'assist2PlayerId' in details.keys():
                assist2 = details['assist2PlayerId']
                insertPlayer(cursor, assist2)


            if event =='goal':

                if assist2 is not None:
                    print("\t" + str(event) + " at " + " id: " + str(playid) + " assister2: " + str(assist2))
                    sql = "UPDATE GameEvent SET Player_3 = :assist2 WHERE playid = :playid AND game_gameid = :gameid and game_seasonid = :seasonid"
                    vals = [assist2, playid, gameid, season]
                    insertEventWithString(cursor, sql, vals)

def iterateGames(cursor):
    games = getGames()
    print(str(len(games)) + " games")
    i = 0
    for game in games:
        gameId = game["id"]
        venue = game["venue"]['default']
        gameWinningGoalieId = game["winningGoalie"]["playerId"]
        homeTeamId = game["homeTeam"]['id']
        awayTeamId = game["awayTeam"]['id']
        homeTeamLocation = game["homeTeam"]['placeName']['default']
        awayTeamLocation = game["awayTeam"]['placeName']['default']
        gameDate = game['startTimeUTC'].split("T")[0]
        pbp = requests.get("https://api-web.nhle.com/v1/gamecenter/{}/play-by-play".format(gameId)).json()
        homeScore = pbp["homeTeam"]["score"]
        awayScore = pbp["awayTeam"]["score"]
        homeSog = pbp["homeTeam"]["sog"]
        awaySog = pbp["awayTeam"]["sog"]
        awayTeamName = pbp["awayTeam"]["name"]["default"]
        homeTeamName = pbp["homeTeam"]["name"]["default"]
        print(str(i) + " " + str(awayTeamName) + "(" + str(awayTeamId) + "): " + str(awayScore) + " at " + str(homeTeamName) + "(" + str(homeTeamId) + "): " + str(homeScore) + " on " + str(gameDate) + " in " + str(venue) + " won by " + str(gameWinningGoalieId) + ". Shots " + str(awaySog) + " " + str(homeSog))
        iteratePlays(cursor, pbp['plays'], gameId)
        i = i + 1
        


def main():
    conn = getConnection()
    cursor = conn.cursor()
    #insertPlayer(cursor, 123)
    #insertTeam(cursor, 1, "Saskatoon", "Blades")
    #insertTeam(cursor, 2, "Kelowna", "Rockets")
    #insertGame(cursor, 1, 1, 2, 33, 30, 1, 2, 123, "2023-11-06", "New Hope Ice Arena")
    #insertGeneralEvent(cursor, 1, 1, 1, "20:00", "Period Start")
    iterateGames(cursor)

    conn.commit()

main()