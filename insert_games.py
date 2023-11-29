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
        period = play['period']
        event = play['typeDescKey']
        timeLeft = play['timeRemaining']
        if 'details' in play.keys():
            details = play['details']
            shooter = None
            blocker = None
            goalie = None
            playTeamId = None
            hitter = None
            hittee = None
            FOwinner = None
            FOloser = None
            assist1 = None
            assist2 = None
            scorer = None
            reason = None
            shotype = None
            x = None
            y = None
            player = None
            penaltyName = None
            committedBy = None
            drawnBy = None
            penaltyLength = None


            if 'blockingPlayerId' in details.keys():
                blocker = details['blockingPlayerId']
                insertPlayer(cursor, blocker)

            if 'shootingPlayerId' in details.keys():
                shooter = details['shootingPlayerId']
                insertPlayer(cursor, shooter)

            if 'goalieInNetId' in details.keys():
                goalie = details['goalieInNetId']
                insertPlayer(cursor, goalie)

            if 'eventOwnerTeamId' in details.keys():
                playTeamId = details['eventOwnerTeamId']

            if 'hittingPlayerId' in details.keys():
                hitter = details['hittingPlayerId']
                insertPlayer(cursor, hitter)
            
            if 'hitteePlayerId' in details.keys():
                hittee = details['hitteePlayerId']
                insertPlayer(cursor, hittee)

            if 'losingPlayerId' in details.keys():
                FOloser = details['losingPlayerId']
                insertPlayer(cursor, FOloser)

            if 'winningPlayerId' in details.keys():
                FOwinner = details['winningPlayerId']
                insertPlayer(cursor, FOwinner)

            if 'assist1PlayerId' in details.keys():
                assist1 = details['assist1PlayerId']
                insertPlayer(cursor, assist1)
            
            if 'assist2PlayerId' in details.keys():
                assist2 = details['assist2PlayerId']
                insertPlayer(cursor, assist2)

            if 'scoringPlayerId' in details.keys():
                scorer = details['scoringPlayerId']
                insertPlayer(cursor, scorer)

            if 'reason' in details.keys():
                reason = details['reason']
            
            if 'playerId' in details.keys():
                player = details['playerId']
                insertPlayer(cursor, player)

            if 'xCoord' in  details.keys():
                x = details['xCoord']
            
            if 'yCoord' in  details.keys():
                y = details['yCoord']

            if 'shotType' in details.keys():
                shotype = details['shotType']

            if 'descKey' in details.keys():
                penaltyName = details['descKey']
            
            if 'committedByPlayerId' in details.keys():
                committedBy = details['committedByPlayerId']
                insertPlayer(cursor, committedBy)

            if 'drawnByPlayerId' in details.keys():
                drawnBy = details['drawnByPlayerId']
                insertPlayer(cursor, drawnBy)

            if 'duration' in details.keys():
                penaltyLength = details['duration']

            if event == 'period-start':
                #print("\t" + str(event) + " at " + str(timeLeft) + " in " + str(period) + " id: " + str(playid))
                insertGeneralEvent(cursor, playid, gameid, period, timeLeft, event)
            elif event == 'delayed-penalty':
                #print("\t" + str(event) + " at " + str(timeLeft) + " in " + str(period) + " id: " + str(playid))
                insertGeneralEvent(cursor, playid, gameid, period, timeLeft, event)
            elif event == "stoppage":
                #print("\t" + str(event) + " at " + str(timeLeft) + " in " + str(period) + " id: " + str(playid) + " reason: " + str(reason))
                sql = "INSERT INTO GameEvent(playid, game_gameid, game_seasonid, eventperiod, timeremaining, name, reason) VALUES(:playid, :gameid, :season, :period, :timeremaining, :event, :reason)"
                vals = [playid, gameid, season, period, timeLeft, event, reason]
                insertEventWithString(cursor, sql, vals)
            elif event =='hit':
                #print("\t" + str(event) + " at " + str(timeLeft) + " in " + str(period) + " id: " + str(playid) + " hitter: " + str(hitter) + " team: "  + str(playTeamId) + " hittee: " + str(hittee) + " x: " + str(x) + " y: " + str(y))
                sql = "INSERT INTO GameEvent(playid, game_gameid, game_seasonid, eventperiod, timeremaining, name, player_1, player_2, xcoord, ycoord, team_teamid) VALUES(:playid, :gameid, :season, :period, :timeremaining, :event, :hitter, :hittee, :x, :y, :playTeamId)"
                vals = [playid, gameid, season, period, timeLeft, event, hitter, hittee, x, y, playTeamId]
                insertEventWithString(cursor, sql, vals)
            elif event == 'giveaway' or event == 'takeaway':
                #print("\t" + str(event) + " at " + str(timeLeft) + " in " + str(period) + " id: " + str(playid) + " player: " + str(player) + " team: "  + str(playTeamId) + " x: " + str(x) + " y: " + str(y))
                sql = "INSERT INTO GameEvent(playid, game_gameid, game_seasonid, eventperiod, timeremaining, name, team_teamid, player_1, xcoord, ycoord) VALUES(:playid, :gameid, :season, :period, :timeremaining, :name, :playTeamId, :player, :x, :y)"
                vals = [playid, gameid, season, period, timeLeft, event, playTeamId, player, x, y]
                insertEventWithString(cursor, sql, vals)
            elif event == 'faceoff':
                #print("\t" + str(event) + " at " + str(timeLeft) + " in " + str(period) + " id: " + str(playid) + " winner: " + str(FOwinner) + " loser: " + str(FOloser) + " team: " + str(playTeamId) + " x: " + str(x) + " y: " + str(y))
                sql = "INSERT INTO GameEvent(playid, game_gameid, game_seasonid, eventperiod, timeremaining, name, player_1, player_2, xcoord, ycoord, team_teamid) VALUES(:playid, :gameid, :season, :period, :timeremaining, :event, :FOwinner, :FOloser, :x, :y, :playTeamId)"
                vals = [playid, gameid, season, period, timeLeft, event,  FOwinner, FOloser, x, y, playTeamId]
                insertEventWithString(cursor, sql, vals)
            elif event == 'blocked-shot':
                #print("\t" + str(event) + " at " + str(timeLeft) + " in " + str(period) + " id: " + str(playid) + " team: " + str(playTeamId) + " shooter: " + str(shooter) + " blocker: " + str(blocker) + " x: " + str(x) + " y: " + str(y))
                sql = "INSERT INTO GameEvent(playid, game_gameid, game_seasonid, eventperiod, timeremaining, name, player_1, player_2, xcoord, ycoord, team_teamid) VALUES(:playid, :gameid, :season, :period, :timeremaining, :event, :shooter, :blocker, :x, :y, :playTeamId)"
                vals = [playid, gameid, season, period, timeLeft, event,  shooter, blocker, x, y, playTeamId]
                insertEventWithString(cursor, sql, vals)
            elif event == 'shot-on-goal':
                #print("\t" + str(event) + " at " + str(timeLeft) + " in " + str(period) + " id: " + str(playid) + " team: " + str(playTeamId) + " shooter: " + str(shooter) + " goalie: " + str(goalie) + " x: " + str(x) + " y: " + str(y) + " type: " + str(shotype))
                sql = "INSERT INTO GameEvent(playid, game_gameid, game_seasonid, eventperiod, timeremaining, name, player_1, goalie, xcoord, ycoord, team_teamid, shottype) VALUES(:playid, :gameid, :season, :period, :timeremaining, :event, :shooter, :goalie, :x, :y, :playTeamId, :shotype)"
                vals = [playid, gameid, season, period, timeLeft, event, shooter, goalie, x, y, playTeamId, shotype]
                insertEventWithString(cursor, sql, vals)
            elif event == 'missed-shot':
                #print("\t" + str(event) + " at " + str(timeLeft) + " in " + str(period) + " id: " + str(playid) + " team: " + str(playTeamId) + " shooter: " + str(shooter) + " goalie: " + str(goalie) + " x: " + str(x) + " y: " + str(y) + " type: " + str(shotype))
                sql = "INSERT INTO GameEvent(playid, game_gameid, game_seasonid, eventperiod, timeremaining, name, player_1, goalie, xcoord, ycoord, team_teamid, reason) VALUES(:playid, :gameid, :season, :period, :timeremaining, :event, :shooter, :goalie, :x, :y, :playTeamId, :reason)"
                vals = [playid, gameid, season, period, timeLeft, event, shooter, goalie, x, y, playTeamId, reason]
                insertEventWithString(cursor, sql, vals)
            elif event =='goal':
                if assist1 is not None:
                    #print("\t" + str(event) + " at " + str(timeLeft) + " in " + str(period) + " id: " + str(playid) + " team: " + str(playTeamId) + " scorer: " + str(scorer) + " assister: " + str(assist1) + " goalie: " + str(goalie) + " x: " + str(x) + " y: " + str(y) + " type: " + str(shotype))
                    sql = "INSERT INTO GameEvent(playid, game_gameid, game_seasonid, eventperiod, timeremaining, name, player_1, goalie, xcoord, ycoord, team_teamid, player_2) VALUES(:playid, :gameid, :season, :period, :timeremaining, :event, :scorer, :goalie, :x, :y, :playTeamId, :assist1)"
                    vals = [playid, gameid, season, period, timeLeft, event, scorer, goalie, x, y, playTeamId, assist1]
                    insertEventWithString(cursor, sql, vals)
                elif assist2 is not None:
                    #print("\t" + str(event) + " at " + str(timeLeft) + " in " + str(period) + " id: " + str(playid) + " team: " + str(playTeamId) + " scorer: " + str(scorer) + " assister1: " + str(assist1) + " assister2: " + str(assist2) + " goalie: " + str(goalie) + " x: " + str(x) + " y: " + str(y) + " type: " + str(shotype))
                    sql = "INSERT INTO GameEvent(playid, game_gameid, game_seasonid, eventperiod, timeremaining, name, player_1, goalie, xcoord, ycoord, team_teamid, player_2, player_3) VALUES(:playid, :gameid, :season, :period, :timeremaining, :event, :scorer, :goalie, :x, :y, :playTeamId, :assist1, :assist2)"
                    vals = [playid, gameid, season, period, timeLeft, event,  scorer, goalie, x, y, playTeamId, assist1, assist2]
                    insertEventWithString(cursor, sql, vals)
                else:
                    #print("\t" + str(event) + " at " + str(timeLeft) + " in " + str(period) + " id: " + str(playid) + " team: " + str(playTeamId) + " scorer: " + str(scorer) + " goalie: " + str(goalie) + " x: " + str(x) + " y: " + str(y) + " type: " + str(shotype))
                    sql = "INSERT INTO GameEvent(playid, game_gameid, game_seasonid, eventperiod, timeremaining, name, player_1, goalie, xcoord, ycoord, team_teamid) VALUES(:playid, :gameid, :season, :period, :timeremaining, :event, :scorer, :goalie, :x, :y, :playTeamId)"
                    vals = [playid, gameid, season, period, timeLeft, event,  scorer, goalie, x, y, playTeamId]
                    insertEventWithString(cursor, sql, vals)
            elif event =='penalty':
                #print("\t" + str(event) + " at " + str(timeLeft) + " in " + str(period) + " id: " + str(playid) + " penalty: " + str(penaltyName) + " by: " + str(committedBy) + " drawn by: " + str(drawnBy) + " for: " + str(penaltyLength) +" minutes team: " + str(playTeamId) + " x: " + str(x) + " y: " + str(y))
                sql = "INSERT INTO GameEvent(playid, game_gameid, game_seasonid, eventperiod, timeremaining, name, player_1, player_2, xcoord, ycoord, team_teamid, reason, penmin) VALUES(:playid, :gameid, :season, :period, :timeremaining, :event, :committedBy, :drawnBy, :x, :y, :playTeamId, :penaltyName, :penaltyLength)"
                vals = [playid, gameid, season, period, timeLeft, event, committedBy, drawnBy, x, y, playTeamId, penaltyName, penaltyLength]
                insertEventWithString(cursor, sql, vals)
            else:
                insertGeneralEvent(cursor, playid, gameid, period, timeLeft, event)
                #print("\t" + str(event) + " at " + str(timeLeft) + " in " + str(period) + " id: " + str(playid))
                #print("\t\t" + str(details))
        else:
            #print("\t" + str(event) + " at " + str(timeLeft) + " in " + str(period) + " id: " + str(playid))
            insertGeneralEvent(cursor, playid, gameid, period, timeLeft, event)
        

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

        insertTeam(cursor, homeTeamId, homeTeamLocation, homeTeamName)
        insertTeam(cursor, awayTeamId, awayTeamLocation, awayTeamName)


        print(str(i) + " " + str(awayTeamName) + "(" + str(awayTeamId) + "): " + str(awayScore) + " at " + str(homeTeamName) + "(" + str(homeTeamId) + "): " + str(homeScore) + " on " + str(gameDate) + " in " + str(venue) + " won by " + str(gameWinningGoalieId) + ". Shots " + str(awaySog) + " " + str(homeSog))
        insertGame(cursor, gameId, homeTeamId, awayTeamId, homeSog, awaySog, homeScore,  awayScore, gameWinningGoalieId, gameDate, venue)
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