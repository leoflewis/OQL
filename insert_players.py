import requests
import oracledb
import cx_Oracle
import os

cx_Oracle.init_oracle_client(lib_dir="C:\Program Files\instantclient_21_12")

season = 20232024
teams = requests.get("https://api.nhle.com/stats/rest/en/team").json()['data']

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
        sql = "SELECT player_id FROM Player WHERE Fullname is null"
        cursor.execute(sql,)
        rows = cursor.fetchall()
        col_names = [row[0] for row in cursor.description]
        
        return rows
    except cx_Oracle.Error as error:
        print('Error occurred:')
        print(error)

def updatePlayerNoDraft(playerid, fullname, position, cursor):
    try:
        sql = "UPDATE Player SET fullname = :fullname, pposition = :position WHERE player_id = :playerid"
        cursor.execute(sql, [fullname, position, playerid])
    except oracledb.IntegrityError as e:
        return
    except cx_Oracle.Error as error:
        print('Error occurred:')
        print(error)

def insertDraft(playerid, dposition, round, year, team, cursor):
    try:
        sql = "INSERT INTO Draft(Playerid, draftyear, draftposition, draftround, teamid) VALUES(:playerid, :year, :dposition, :round, :team)"
        cursor.execute(sql, [playerid, year, dposition, round, team])
    except oracledb.IntegrityError as e:
        return
    except cx_Oracle.Error as error:
        print('Error occurred:')
        print(error)

def updatePlayerWithDraft(playerid, fullname, year, dposition, position, round, cursor):
    try:
        sql = "UPDATE PLAYER SET draftyear = :year, draftposition = :dposition, draftround = :round, fullname = :fullname, pposition = :position WHERE Player_id = :playerid"
        cursor.execute(sql, [year, dposition, round, fullname, position, playerid])
    except oracledb.IntegrityError as e:
        return
    except cx_Oracle.Error as error:
        print('Error occurred:')
        print(error)


def iteratePlayers(players, cursor):
    for player in players:
        playerid = player[0]
        playerInfo = requests.get("https://api-web.nhle.com/v1/player/{}/landing".format(playerid)).json()
        playerName = playerInfo['firstName']['default'] + " " + playerInfo['lastName']['default']
        playerPos =  playerInfo['position']
        updatePlayerNoDraft(playerid, playerName, playerPos, cursor)
            


def main():
    conn = getConnection()
    cursor = conn.cursor()
    players = selectPlayer(cursor)
    iteratePlayers(players, cursor)
    conn.commit()

main()